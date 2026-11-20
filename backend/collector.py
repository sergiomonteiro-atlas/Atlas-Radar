"""
AtlasRadar & AtlasNews Live — Motor de Coleta & Inteligência 24h (v0.2 · Clean Room Atlas-SI)
- Coleta paralela multi-idioma (EN, PT-BR/PT-PT, FR) nas 4 verticais da Atlas
- Coleta em tempo real de Modelos de IA em alta (Hugging Face Trending API)
- Deduplicação, Heat Score (0–99), geolocalização de hubs e exportação para Atlas-Cortex (.md)

Zero dependências externas: Python 3.10+ stdlib puro.
"""

from __future__ import annotations

import concurrent.futures
import email.utils
import hashlib
import html
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CORTEX_EXPORT_DIR = DATA_DIR / "cortex_export"
OUTPUT_FILE = DATA_DIR / "trends_live.json"

USER_AGENT = "AtlasRadar/0.2 (+https://Club.Atlas-SI.com; AtlasNews Live Engine)"
REQUEST_TIMEOUT = 10

HUBS: dict[str, dict[str, Any]] = {
    "san_francisco": {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    "new_york": {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    "london": {"city": "London", "lat": 51.5074, "lon": -0.1278},
    "paris": {"city": "Paris", "lat": 48.8566, "lon": 2.3522},
    "lisbon": {"city": "Lisboa", "lat": 38.7223, "lon": -9.1393},
    "sao_paulo": {"city": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    "tokyo": {"city": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    "seattle": {"city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    "beijing": {"city": "Beijing", "lat": 39.9042, "lon": 116.4074},
    "zurich": {"city": "Zurich", "lat": 47.3769, "lon": 8.5417},
}

# Catálogo multi-idioma (EN, PT, FR) organizado pelas verticais oficiais da Atlas
RSS_SOURCES: list[dict[str, Any]] = [
    # --- IA & AGENTES (EN) ---
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "ai", "lang": "en", "hub": "san_francisco", "weight": 1.25},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "category": "ai", "lang": "en", "hub": "new_york", "weight": 1.22},
    {"name": "OpenAI News", "url": "https://openai.com/news/rss.xml", "category": "ai", "lang": "en", "hub": "san_francisco", "weight": 1.35},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "ai", "lang": "en", "hub": "paris", "weight": 1.25},
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed", "category": "ai", "lang": "en", "hub": "new_york", "weight": 1.20},

    # --- TECH & ENGENHARIA (EN / PT / FR) ---
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "category": "tech", "lang": "en", "hub": "new_york", "weight": 1.10},
    {"name": "Wired AI", "url": "https://www.wired.com/feed/category/ai/latest/rss", "category": "ai", "lang": "en", "hub": "san_francisco", "weight": 1.15},
    {"name": "Tecnoblog (BR)", "url": "https://tecnoblog.net/feed/", "category": "tech", "lang": "pt", "hub": "sao_paulo", "weight": 1.12},
    {"name": "Observador Tech (PT)", "url": "https://observador.pt/seccao/tecnologia/feed/", "category": "tech", "lang": "pt", "hub": "lisbon", "weight": 1.12},
    {"name": "Numerama (FR)", "url": "https://www.numerama.com/feed/", "category": "tech", "lang": "fr", "hub": "paris", "weight": 1.12},
    {"name": "Le Monde Pixels (FR)", "url": "https://www.lemonde.fr/pixels/rss_full.xml", "category": "tech", "lang": "fr", "hub": "paris", "weight": 1.15},

    # --- NEGÓCIOS & GEOPOLÍTICA (EN / PT / FR) ---
    {"name": "TechCrunch Startups", "url": "https://techcrunch.com/category/startups/feed/", "category": "business", "lang": "en", "hub": "san_francisco", "weight": 1.10},
    {"name": "BBC Business", "url": "https://feeds.bbci.co.uk/news/business/rss.xml", "category": "business", "lang": "en", "hub": "london", "weight": 1.08},
    {"name": "InfoMoney (BR)", "url": "https://www.infomoney.com.br/feed/", "category": "business", "lang": "pt", "hub": "sao_paulo", "weight": 1.10},
    {"name": "Euronews PT", "url": "https://pt.euronews.com/rss?format=mrss&level=theme&name=news", "category": "business", "lang": "pt", "hub": "lisbon", "weight": 1.08},
    {"name": "France 24 Éco (FR)", "url": "https://www.france24.com/fr/eco-tech/rss", "category": "business", "lang": "fr", "hub": "paris", "weight": 1.12},

    # --- GAMING (AtlasNews-Gaming) ---
    {"name": "IGN News", "url": "https://feeds.feedburner.com/ign/news", "category": "gaming", "lang": "en", "hub": "san_francisco", "weight": 1.15},
    {"name": "PC Gamer", "url": "https://www.pcgamer.com/rss/", "category": "gaming", "lang": "en", "hub": "london", "weight": 1.10},
    {"name": "Eurogamer", "url": "https://www.eurogamer.net/feed", "category": "gaming", "lang": "en", "hub": "london", "weight": 1.08},
]

HOT_KEYWORDS: dict[str, int] = {
    "agent": 14, "agentic": 15, "hermes": 18, "mcp": 15, "llm": 12,
    "openai": 12, "anthropic": 14, "claude": 14, "gemini": 14, "google": 8,
    "deepseek": 14, "mistral": 14, "qwen": 13, "llama": 12, "nvidia": 11,
    "gpu": 9, "robotics": 10, "automation": 11, "open source": 10, "open-source": 10,
    "gta": 14, "gta vi": 18, "rockstar": 12, "playstation": 9, "nintendo": 9,
    "inteligência artificial": 12, "intelligence artificielle": 12, "ia": 9, "ai": 9,
}

HUB_KEYWORDS: dict[str, list[str]] = {
    "san_francisco": ["openai", "anthropic", "silicon valley", "california", "meta", "nvidia", "y combinator"],
    "seattle": ["microsoft", "amazon", "aws", "copilot"],
    "london": ["deepmind", "uk", "britain", "london", "bbc", "eurogamer"],
    "paris": ["mistral", "hugging face", "france", "paris", "europe", "frança", "union européenne"],
    "lisbon": ["portugal", "lisboa", "lisbon", "porto"],
    "sao_paulo": ["brasil", "brazil", "são paulo", "b3", "ibovespa", "selic", "pix"],
    "tokyo": ["japan", "tokyo", "nintendo", "sony", "playstation", "softbank"],
    "beijing": ["china", "deepseek", "alibaba", "qwen", "bytedance", "tencent", "huawei"],
    "new_york": ["wall street", "nasdaq", "nyse", "new york", "rockstar"],
}


def fetch_url(url: str, accept: str = "*/*") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ssl.create_default_context()) as resp:
        return resp.read()


