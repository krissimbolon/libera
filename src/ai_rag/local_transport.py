"""Evidence-bearing Ollama requests stay on literal loopback; no redirects."""
import ipaddress
import urllib.parse
import urllib.request

class LocalTransportError(ValueError):
    pass

def validate_local_url(url):
    parts=urllib.parse.urlsplit(url)
    if parts.scheme not in {'http','https'} or parts.username or parts.password or parts.fragment:
        raise LocalTransportError('Ollama endpoint must be a credential-free loopback HTTP URL')
    host=parts.hostname or ''
    # Resolve localhost to a literal address to avoid DNS alias behavior.
    if host.casefold()=='localhost':
        port=f':{parts.port}' if parts.port else ''
        return urllib.parse.urlunsplit((parts.scheme,'127.0.0.1'+port,parts.path,parts.query,''))
    try: local=ipaddress.ip_address(host).is_loopback
    except ValueError: local=False
    if not local: raise LocalTransportError('Ollama endpoint must use literal loopback IP or localhost')
    return url

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise LocalTransportError('Ollama redirects are forbidden')

def local_urlopen(request, timeout):
    url=request.full_url if isinstance(request,urllib.request.Request) else request
    safe=validate_local_url(url)
    if isinstance(request,urllib.request.Request):
        request=urllib.request.Request(safe,data=request.data,headers=dict(request.headers),method=request.get_method())
    else: request=safe
    # Disable environment proxies as evidence must never transit a proxy.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    return opener.open(request,timeout=timeout)
