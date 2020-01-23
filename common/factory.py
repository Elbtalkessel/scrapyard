from datetime import datetime
import typing
from itertools import cycle
import dataclasses
from urllib import request
import random
import re


def fetch_path(path: str):
    def from_url(url: str) -> list:
        response = request.urlopen(url)
        return [l.decode('utf-8').strip() for l in response.readlines()]

    def from_file(path: str) -> list:
        with open(path, 'r') as f:
            return [l.strip() for l in f.readlines()]

    proxies = from_url(path) if path.startswith('http') else from_file(path)
    return proxies


def cycle_lines(path):
    with open(path) as f:
        strings = [s.strip() for s in f.readlines()]
    return cycle(strings)


@dataclasses.dataclass
class ProxySettings:
    host: str
    username: str = None
    password: str = None
    port: int = None
    protocol: str = 'http'

    @classmethod
    def fromstring(cls, string: str, **kwargs) -> 'ProxySettings':
        """
        string formats:
            [protocol://]ip:port
            [protocol://]username:password@ip:port
            [protocol://]host:port
            [protocol://]username:password@host:port
        HTTP protocol by default or protocol from this method params
        """
        rgx = re.compile(
            r'((?P<protocol>((https?)|(socks5h)))://)?'
            r'((?P<username>\w+):(?P<password>[^\W]+)@)?'
            r'(?P<host>[\d\w.]+):(?P<port>\d+)'
        )
        matched = rgx.match(string).groupdict()
        matched.update(kwargs)
        return cls(**matched)

    @classmethod
    def factory(cls, path: str, refresh_each=None) -> typing.Generator['ProxySettings', None, None]:
        def fetch():
            prx = fetch_path(path)
            random.shuffle(prx)
            return cycle(prx)

        proxies = fetch()
        last_fetch = datetime.now()
        while True:
            yield ProxySettings.fromstring(next(proxies))
            if refresh_each and (datetime.now() - last_fetch).seconds >= refresh_each:
                proxies = fetch()
                last_fetch = datetime.now()


