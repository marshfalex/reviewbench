import abc
import asyncio
import base64
import hashlib
import inspect
import keyword
import os
import re
import warnings
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Container,
    Dict,
    Final,
    Generator,
    Iterable,
    Iterator,
    List,
    Mapping,
    NoReturn,
    Optional,
    Pattern,
    Set,
    Sized,
    Tuple,
    Type,
    TypedDict,
    Union,
    cast,
)

from yarl import URL, __version__ as yarl_version  # type: ignore[attr-defined]

from . import hdrs
from .abc import AbstractMatchInfo, AbstractRouter, AbstractView
from .helpers import DEBUG
from .http import HttpVersion11
from .typedefs import Handler, PathLike
from .web_exceptions import (
    HTTPException,
    HTTPExpectationFailed,
    HTTPForbidden,
    HTTPMethodNotAllowed,
    HTTPNotFound,
)
from .web_fileresponse import FileResponse
from .web_request import Request
from .web_response import Response, StreamResponse
from .web_routedef import AbstractRouteDef

__all__ = (
    "UrlDispatcher",
    "UrlMappingMatchInfo",
# [... lines 61-538 of the upstream file omitted ...]
class StaticResource(PrefixResource):
    VERSION_KEY = "v"

    def __init__(
        self,
        prefix: str,
        directory: PathLike,
        *,
        name: Optional[str] = None,
        expect_handler: Optional[_ExpectHandler] = None,
        chunk_size: int = 256 * 1024,
        show_index: bool = False,
        follow_symlinks: bool = False,
        append_version: bool = False,
    ) -> None:
        super().__init__(prefix, name=name)
        try:
            directory = Path(directory)
            if str(directory).startswith("~"):
                directory = Path(os.path.expanduser(str(directory)))
            directory = directory.resolve()
            if not directory.is_dir():
                raise ValueError("Not a directory")
        except (FileNotFoundError, ValueError) as error:
            raise ValueError(f"No directory exists at '{directory}'") from error
        self._directory = directory
        self._show_index = show_index
        self._chunk_size = chunk_size
        self._follow_symlinks = follow_symlinks
        self._expect_handler = expect_handler
        self._append_version = append_version

        self._routes = {
            "GET": ResourceRoute(
                "GET", self._handle, self, expect_handler=expect_handler
            ),
            "HEAD": ResourceRoute(
                "HEAD", self._handle, self, expect_handler=expect_handler
            ),
        }

    def url_for(  # type: ignore[override]
        self,
        *,
        filename: PathLike,
        append_version: Optional[bool] = None,
    ) -> URL:
        if append_version is None:
            append_version = self._append_version
        filename = str(filename).lstrip("/")

        url = URL.build(path=self._prefix, encoded=True)
        # filename is not encoded
        if YARL_VERSION < (1, 6):
            url = url / filename.replace("%", "%25")
        else:
            url = url / filename

        if append_version:
            unresolved_path = self._directory.joinpath(filename)
            try:
                if self._follow_symlinks:
                    normalized_path = Path(os.path.normpath(unresolved_path))
                    normalized_path.relative_to(self._directory)
                    filepath = normalized_path.resolve()
                else:
                    filepath = unresolved_path.resolve()
                    filepath.relative_to(self._directory)
            except (ValueError, FileNotFoundError):
                # ValueError for case when path point to symlink
                # with follow_symlinks is False
                return url  # relatively safe
            if filepath.is_file():
                # TODO cache file content
                # with file watcher for cache invalidation
                with filepath.open("rb") as f:
                    file_bytes = f.read()
                h = self._get_file_hash(file_bytes)
                url = url.with_query({self.VERSION_KEY: h})
                return url
        return url

    @staticmethod
    def _get_file_hash(byte_array: bytes) -> str:
        m = hashlib.sha256()  # todo sha256 can be configurable param
        m.update(byte_array)
        b64 = base64.urlsafe_b64encode(m.digest())
        return b64.decode("ascii")

    def get_info(self) -> _InfoDict:
        return {
            "directory": self._directory,
            "prefix": self._prefix,
            "routes": self._routes,
        }

    def set_options_route(self, handler: Handler) -> None:
        if "OPTIONS" in self._routes:
            raise RuntimeError("OPTIONS route was set already")
        self._routes["OPTIONS"] = ResourceRoute(
            "OPTIONS", handler, self, expect_handler=self._expect_handler
        )

    async def resolve(self, request: Request) -> _Resolve:
        path = request.rel_url.raw_path
        method = request.method
        allowed_methods = set(self._routes)
        if not path.startswith(self._prefix2) and path != self._prefix:
            return None, set()

        if method not in allowed_methods:
            return None, allowed_methods

        match_dict = {"filename": _unquote_path(path[len(self._prefix) + 1 :])}
        return (UrlMappingMatchInfo(match_dict, self._routes[method]), allowed_methods)

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._routes.values())

    async def _handle(self, request: Request) -> StreamResponse:
        rel_url = request.match_info["filename"]
        try:
            filename = Path(rel_url)
            if filename.anchor:
                # rel_url is an absolute name like
                # /static/\\machine_name\c$ or /static/D:\path
                # where the static dir is totally different
                raise HTTPForbidden()
            unresolved_path = self._directory.joinpath(filename)
            if self._follow_symlinks:
                normalized_path = Path(os.path.normpath(unresolved_path))
                normalized_path.relative_to(self._directory)
                filepath = normalized_path.resolve()
            else:
                filepath = unresolved_path.resolve()
                filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            # relatively safe
            raise HTTPNotFound() from error
        except HTTPForbidden:
            raise
        except Exception as error:
            # perm error or other kind!
            request.app.logger.exception(error)
            raise HTTPNotFound() from error

        # on opening a dir, load its contents if allowed
        if filepath.is_dir():
            if self._show_index:
                try:
                    return Response(
                        text=self._directory_as_html(filepath), content_type="text/html"
                    )
                except PermissionError:
                    raise HTTPForbidden()
            else:
                raise HTTPForbidden()
        elif filepath.is_file():
            return FileResponse(filepath, chunk_size=self._chunk_size)
        else:
            raise HTTPNotFound

# [... lines 704-1232 of the upstream file omitted ...]
