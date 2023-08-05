import ssl
import urllib3
from requests.adapters import HTTPAdapter


class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""

    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=0')  # Decreases the security level for requests amount
        self.poolmanager = urllib3.poolmanager.PoolManager(
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx
        )
