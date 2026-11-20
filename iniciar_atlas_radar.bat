@echo off
title AtlasRadar // AtlasNews Live
cd /d "%~dp0"
echo ========================================================
echo   ATLAS RADAR // ATLASNEWS LIVE (MVP v0.1 · Atlas-SI)
echo   Interface: http://localhost:8787
echo   MCP API:   POST http://localhost:8787/mcp
echo ========================================================
start "" http://localhost:8787
python backend\server.py
pause
