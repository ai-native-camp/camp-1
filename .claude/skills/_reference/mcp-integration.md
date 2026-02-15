# MCP Integration Reference (from plugin-dev)

> Source: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/mcp-integration/SKILL.md

## MCP Server Configuration Methods

### Method 1: .mcp.json (Recommended)
```json
{
  "server-name": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-name"],
    "env": { "API_KEY": "${API_KEY}" }
  }
}
```

### Method 2: plugin.json inline
```json
{
  "mcpServers": {
    "server-name": { "command": "...", "args": ["..."] }
  }
}
```

## MCP Server Types

| Type | Transport | Best For | Auth |
|------|-----------|----------|------|
| stdio | Process | Local tools, custom servers | Env vars |
| SSE | HTTP | Hosted services, cloud APIs | OAuth |
| HTTP | REST | API backends, token auth | Tokens |
| ws | WebSocket | Real-time, streaming | Tokens |

### stdio (가장 일반적)
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
    "env": { "LOG_LEVEL": "debug" }
  }
}
```

### SSE (클라우드 서비스)
```json
{
  "asana": {
    "type": "sse",
    "url": "https://mcp.asana.com/sse"
  }
}
```

## Environment Variable Expansion
- `${CLAUDE_PLUGIN_ROOT}` - 플러그인 디렉토리 (이식성 위해 항상 사용)
- `${MY_API_KEY}` - 사용자 shell 환경변수

## MCP Tool Naming
Format: `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`

## 설치 방법
1. .mcp.json 생성
2. `/mcp` 명령으로 서버 확인
3. 도구 호출 테스트

## 디버깅
- `claude --debug` 로그 확인
- `/mcp` 명령으로 연결 상태 확인
- 환경변수 설정 확인

## Official Resources
- MCP Docs: https://modelcontextprotocol.io/
- Claude Code MCP Docs: https://docs.claude.com/en/docs/claude-code/mcp
- MCP Servers README: https://github.com/modelcontextprotocol/servers/blob/main/README.md
