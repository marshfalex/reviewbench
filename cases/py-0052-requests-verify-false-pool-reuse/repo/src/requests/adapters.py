# Excerpt of src/requests/adapters.py from an upstream project; code outside the functions below is omitted.
import os.path
import socket  # noqa: F401
import typing
from urllib3.exceptions import ClosedPoolError, ConnectTimeoutError
from urllib3.exceptions import HTTPError as _HTTPError
from urllib3.exceptions import InvalidHeader as _InvalidHeader
from urllib3.exceptions import (
    LocationValueError,
    MaxRetryError,
    NewConnectionError,
    ProtocolError,
)
from urllib3.exceptions import ProxyError as _ProxyError
from urllib3.exceptions import ReadTimeoutError, ResponseError
from urllib3.exceptions import SSLError as _SSLError
from urllib3.poolmanager import PoolManager, proxy_from_url
from urllib3.util import Timeout as TimeoutSauce
from urllib3.util import parse_url
from urllib3.util.retry import Retry
from .auth import _basic_auth_str
from .compat import basestring, urlparse
from .cookies import extract_cookies_to_jar
from .exceptions import (
    ConnectionError,
    ConnectTimeout,
    InvalidHeader,
    InvalidProxyURL,
    InvalidSchema,
    InvalidURL,
    ProxyError,
    ReadTimeout,
    RetryError,
    SSLError,
)
from .models import Response
from .structures import CaseInsensitiveDict
from .utils import (
    DEFAULT_CA_BUNDLE_PATH,
    extract_zipped_paths,
    get_auth_from_url,
    get_encoding_from_headers,
    prepend_scheme_if_needed,
    select_proxy,
    urldefragauth,
)


if typing.TYPE_CHECKING:
    from .models import PreparedRequest

DEFAULT_POOLBLOCK = False


def _urllib3_request_context(
    request: "PreparedRequest", verify: "bool | str | None"
) -> "(typing.Dict[str, typing.Any], typing.Dict[str, typing.Any])":
    host_params = {}
    pool_kwargs = {}
    parsed_request_url = urlparse(request.url)
    scheme = parsed_request_url.scheme.lower()
    port = parsed_request_url.port
    cert_reqs = "CERT_REQUIRED"
    if verify is False:
        cert_reqs = "CERT_NONE"
    if isinstance(verify, str):
        pool_kwargs["ca_certs"] = verify
    pool_kwargs["cert_reqs"] = cert_reqs
    host_params = {
        "scheme": scheme,
        "host": parsed_request_url.hostname,
        "port": port,
    }
    return host_params, pool_kwargs


class HTTPAdapter:
    # [... omitted ...]

    def _get_connection(self, request, verify, proxies=None):
        # Replace the existing get_connection without breaking things and
        # ensure that TLS settings are considered when we interact with
        # urllib3 HTTP Pools
        proxy = select_proxy(request.url, proxies)
        try:
            host_params, pool_kwargs = _urllib3_request_context(request, verify)
        except ValueError as e:
            raise InvalidURL(e, request=request)
        if proxy:
            proxy = prepend_scheme_if_needed(proxy, "http")
            proxy_url = parse_url(proxy)
            if not proxy_url.host:
                raise InvalidProxyURL(
                    "Please check proxy URL. It is malformed "
                    "and could be missing the host."
                )
            proxy_manager = self.proxy_manager_for(proxy)
            conn = proxy_manager.connection_from_host(
                **host_params, pool_kwargs=pool_kwargs
            )
        else:
            # Only scheme should be lower case
            conn = self.poolmanager.connection_from_host(
                **host_params, pool_kwargs=pool_kwargs
            )

        return conn

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """Sends PreparedRequest object. Returns Response object.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """

        try:
            conn = self._get_connection(request, verify, proxies)
        except LocationValueError as e:
            raise InvalidURL(e, request=request)

        self.cert_verify(conn, request.url, verify, cert)
        url = self.request_url(request, proxies)
        self.add_headers(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )

        chunked = not (request.body is None or "Content-Length" in request.headers)

        if isinstance(timeout, tuple):
            try:
                connect, read = timeout
                timeout = TimeoutSauce(connect=connect, read=read)
            except ValueError:
                raise ValueError(
                    f"Invalid timeout {timeout}. Pass a (connect, read) timeout tuple, "
                    f"or a single float to set both timeouts to the same value."
                )
        elif isinstance(timeout, TimeoutSauce):
            pass
        else:
            timeout = TimeoutSauce(connect=timeout, read=timeout)

        try:
            resp = conn.urlopen(
                method=request.method,
                url=url,
                body=request.body,
                headers=request.headers,
                redirect=False,
                assert_same_host=False,
                preload_content=False,
                decode_content=False,
                retries=self.max_retries,
                timeout=timeout,
                chunked=chunked,
            )

        except (ProtocolError, OSError) as err:
            raise ConnectionError(err, request=request)

        except MaxRetryError as e:
            if isinstance(e.reason, ConnectTimeoutError):
                # TODO: Remove this in 3.0.0: see #2811
                if not isinstance(e.reason, NewConnectionError):
                    raise ConnectTimeout(e, request=request)

            if isinstance(e.reason, ResponseError):
                raise RetryError(e, request=request)

            if isinstance(e.reason, _ProxyError):
                raise ProxyError(e, request=request)

            if isinstance(e.reason, _SSLError):
                # This branch is for urllib3 v1.22 and later.
                raise SSLError(e, request=request)

            raise ConnectionError(e, request=request)

        except ClosedPoolError as e:
            raise ConnectionError(e, request=request)

        except _ProxyError as e:
            raise ProxyError(e)

        except (_SSLError, _HTTPError) as e:
            if isinstance(e, _SSLError):
                # This branch is for urllib3 versions earlier than v1.22
                raise SSLError(e, request=request)
            elif isinstance(e, ReadTimeoutError):
                raise ReadTimeout(e, request=request)
            elif isinstance(e, _InvalidHeader):
                raise InvalidHeader(e, request=request)
            else:
                raise

        return self.build_response(request, resp)