def clean_text(raw: str | None, max_len: int = 280) -> str:
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[: max_len - 1].rstrip() + "…"
    return text


def parse_date(date_str: str | None) -> datetime:
    now = datetime.now(timezone.utc)
    if not date_str:
        return now
    date_str = date_str.strip()
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return now


def detect_hub(text: str, default_hub: str) -> dict[str, Any]:
    lower = text.lower()
    for hub_key, keywords in HUB_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return HUBS[hub_key]
    return HUBS.get(default_hub, HUBS["san_francisco"])


def compute_heat(title: str, summary: str, age_hours: float, weight: float, extra_points: int = 0) -> int:
    if age_hours <= 1:
        recency = 60.0
    elif age_hours <= 24:
        recency = 60.0 - (age_hours * 1.35)
    elif age_hours <= 72:
        recency = max(8.0, 27.6 - ((age_hours - 24) * 0.4))
    else:
        recency = 5.0

    combined = f"{title} {summary}".lower()
    kw_bonus = 0
    for kw, pts in HOT_KEYWORDS.items():
        if re.search(rf"\b{re.escape(kw)}\b", combined):
            kw_bonus += pts
    kw_bonus = min(kw_bonus, 34)

    raw_score = (recency + kw_bonus + min(extra_points, 20)) * weight
    return max(10, min(99, int(round(raw_score))))


def make_id(url: str, title: str) -> str:
    return hashlib.sha1(f"{url}|{title}".encode("utf-8", errors="ignore")).hexdigest()[:12]


