from git.types import PathLike
import os

from git.compat import defenc
from git.objects import Object
from git.objects.commit import Commit
from git.util import (
    join_path,
    join_path_native,
    to_native_path_linux,
    assure_directory_exists,
    hex_to_bin,
    LockedFD,
)
from gitdb.exc import BadObject, BadName

from .log import RefLog

# typing ------------------------------------------------------------------

from typing import (
    Any,
    Iterator,
    List,
    Tuple,
    Type,
    TypeVar,
    Union,
    TYPE_CHECKING,
    cast,
)  # NOQA
from git.types import Commit_ish, PathLike  # NOQA

if TYPE_CHECKING:
    from git.repo import Repo
    from git.refs import Head, TagReference, RemoteReference, Reference
    from .log import RefLogEntry
    from git.config import GitConfigParser
    from git.objects.commit import Actor


T_References = TypeVar("T_References", bound="SymbolicReference")

# ------------------------------------------------------------------------------


__all__ = ["SymbolicReference"]


def _git_dir(repo: "Repo", path: Union[PathLike, None]) -> PathLike:
    """Find the git dir that's appropriate for the path"""
    name = f"{path}"
    if name in ["HEAD", "ORIG_HEAD", "FETCH_HEAD", "index", "logs"]:
        return repo.git_dir
    return repo.common_dir


class SymbolicReference(object):

    """Represents a special case of a reference such that this reference is symbolic.
    It does not point to a specific commit, but to another Head, which itself
    specifies a commit.

    A typical example for a symbolic reference is HEAD."""

    __slots__ = ("repo", "path")
    _resolve_ref_on_create = False
    _points_to_commits_only = True
    _common_path_default = ""
    _remote_common_path_default = "refs/remotes"
# [... lines 71-149 of the upstream file omitted ...]

    @classmethod
    def dereference_recursive(cls, repo: "Repo", ref_path: Union[PathLike, None]) -> str:
        """
        :return: hexsha stored in the reference at the given ref_path, recursively dereferencing all
            intermediate references as required
        :param repo: the repository containing the reference at ref_path"""

        while True:
            hexsha, ref_path = cls._get_ref_info(repo, ref_path)
            if hexsha is not None:
                return hexsha
        # END recursive dereferencing

    @classmethod
    def _get_ref_info_helper(
        cls, repo: "Repo", ref_path: Union[PathLike, None]
    ) -> Union[Tuple[str, None], Tuple[None, str]]:
        """Return: (str(sha), str(target_ref_path)) if available, the sha the file at
        rela_path points to, or None. target_ref_path is the reference we
        point to, or None"""
        if ".." in str(ref_path):
            raise ValueError(f"Invalid reference '{ref_path}'")
        tokens: Union[None, List[str], Tuple[str, str]] = None
        repodir = _git_dir(repo, ref_path)
        try:
            with open(os.path.join(repodir, str(ref_path)), "rt", encoding="UTF-8") as fp:
                value = fp.read().rstrip()
            # Don't only split on spaces, but on whitespace, which allows to parse lines like
            # 60b64ef992065e2600bfef6187a97f92398a9144                branch 'master' of git-server:/path/to/repo
            tokens = value.split()
            assert len(tokens) != 0
        except OSError:
            # Probably we are just packed, find our entry in the packed refs file
            # NOTE: We are not a symbolic ref if we are in a packed file, as these
            # are excluded explicitly
            for sha, path in cls._iter_packed_refs(repo):
                if path != ref_path:
                    continue
                # sha will be used
                tokens = sha, path
                break
            # END for each packed ref
        # END handle packed refs
        if tokens is None:
            raise ValueError("Reference at %r does not exist" % ref_path)

        # is it a reference ?
        if tokens[0] == "ref:":
            return (None, tokens[1])

        # its a commit
        if repo.re_hexsha_only.match(tokens[0]):
            return (tokens[0], None)

        raise ValueError("Failed to parse reference information from %r" % ref_path)

    @classmethod
    def _get_ref_info(cls, repo: "Repo", ref_path: Union[PathLike, None]) -> Union[Tuple[str, None], Tuple[None, str]]:
        """Return: (str(sha), str(target_ref_path)) if available, the sha the file at
        rela_path points to, or None. target_ref_path is the reference we
        point to, or None"""
        return cls._get_ref_info_helper(repo, ref_path)

    def _get_object(self) -> Commit_ish:
        """
# [... lines 216-769 of the upstream file omitted ...]
