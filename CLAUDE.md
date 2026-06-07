# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

This is an empty research workspace ("chaos research works"). There is no source code, build system, test suite, or version control here yet. The only file present is `.mcp.json`.

As code is added, update this file with the real build/lint/test commands and an architecture overview. Until then, the notes below are all that apply.

## MCP servers

`.mcp.json` configures one project-scoped MCP server:

- **mem0** — a memory server run via `D:/ai-stack/mem0-venv/Scripts/python.exe` executing `D:/ai-stack/mcp/mem0_mcp_server.py`. It exposes `mem0_add`, `mem0_search`, `mem0_list`, `mem0_delete`, and `mem0_project` tools for storing and recalling persistent memories. The server lives outside this directory; changes to its behavior happen in `D:/ai-stack/`, not here.

## Notes

- Git repository initialized; default branch is `master`. No commits yet.
