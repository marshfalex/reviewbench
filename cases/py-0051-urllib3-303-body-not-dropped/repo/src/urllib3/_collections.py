# Excerpt of src/urllib3/_collections.py from an upstream project; code outside the functions below is omitted.
from __future__ import annotations
import typing
from collections import OrderedDict
from enum import Enum, auto
from threading import RLock


if typing.TYPE_CHECKING:
    # We can only import Protocol if TYPE_CHECKING because it's a development
    # dependency, and is not available at runtime.
    from typing_extensions import Protocol, Self

    class HasGettableStringKeys(Protocol):
        def keys(self) -> typing.Iterator[str]:
            ...

        def __getitem__(self, key: str) -> str:
            ...


class HTTPHeaderDict:
    # [... omitted ...]

    def _prepare_for_method_change(self) -> Self:
        """
        Remove content-specific header fields before changing the request
        method to GET or HEAD according to RFC 9110, Section 15.4.
        """
        content_specific_headers = [
            "Content-Encoding",
            "Content-Language",
            "Content-Location",
            "Content-Type",
            "Content-Length",
            "Digest",
            "Last-Modified",
        ]
        for header in content_specific_headers:
            self.discard(header)
        return self
