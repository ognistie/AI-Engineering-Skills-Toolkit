# Compatibilidade

| Superfície | Formato | Descoberta | Ferramentas e segurança |
| --- | --- | --- | --- |
| Codex | Pasta Agent Skills; UI opcional em `agents/openai.yaml` | `~/.agents/skills`, `.agents/skills` no projeto ou destino do perfil. Invocação com `$nome`. | A política do Codex continua valendo. |
| Claude Code | Mesma pasta portátil | `~/.claude/skills` ou `.claude/skills` no projeto. Invocação com `/nome`. | Ferramentas, trust e permissões pertencem ao Claude Code. |
| Generic Agent Skills | ZIP por skill ou pasta | O consumidor precisa importar e disponibilizar o recurso. | Nenhum mecanismo comum de execução, segurança ou seleção é assumido. |

Fontes: [Codex Skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code Skills](https://code.claude.com/docs/en/skills) e [Agent Skills](https://agentskills.io/specification).

O CLI Python funciona sem dependências extras. Windows PowerShell e shell POSIX só encaminham os argumentos. Testes com destinos temporários comprovam instalação no filesystem; descoberta no app, políticas do host e desempenho em modelos são níveis separados. As métricas de avaliação exigem observações do host.
