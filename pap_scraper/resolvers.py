"""
Custom DNS resolver for pap_scraper.
Directly maps pap.pl and www.pap.pl to origin server IP 193.200.216.72
to bypass Imperva Incapsula WAF/CDN.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from twisted.internet import defer
from scrapy.resolver import CachingThreadedResolver

if TYPE_CHECKING:
    from collections.abc import Sequence
    from twisted.internet.defer import Deferred

ORIGIN_IP = "193.200.216.72"
PAP_HOSTS = frozenset({"www.pap.pl", "pap.pl"})


class PapOriginResolver(CachingThreadedResolver):
    """
    Custom DNS resolver for Scrapy that routes www.pap.pl and pap.pl
    directly to the PAP origin server IP (193.200.216.72), bypassing
    the Imperva Incapsula CDN and anti-bot challenge page.

    Other hostnames fall back to default CachingThreadedResolver behavior.
    """

    def getHostByName(
        self, name: str | bytes, timeout: Sequence[int] = ()
    ) -> Deferred[str]:
        clean_name = name.decode("idna") if isinstance(name, bytes) else str(name)
        clean_host = clean_name.lower().rstrip(".")
        if clean_host in PAP_HOSTS:
            return defer.succeed(ORIGIN_IP)
        return super().getHostByName(clean_name, timeout)
