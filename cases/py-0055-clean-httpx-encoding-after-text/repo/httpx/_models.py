# Excerpt of httpx/_models.py from an upstream project; code outside the functions below is omitted.
import datetime
import email.message
import json as jsonlib
import typing
import urllib.request
from collections.abc import Mapping
from http.cookiejar import Cookie, CookieJar
from ._content import ByteStream, UnattachedStream, encode_request, encode_response
from ._decoders import (
    SUPPORTED_DECODERS,
    ByteChunker,
    ContentDecoder,
    IdentityDecoder,
    LineDecoder,
    MultiDecoder,
    TextChunker,
    TextDecoder,
)
from ._exceptions import (
    CookieConflict,
    HTTPStatusError,
    RequestNotRead,
    ResponseNotRead,
    StreamClosed,
    StreamConsumed,
    request_context,
)
from ._multipart import get_multipart_boundary_from_content_type
from ._status_codes import codes
from ._types import (
    AsyncByteStream,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    ResponseContent,
    ResponseExtensions,
    SyncByteStream,
)
from ._urls import URL
from ._utils import (
    guess_json_utf,
    is_known_encoding,
    normalize_header_key,
    normalize_header_value,
    obfuscate_sensitive_headers,
    parse_content_type_charset,
    parse_header_links,
)



class Response:
    # [... omitted ...]

    @encoding.setter
    def encoding(self, value: str) -> None:
        self._encoding = value