def fetch_rss_source(source: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    now = datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    status = {"source": source["name"], "category": source["category"], "lang": source["lang"], "ok": False, "count": 0, "error": None}
    try:
        raw = fetch_url(source["url"], accept="application/rss+xml, application/xml, text/xml")
        root = ET.fromstring(raw)

        entries = root.findall(".//item")
        is_atom = False
        if not entries:
            entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
            is_atom = True

        for entry in entries[:9]:
            if not is_atom:
                title = clean_text(entry.findtext("title"), 180)
                link = (entry.findtext("link") or "").strip()
                desc = clean_text(entry.findtext("description") or entry.findtext("{http://purl.org/rss/1.0/modules/content/}encoded"), 260)
                pub = entry.findtext("pubDate") or entry.findtext("{http://purl.org/dc/elements/1.1/}date")
            else:
                ns = "{http://www.w3.org/2005/Atom}"
                title = clean_text(entry.findtext(f"{ns}title"), 180)
                link_el = entry.find(f"{ns}link")
                link = link_el.attrib.get("href", "").strip() if link_el is not None else ""
                desc = clean_text(entry.findtext(f"{ns}summary") or entry.findtext(f"{ns}content"), 260)
                pub = entry.findtext(f"{ns}updated") or entry.findtext(f"{ns}published")

            if not title or not link:
                continue

            pub_dt = parse_date(pub)
            age_hours = max(0.05, (now - pub_dt).total_seconds() / 3600.0)
            if age_hours > 168:
                continue

            # Reclassifica para AI se o título/resumo PT/FR falar explicitamente de IA/LLM
            cat = source["category"]
            lower = f"{title} {desc}".lower()
            if cat == "tech" and any(k in lower for k in ["inteligência artificial", "intelligence artificielle", "openai", "claude", "gemini", "chatgpt", "llm", "agentes de ia"]):
                cat = "ai"

            hub = detect_hub(f"{title} {desc}", source["hub"])
            heat = compute_heat(title, desc, age_hours, source["weight"])

            items.append({
                "id": make_id(link, title),
                "title": title,
                "summary": desc or f"Sinal captado via {source['name']}.",
                "url": link,
                "source": source["name"],
                "category": cat,
                "lang": source["lang"],
                "published_at": pub_dt.isoformat(),
                "age_hours": round(age_hours, 2),
                "heat_score": heat,
                "hub": hub,
                "metrics": {},
            })

        status["ok"] = True
        status["count"] = len(items)
    except Exception as exc:
        status["error"] = str(exc)[:120]
    return items, status


def fetch_hacker_news() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    now = datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    status = {"source": "Hacker News", "category": "tech", "lang": "en", "ok": False, "count": 0, "error": None}
    try:
        top_ids = json.loads(fetch_url("https://hacker-news.firebaseio.com/v0/topstories.json"))[:16]

        def _get(item_id: int) -> dict[str, Any] | None:
            try:
                return json.loads(fetch_url(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"))
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            raw_items = [r for r in ex.map(_get, top_ids) if r and r.get("title")]

        for r in raw_items:
            title = clean_text(r.get("title"), 180)
            url = r.get("url") or f"https://news.ycombinator.com/item?id={r['id']}"
            score = int(r.get("score") or 0)
            comments = int(r.get("descendants") or 0)
            pub_dt = datetime.fromtimestamp(int(r.get("time") or time.time()), tz=timezone.utc)
            age_hours = max(0.05, (now - pub_dt).total_seconds() / 3600.0)
            lower = title.lower()
            cat = "ai" if any(k in lower for k in ["ai", "llm", "agent", "gpt", "claude", "gemini", "model", "mcp", "neural"]) else "tech"
            hub = detect_hub(title, "san_francisco")
            heat = compute_heat(title, "", age_hours, 1.15, extra_points=min(20, score // 25))
            items.append({
                "id": make_id(url, title),
                "title": title,
                "summary": f"Trending no Hacker News com {score} pontos e {comments} comentários.",
                "url": url,
                "source": "Hacker News",
                "category": cat,
                "lang": "en",
                "published_at": pub_dt.isoformat(),
                "age_hours": round(age_hours, 2),
                "heat_score": heat,
                "hub": hub,
                "metrics": {"points": score, "comments": comments},
            })
        status["ok"] = True
        status["count"] = len(items)
    except Exception as exc:
        status["error"] = str(exc)[:120]
    return items, status


def fetch_github_trending_ai() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    now = datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    status = {"source": "GitHub Radar", "category": "ai", "lang": "en", "ok": False, "count": 0, "error": None}
    try:
        q = urllib.parse.quote("topic:ai-agents OR topic:llm OR topic:mcp pushed:>2026-01-01")
        url = f"https://api.github.com/search/repositories?q={q}&sort=updated&order=desc&per_page=8"
        data = json.loads(fetch_url(url, accept="application/vnd.github+json"))
        for repo in data.get("items", []):
            full_name = repo.get("full_name", "")
            desc = clean_text(repo.get("description") or "Repositório open-source em destaque no GitHub.", 240)
            stars = int(repo.get("stargazers_count") or 0)
            pushed = parse_date(repo.get("pushed_at"))
            age_hours = max(0.1, (now - pushed).total_seconds() / 3600.0)
            title = f"[GitHub] {full_name} ({stars:,} ★)"
            link = repo.get("html_url", "")
            hub = detect_hub(f"{full_name} {desc}", "san_francisco")
            heat = compute_heat(title, desc, min(age_hours, 18.0), 1.15, extra_points=min(18, stars // 500))
            items.append({
                "id": make_id(link, full_name),
                "title": title,
                "summary": desc,
                "url": link,
                "source": "GitHub Radar",
                "category": "ai",
                "lang": "en",
                "published_at": pushed.isoformat(),
                "age_hours": round(age_hours, 2),
                "heat_score": heat,
                "hub": hub,
                "metrics": {"stars": stars, "language": repo.get("language") or "Multi"},
            })
        status["ok"] = True
        status["count"] = len(items)
    except Exception as exc:
        status["error"] = str(exc)[:120]
    return items, status


def fetch_ai_models_live() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Busca em tempo real os modelos de IA em alta no Hugging Face."""
    models: list[dict[str, Any]] = []
    status = {"source": "HuggingFace Models", "category": "ai", "lang": "en", "ok": False, "count": 0, "error": None}
    try:
        url = "https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=12"
        raw = json.loads(fetch_url(url, accept="application/json"))
        for m in raw[:12]:
            model_id = m.get("id") or m.get("modelId") or ""
            if not model_id:
                continue
            parts = model_id.split("/")
            org = parts[0] if len(parts) > 1 else "Community"
            name = parts[-1]
            models.append({
                "id": model_id,
                "org": org,
                "name": name,
                "pipeline": m.get("pipeline_tag") or "foundation-model",
                "likes": int(m.get("likes") or 0),
                "downloads": int(m.get("downloads") or 0),
                "trending_score": round(float(m.get("trendingScore") or 0), 1),
                "url": f"https://huggingface.co/{model_id}",
            })
        status["ok"] = True
        status["count"] = len(models)
    except Exception as exc:
        status["error"] = str(exc)[:120]
    return models, status


def detect_new_terms(signals: list[dict[str, Any]], ai_models: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Sensor 'Termos Novos Hoje' (inspirado no new-term-radar · MIT):
    Detecta nomes de novos modelos, produtos, versões e termos emergentes de IA
    captados nas últimas 24h no Hugging Face, GitHub e notícias.
    """
    terms: dict[str, dict[str, Any]] = {}

    # 1. Novos modelos em alta no Hugging Face
    for idx, m in enumerate(ai_models[:10]):
        term = m["name"]
        key = term.lower()
        terms[key] = {
            "term": term,
            "kind": "model",
            "source": f"HuggingFace ({m['org']})",
            "score": max(65, 98 - idx * 3),
            "mentions": 1,
            "summary": f"Modelo {m['pipeline']} em alta ({m['likes']:,} likes · {m['downloads']:,} downloads).",
            "url": m["url"],
        }

    # 2. Termos/versões emergentes nos sinais das últimas 24h (ex: GPT-5, Qwen3.8, LTX-2.5, Claude 4, Hermes...)
    pattern = re.compile(
        r"\b((?:GPT|Claude|Gemini|Llama|Qwen|DeepSeek|Mistral|Hermes|Grok|Sora|Veo|LTX|OpenClaw|Flux|Kling|MCP|Agent|Phi|Gemma|Nova|Command|Sonnet|Opus|Haiku|Riemann)[A-Za-z0-9.\-_]{0,18}(?:\s+[0-9]+(?:\.[0-9]+)?[A-Za-z]?)?)\b"
    )
    stop_terms = {"ai", "agent", "agents", "model", "models", "google", "meta", "openai"}

    for s in signals:
        if s.get("age_hours", 99) > 36:
            continue
        found = set(m.group(1).strip() for m in pattern.finditer(s.get("title", "")))
        for raw_t in found:
            clean_t = raw_t.strip(" .-_")
            key = clean_t.lower()
            if len(clean_t) < 3 or key in stop_terms:
                continue
            if key not in terms:
                terms[key] = {
                    "term": clean_t,
                    "kind": "repo" if s.get("source") == "GitHub Radar" else "term",
                    "source": s.get("source", "AtlasRadar"),
                    "score": min(99, int(s.get("heat_score", 70))),
                    "mentions": 1,
                    "summary": s.get("title", ""),
                    "url": s.get("url", ""),
                }
            else:
                terms[key]["mentions"] += 1
                terms[key]["score"] = min(99, terms[key]["score"] + 4)

    ranked = sorted(terms.values(), key=lambda x: (x["score"], x["mentions"]), reverse=True)
    return ranked[:18]


def deduplicate(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        norm_title = re.sub(r"[^a-z0-9]+", "", item["title"].lower())[:60]
        if item["url"] in seen_urls or norm_title in seen_titles:
            continue
        seen_urls.add(item["url"])
        seen_titles.add(norm_title)
        unique.append(item)
    return unique


def collect_all() -> dict[str, Any]:
    started = time.time()
    all_items: list[dict[str, Any]] = []
    sources_status: list[dict[str, Any]] = []
    ai_models: list[dict[str, Any]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as pool:
        rss_futs = [pool.submit(fetch_rss_source, src) for src in RSS_SOURCES]
        hn_fut = pool.submit(fetch_hacker_news)
        gh_fut = pool.submit(fetch_github_trending_ai)
        hf_fut = pool.submit(fetch_ai_models_live)

        for fut in concurrent.futures.as_completed(rss_futs + [hn_fut, gh_fut]):
            items, st = fut.result()
            all_items.extend(items)
            sources_status.append(st)

        ai_models, hf_st = hf_fut.result()
        sources_status.append(hf_st)

    unique_items = deduplicate(all_items)
    unique_items.sort(key=lambda x: (x["heat_score"], -x["age_hours"]), reverse=True)

    counts = {"all": len(unique_items), "ai": 0, "tech": 0, "business": 0, "gaming": 0}
    langs = {"en": 0, "pt": 0, "fr": 0}
    last_24h = 0
    for it in unique_items:
        if it["category"] in counts:
            counts[it["category"]] += 1
        if it.get("lang") in langs:
            langs[it["lang"]] += 1
        if it["age_hours"] <= 24:
            last_24h += 1

    new_terms = detect_new_terms(unique_items, ai_models)

    payload = {
        "meta": {
            "engine": "AtlasRadar v0.3 (Broadcast + AI Models + New Terms · Atlas-SI)",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(time.time() - started, 2),
            "total_signals": len(unique_items),
            "signals_24h": last_24h,
            "sources_ok": sum(1 for s in sources_status if s["ok"]),
            "sources_total": len(sources_status),
            "counts": counts,
            "langs": langs,
            "ai_models_count": len(ai_models),
            "new_terms_count": len(new_terms),
        },
        "sources": sorted(sources_status, key=lambda x: x["source"]),
        "ai_models": ai_models,
        "new_terms": new_terms,
        "signals": unique_items[:160],
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def export_signal_to_cortex(signal: dict[str, Any]) -> Path:
    CORTEX_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", signal["title"]).strip("-").lower()[:55]
    date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{date_prefix}_{signal['category']}_{slug}.md"
    target = CORTEX_EXPORT_DIR / filename

    md = f"""---
type: atlas-radar-signal
id: "{signal['id']}"
category: "{signal['category']}"
lang: "{signal.get('lang', 'en')}"
source: "{signal['source']}"
heat_score: {signal['heat_score']}
hub: "{signal.get('hub', {}).get('city', 'Global')}"
published_at: "{signal['published_at']}"
captured_at: "{datetime.now(timezone.utc).isoformat()}"
url: "{signal['url']}"
tags:
  - atlas-radar
  - atlas-cortex
  - {signal['category']}
---

# {signal['title']}

> **Fonte:** {signal['source']} · **Score de Tendência:** {signal['heat_score']}/99 · **Vertical:** `{signal['category'].upper()}` · **Idioma:** `{signal.get('lang', 'en').upper()}`
> **Link original:** {signal['url']}

## Resumo do Sinal
{signal['summary']}

## Ações Sugeridas (Atlas-Harness / AtlasNews)
- [ ] Avaliar pauta para **AtlasNews** (Carrossel / Vídeo Curto)
- [ ] Gerar tutorial ou análise para membros do **AtlasClub** (`Club.Atlas-SI.com`)
- [ ] Conectar na **Atlas-Cortex Galaxy 3D**
"""
    target.write_text(md, encoding="utf-8")
    return target


if __name__ == "__main__":
    result = collect_all()
    m = result["meta"]
    print(
        f"[AtlasRadar v0.2] Coleta concluída em {m['elapsed_seconds']}s | "
        f"{m['sources_ok']}/{m['sources_total']} fontes OK | "
        f"{m['total_signals']} sinais ({m['signals_24h']} em 24h) | "
        f"Idiomas: {m['langs']} | Modelos IA Live: {m['ai_models_count']}"
    )
