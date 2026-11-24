# Excerpt of src/urllib3/poolmanager.py from an upstream project; code outside the functions below is omitted.
from __future__ import annotations
import functools
import logging
import typing
import warnings
from types import TracebackType
from urllib.parse import urljoin
from ._collections import HTTPHeaderDict, RecentlyUsedContainer
from ._request_methods import RequestMethods
from .connection import ProxyConfig
from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool, port_by_scheme
from .exceptions import (
    LocationValueError,
    MaxRetryError,
    ProxySchemeUnknown,
    URLSchemeUnknown,
)
from .response import BaseHTTPResponse
from .util.connection import _TYPE_SOCKET_OPTIONS
from .util.proxy import connection_requires_http_tunnel
from .util.retry import Retry
from .util.timeout import Timeout
from .util.url import Url, parse_url



class PoolManager:
    # [... omitted ...]

    def urlopen(  # type: ignore[override]
        self, method: str, url: str, redirect: bool = True, **kw: typing.Any
    ) -> BaseHTTPResponse:
        """
        Same as :meth:`urllib3.HTTPConnectionPool.urlopen`
        with custom cross-host redirect logic and only sends the request-uri
        portion of the ``url``.

        The given ``url`` parameter must be absolute, such that an appropriate
        :class:`urllib3.connectionpool.ConnectionPool` can be chosen for it.
        """
        u = parse_url(url)

        if u.scheme is None:
            warnings.warn(
                "URLs without a scheme (ie 'https://') are deprecated and will raise an error "
                "in a future version of urllib3. To avoid this DeprecationWarning ensure all URLs "
                "start with 'https://' or 'http://'. Read more in this issue: "
                "https://github.com/urllib3/urllib3/issues/2920",
                category=DeprecationWarning,
                stacklevel=2,
            )

        conn = self.connection_from_host(u.host, port=u.port, scheme=u.scheme)

        kw["assert_same_host"] = False
        kw["redirect"] = False

        if "headers" not in kw:
            kw["headers"] = self.headers

        if self._proxy_requires_url_absolute_form(u):
            response = conn.urlopen(method, url, **kw)
        else:
            response = conn.urlopen(method, u.request_uri, **kw)

        redirect_location = redirect and response.get_redirect_location()
        if not redirect_location:
            return response

        # Support relative URLs for redirecting.
        redirect_location = urljoin(url, redirect_location)

        if response.status == 303:
            # Change the method according to RFC 9110, Section 15.4.4.
            method = "GET"
            # And lose the body not to transfer anything sensitive.
            kw["body"] = None
            kw["headers"] = HTTPHeaderDict(kw["headers"])._prepare_for_method_change()

        retries = kw.get("retries")
        if not isinstance(retries, Retry):
            retries = Retry.from_int(retries, redirect=redirect)

        # Strip headers marked as unsafe to forward to the redirected location.
        # Check remove_headers_on_redirect to avoid a potential network call within
        # conn.is_same_host() which may use socket.gethostbyname() in the future.
        if retries.remove_headers_on_redirect and not conn.is_same_host(
            redirect_location
        ):
            new_headers = kw["headers"].copy()
            for header in kw["headers"]:
                if header.lower() in retries.remove_headers_on_redirect:
                    new_headers.pop(header, None)
            kw["headers"] = new_headers

        try:
            retries = retries.increment(method, url, response=response, _pool=conn)
        except MaxRetryError:
            if retries.raise_on_redirect:
                response.drain_conn()
                raise
            return response

        kw["retries"] = retries
        kw["redirect"] = redirect

        log.info("Redirecting %s -> %s", url, redirect_location)

        response.drain_conn()
        return self.urlopen(method, redirect_location, **kw)
