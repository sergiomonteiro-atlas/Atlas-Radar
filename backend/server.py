"""
AtlasRadar & AtlasNews Live — Servidor Unificado (HTTP + API REST + MCP JSON-RPC 2.0)
Serve a interface Live em http://localhost:8787, expõe endpoints REST para o dashboard
e fornece um servidor MCP nativo em POST /mcp para o Hermes-Agent e AtlasVoice.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import threading
import time
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

# Permite importar collector e live_tv independentemente do cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import collector  # noqa: E402
import live_tv  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"
HOST = os.environ.get("ATLAS_RADAR_HOST", "127.0.0.1")
PORT = int(os.environ.get("ATLAS_RADAR_PORT", "8787"))
AUTO_REFRESH_SECONDS = int(os.environ.get("ATLAS_RADAR_REFRESH_SEC", "900"))

_LOCK = threading.Lock()
_CACHE: dict[str, Any] = {}


def load_or_collect(force: bool = False) -> dict[str, Any]:
    global _CACHE
    with _LOCK:
        if not force and _CACHE:
            return _CACHE
        if not force and collector.OUTPUT_FILE.exists():
            try:
                _CACHE = json.loads(collector.OUTPUT_FILE.read_text(encoding="utf-8"))
                return _CACHE
            except Exception:
                pass
    fresh = collector.collect_all()
    with _LOCK:
        _CACHE = fresh
    return fresh


def filter_signals(
    payload: dict[str, Any],
    category: str = "all",
    lang: str = "all",
    max_hours: float = 72.0,
    query: str = "",
    limit: int = 120,
) -> list[dict[str, Any]]:
    signals = payload.get("signals", [])
    q = query.strip().lower()
    out: list[dict[str, Any]] = []
    for s in signals:
        if category and category != "all" and s.get("category") != category:
            continue
        if lang and lang != "all" and s.get("lang") != lang:
            continue
        if max_hours > 0 and float(s.get("age_hours", 0)) > max_hours:
            continue
        if q:
            hay = f"{s.get('title', '')} {s.get('summary', '')} {s.get('source', '')}".lower()
            if q not in hay:
                continue
        out.append(s)
        if len(out) >= limit:
            break
    return out


MCP_TOOLS = [
    {
        "name": "atlas_radar_get_trends",
        "description": "Retorna os sinais e tendências em tempo real do AtlasRadar (IA, Tech, Negócios, Gaming) ordenados por Heat Score.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["all", "ai", "tech", "business", "gaming"],
                    "default": "all",
                },
                "max_hours": {"type": "number", "default": 24},
                "limit": {"type": "integer", "default": 15},
            },
        },
    },
    {
        "name": "atlas_radar_search",
        "description": "Pesquisa notícias e tendências específicas no AtlasRadar por palavra-chave.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_hours": {"type": "number", "default": 72},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    },
    {
        "name": "atlas_radar_export_to_cortex",
        "description": "Exporta um sinal do AtlasRadar (pelo ID) como nota Markdown estruturada para o Atlas-Cortex (GBRAIN + Obsidian).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "signal_id": {"type": "string"},
            },
            "required": ["signal_id"],
        },
    },
    {
        "name": "atlas_radar_get_ai_models",
        "description": "Retorna os modelos de IA em alta em tempo real no Hugging Face (trendingScore, downloads, likes, pipeline).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 10},
            },
        },
    },
    {
        "name": "atlas_radar_get_new_terms",
        "description": "Sensor 'Termos Novos Hoje': retorna nomes emergentes de novos modelos, produtos e repos de IA detectados nas últimas 24h.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 15},
            },
        },
    },
]


def handle_mcp_request(body: dict[str, Any]) -> dict[str, Any]:
    req_id = body.get("id")
    method = body.get("method", "")
    params = body.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "atlas-radar-mcp", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            },
        }

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        payload = load_or_collect()

        if name == "atlas_radar_get_trends":
            items = filter_signals(
                payload,
                category=str(args.get("category", "all")),
                max_hours=float(args.get("max_hours", 24)),
                limit=int(args.get("limit", 15)),
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(items, ensure_ascii=False, indent=2)}]
                },
            }

        if name == "atlas_radar_search":
            items = filter_signals(
                payload,
                query=str(args.get("query", "")),
                max_hours=float(args.get("max_hours", 72)),
                limit=int(args.get("limit", 10)),
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(items, ensure_ascii=False, indent=2)}]
                },
            }

        if name == "atlas_radar_export_to_cortex":
            sig_id = str(args.get("signal_id", ""))
            sig = next((s for s in payload.get("signals", []) if s["id"] == sig_id), None)
            if not sig:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Sinal não encontrado: {sig_id}"},
                }
            saved_path = collector.export_signal_to_cortex(sig)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                {"status": "exported", "path": str(saved_path), "title": sig["title"]},
                                ensure_ascii=False,
                            ),
                        }
                    ]
                },
            }

        if name == "atlas_radar_get_ai_models":
            lim = int(args.get("limit", 10))
            models = payload.get("ai_models", [])[:lim]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(models, ensure_ascii=False, indent=2)}]
                },
            }

        if name == "atlas_radar_get_new_terms":
            lim = int(args.get("limit", 15))
            terms = payload.get("new_terms", [])[:lim]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(terms, ensure_ascii=False, indent=2)}]
                },
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Tool desconhecida: {name}"},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Método MCP não suportado: {method}"},
    }


class AtlasRadarHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        # Log limpo no terminal
        sys.stdout.write(f"[AtlasRadar HTTP] {self.address_string()} - {format % args}\n")

    def _send_json(self, data: Any, status: int = HTTPStatus.OK) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/api/health":
            payload = load_or_collect()
            self._send_json({"status": "online", "meta": payload.get("meta", {})})
            return

        if path == "/api/tv":
            force = (qs.get("refresh") or ["0"])[0] == "1"
            channels = live_tv.resolve_live_channels(force=force)
            self._send_json({"channels": channels})
            return

        if path == "/api/trends":
            payload = load_or_collect()
            category = (qs.get("category") or ["all"])[0]
            lang = (qs.get("lang") or ["all"])[0]
            max_hours = float((qs.get("hours") or ["72"])[0])
            query = (qs.get("q") or [""])[0]
            limit = int((qs.get("limit") or ["140"])[0])
            filtered = filter_signals(payload, category=category, lang=lang, max_hours=max_hours, query=query, limit=limit)
            self._send_json(
                {
                    "meta": payload.get("meta", {}),
                    "sources": payload.get("sources", []),
                    "ai_models": payload.get("ai_models", []),
                    "new_terms": payload.get("new_terms", []),
                    "signals": filtered,
                }
            )
            return

        # Arquivos estáticos em web/
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        target = (WEB_DIR / rel).resolve()
        if not str(target).startswith(str(WEB_DIR.resolve())) or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        mime, _ = mimetypes.guess_type(str(target))
        content = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{mime or 'application/octet-stream'}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/refresh":
            payload = load_or_collect(force=True)
            self._send_json({"status": "refreshed", "meta": payload.get("meta", {}), "signals": payload.get("signals", [])})
            return

        if path == "/api/export-cortex":
            body = self._read_json_body()
            sig_id = str(body.get("id", ""))
            payload = load_or_collect()
            sig = next((s for s in payload.get("signals", []) if s["id"] == sig_id), None)
            if not sig:
                self._send_json({"error": "Sinal não encontrado"}, status=HTTPStatus.NOT_FOUND)
                return
            saved = collector.export_signal_to_cortex(sig)
            self._send_json({"status": "exported", "file": saved.name, "path": str(saved)})
            return

        if path == "/mcp":
            try:
                body = self._read_json_body()
                resp = handle_mcp_request(body)
                self._send_json(resp)
            except Exception as exc:
                self._send_json(
                    {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}},
                    status=HTTPStatus.BAD_REQUEST,
                )
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")


def _auto_refresh_loop() -> None:
    while True:
        time.sleep(AUTO_REFRESH_SECONDS)
        try:
            print("[AtlasRadar] Atualização automática em background...")
            load_or_collect(force=True)
        except Exception as exc:
            print(f"[AtlasRadar] Erro no auto-refresh: {exc}")


def main() -> None:
    print("[AtlasRadar] Inicializando base de sinais ao vivo...")
    load_or_collect(force=not collector.OUTPUT_FILE.exists())

    t = threading.Thread(target=_auto_refresh_loop, daemon=True)
    t.start()

    server = ThreadingHTTPServer((HOST, PORT), AtlasRadarHandler)
    print(f"[AtlasRadar & AtlasNews Live] Online em: http://{HOST}:{PORT}")
    print(f"[AtlasRadar MCP Endpoint]     POST       http://{HOST}:{PORT}/mcp")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[AtlasRadar] Encerrando servidor...")
        server.server_close()


if __name__ == "__main__":
    main()
