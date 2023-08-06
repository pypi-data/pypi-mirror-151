from typing import Sequence

import requests as rq
import urllib.parse
import json
import re


class Repository:
    def __init__(self, owner: str, reponame: str, oauth_token: str = None) -> None:
        self.owner = owner
        self.reponame = reponame

        self.oauth_token = oauth_token

    @classmethod
    def fromURL(cls, url, *args, **kw):
        return cls(*re.findall(r".*github.com/(.*)/(.*)", url)[0], *args, **kw)

    @property
    def urlhttp(self):
        return f"https://github.com/{self.owner}/{self.reponame}"

    @property
    def urlapi(self):
        return f"https://api.github.com/repos/{self.owner}/{self.reponame}"

    def getcommits(self, **kw) -> Sequence[dict]:
        for k in kw:
            if k not in ("per_page", "author", "since", "page", "until"):
                raise AttributeError("Invalid Attribute {}".format(k))
        
        opts = '&'.join((
            f"{k}={v}" for k, v in kw.items() if v
        ))

        url = urllib.parse.urljoin(self.urlapi, "commits") + (
            f"?{opts}" if opts else ""
        )

        resp = []

        # ...

        return resp

    def getcommit(self, sha) -> dict:
        url = urllib.parse.urljoin(self.urlapi, f"commits/{sha}")

        # ...
