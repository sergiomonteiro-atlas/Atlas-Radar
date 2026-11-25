"""
AtlasRadar — Curadoria Contínua para AtlasClub (`club.atlashub.si`) & Discord
Transforma os sinais 24h, Termos Novos Hoje e Modelos de IA em:
1. Post diário pronto em Markdown para as comunidades Free (Genesis PT / France FR) do AtlasClub
2. Payload de Embed para Discord Webhook (alertas automáticos)
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone
from typing import Any


def _select_top_signals(payload: dict[str, Any], lang: str = "pt", limit: int = 4) -> list[dict[str, Any]]:
    signals = payload.get("signals", [])
    # Prioriza sinais no idioma pedido quando houver, completando com sinais globais de alto heat_score
    preferred = [s for s in signals if s.get("lang") == lang and s.get("age_hours", 99) <= 48]
    global_hot = [s for s in signals if s.get("lang") != lang and s.get("age_hours", 99) <= 36]
    combined: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for s in preferred[:2] + global_hot + preferred[2:]:
        if s["id"] not in seen_ids:
            seen_ids.add(s["id"])
            combined.append(s)
        if len(combined) >= limit:
            break
    return combined


def build_club_digest(payload: dict[str, Any], lang: str = "pt", limit: int = 4) -> str:
    """Gera o post diário curado para o AtlasClub (PT ou FR)."""
    today = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    top = _select_top_signals(payload, lang=lang, limit=limit)
    terms = payload.get("new_terms", [])[:5]
    models = payload.get("ai_models", [])[:3]

    if lang == "fr":
        lines = [
            f"# 📡 Radar Quotidien AtlasClub France — {today}",
            "",
            "Voici les **signaux majeurs des dernières 24h** sélectionnés par **AtlasRadar** (`radar.atlashub.si`) :",
            "",
            "## 🔥 À la une aujourd'hui",
        ]
        for idx, s in enumerate(top, start=1):
            lines.append(f"{idx}. **[{s['title']}]({s['url']})** *(Score {s['heat_score']}/99 · {s['source']})*")
            lines.append(f"   > {s['summary']}")
        if terms:
            lines += ["", "## 🆕 Termes & Modèles émergents"]
            lines.append(", ".join(f"`{t['term']}`" for t in terms))
        if models:
            lines += ["", "## 🤖 Modèles IA en tendance (Hugging Face)"]
            for m in models:
                lines.append(f"- **{m['id']}** ({m['pipeline']}) — {m['likes']} likes")
        lines += [
            "",
            "---",
            "💬 **Question du jour :** Lequel de ces outils ou modèles souhaitez-vous voir décortiqué dans notre prochain atelier sur **club.atlashub.si** ?",
        ]
        return "\n".join(lines)

    # Padrão PT (Genesis PT)
    lines = [
        f"# 📡 Curadoria Diária AtlasClub Genesis — {today}",
        "",
        "Estes são os **principais sinais das últimas 24h** captados pelo **AtlasRadar** (`radar.atlashub.si`):",
        "",
        "## 🔥 Destaques de Hoje",
    ]
    for idx, s in enumerate(top, start=1):
        lines.append(f"{idx}. **[{s['title']}]({s['url']})** *(Score {s['heat_score']}/99 · {s['source']})*")
        lines.append(f"   > {s['summary']}")
    if terms:
        lines += ["", "## 🆕 Termos & Lançamentos Emergentes"]
        lines.append(", ".join(f"`{t['term']}`" for t in terms))
    if models:
        lines += ["", "## 🤖 Modelos de IA em Alta (Hugging Face)"]
        for m in models:
            lines.append(f"- **{m['id']}** ({m['pipeline']}) — {m['likes']} likes")
    lines += [
        "",
        "---",
        "💬 **Pergunta de debate:** Qual desses avanços você gostaria de ver transformado em workflow prático no **Atlas-Harness** dentro do **club.atlashub.si**?",
    ]
    return "\n".join(lines)


def build_discord_payload(payload: dict[str, Any], lang: str = "pt", limit: int = 4) -> dict[str, Any]:
    """Monta o JSON de Embed para Discord Webhook."""
    top = _select_top_signals(payload, lang=lang, limit=limit)
    terms = payload.get("new_terms", [])[:5]
    today = datetime.now(timezone.utc).strftime("%d/%m/%Y")

    fields = [
        {
            "name": f"#{i + 1} [{s['category'].upper()}] Score {s['heat_score']}/99 · {s['source']}",
            "value": f"[{s['title']}]({s['url']})",
            "inline": False,
        }
        for i, s in enumerate(top)
    ]
    if terms:
        fields.append(
            {
                "name": "🔥 Termos Novos Hoje",
                "value": " · ".join(f"`{t['term']}`" for t in terms),
                "inline": False,
            }
        )

    title = (
        f"📡 AtlasRadar France · Top Sinais ({today})"
        if lang == "fr"
        else f"📡 AtlasRadar Genesis · Top Sinais ({today})"
    )
    return {
        "username": "AtlasRadar // AtlasNews Live",
        "content": "Debate completo e tutoriais em **https://club.atlashub.si** · Radar ao vivo: **https://radar.atlashub.si**",
        "embeds": [
            {
                "title": title,
                "color": 39423,  # #0099ff Atlas Electric Blue
                "fields": fields,
                "footer": {"text": "AtlasHub.SI · Curadoria Automática 24h"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ],
    }


def send_to_discord(
    payload: dict[str, Any],
    webhook_url: str | None = None,
    lang: str = "pt",
    limit: int = 4,
    dry_run: bool = False,
) -> dict[str, Any]:
    target = (webhook_url or os.environ.get("DISCORD_WEBHOOK_URL", "")).strip()
    discord_body = build_discord_payload(payload, lang=lang, limit=limit)
    if dry_run or not target:
        return {
            "sent": False,
            "dry_run": True,
            "reason": "no_discord_webhook_url_configured" if not target else "dry_run",
            "discord_payload": discord_body,
        }
    req = urllib.request.Request(
        target,
        data=json.dumps(discord_body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "AtlasRadar/0.3"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10, context=ssl.create_default_context()) as resp:
        return {"sent": 200 <= resp.status < 300, "status_code": resp.status, "dry_run": False}
