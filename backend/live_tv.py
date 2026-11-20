"""
AtlasRadar — Resolvedor Dinâmico de Canais Live TV (YouTube Live 24h)
Verifica em paralelo quais canais PT / FR / EN estão realmente AO VIVO e
com embed habilitado (playableInEmbed), retornando o videoId exato da live ativa.
"""

from __future__ import annotations

import concurrent.futures
import re
import ssl
import time
import urllib.request
from typing import Any

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

TV_CATALOG: list[dict[str, str]] = [
    # PT (Brasil & Portugal)
    {"id": "cnn_br", "name": "CNN Brasil", "lang": "PT", "handle": "@CNNbrasil"},
    {"id": "jp_br", "name": "Jovem Pan News", "lang": "PT", "handle": "@jovempannews"},
    {"id": "record_br", "name": "Record News", "lang": "PT", "handle": "@RecordNews"},
    {"id": "band_br", "name": "Band Jornalismo", "lang": "PT", "handle": "@BandJornalismo"},
    {"id": "sbt_br", "name": "SBT News", "lang": "PT", "handle": "@SBTNews"},
    {"id": "euronews_pt", "name": "Euronews PT", "lang": "PT", "handle": "@euronewspt"},
    # FR (França & Europa Francófona)
    {"id": "france24_fr", "name": "France 24", "lang": "FR", "handle": "@FRANCE24"},
    {"id": "euronews_fr", "name": "Euronews FR", "lang": "FR", "handle": "@euronewsfr"},
    {"id": "bfmtv_fr", "name": "BFMTV", "lang": "FR", "handle": "@BFMTV"},
    # EN (Global / Business / Tech)
    {"id": "sky_en", "name": "Sky News", "lang": "EN", "handle": "@SkyNews"},
    {"id": "dw_en", "name": "DW News", "lang": "EN", "handle": "@DWNews"},
    {"id": "aj_en", "name": "Al Jazeera", "lang": "EN", "handle": "@aljazeeraenglish"},
    {"id": "france24_en", "name": "France 24 EN", "lang": "EN", "handle": "@FRANCE24English"},
    {"id": "euronews_en", "name": "Euronews EN", "lang": "EN", "handle": "@euronews"},
    {"id": "bloomberg_en", "name": "Bloomberg", "lang": "EN", "handle": "@markets"},
]

_CACHE_TTL = 600  # 10 min
_CACHE_AT = 0.0
_CACHE_DATA: list[dict[str, Any]] = []


def _check_channel(ch: dict[str, str]) -> dict[str, Any]:
    url = f"https://www.youtube.com/{ch['handle']}/live"
    out: dict[str, Any] = {
        "id": ch["id"],
        "name": ch["name"],
        "lang": ch["lang"],
        "handle": ch["handle"],
        "live_url": url,
        "video_id": None,
        "embed_url": None,
        "online": False,
        "embeddable": False,
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
        with urllib.request.urlopen(req, timeout=7, context=ssl.create_default_context()) as resp:
            body = resp.read().decode("utf-8", errors="ignore")

        is_live = '"isLiveNow":true' in body or '"isLive":true' in body
        embeddable = '"playableInEmbed":true' in body
        vid_match = re.search(r'"canonicalUrl":"https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})"', body)
        if not vid_match:
            vid_match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', body)

        if vid_match and is_live:
            vid = vid_match.group(1)
            out["video_id"] = vid
            out["online"] = True
            out["embeddable"] = embeddable
            if embeddable:
                out["embed_url"] = f"https://www.youtube.com/embed/{vid}?autoplay=0&mute=1&rel=0"
    except Exception:
        pass
    return out


def resolve_live_channels(force: bool = False) -> list[dict[str, Any]]:
    global _CACHE_AT, _CACHE_DATA
    now = time.time()
    if not force and _CACHE_DATA and (now - _CACHE_AT) < _CACHE_TTL:
        return _CACHE_DATA

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(_check_channel, TV_CATALOG))

    # Ordena: primeiro os online+embeddable, depois os online sem embed
    results.sort(key=lambda c: (not (c["online"] and c["embeddable"]), not c["online"], c["lang"], c["name"]))
    _CACHE_DATA = results
    _CACHE_AT = now
    return results


if __name__ == "__main__":
    channels = resolve_live_channels(force=True)
    ok = [c for c in channels if c["online"] and c["embeddable"]]
    print(f"Canais AO VIVO + EMBEDDABLE: {len(ok)}/{len(channels)}")
    for c in channels:
        flag = "OK-EMBED" if (c["online"] and c["embeddable"]) else ("LIVE-ONLY" if c["online"] else "OFFLINE")
        print(f"  [{flag:9}] [{c['lang']}] {c['name']:16} | vid={c['video_id']}")
