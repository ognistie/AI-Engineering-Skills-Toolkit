# Advanced AI Engineering Skills (AAES)

Catálogo independente de **13 Agent Skills** para desenvolver, investigar e avaliar sistemas de IA. Versão 0.1.0. O pacote funciona offline para planejamento, análise de artefatos e verificações locais.

| Grupo | Skill | Entrega |
| --- | --- | --- |
| Roteamento | `skill-orchestrator` | Composição mínima por objetivo, risco e custo, com abstenção. |
| Essenciais | `research-orchestrator` | Síntese de evidências primárias ou plano offline. |
| Essenciais | `process-verifier` | Gates de aceitação conferidos por evidência independente. |
| Essenciais | `trajectory-analyzer` | Cronologia, operações repetidas e latência de traces. |
| Essenciais | `experiment-evaluator` | Comparação pareada com orçamento e critérios congelados. |
| Autonomia | `adaptive-reasoning` | Decide entre tentativa direta, verificação, escalada e parada. |
| Autonomia | `long-horizon-executor` | Checkpoints locais, idempotência e reconciliação de interrupções. |
| Autonomia | `multi-agent-router` | Batches que respeitam dependências, conflitos e autoridade. |
| Autonomia | `runtime-guardian` | Política de ação e reserva atômica em um executor confiável. |
| Pesquisa | `evolutionary-optimizer` | Arquivo de variantes viáveis no Pareto, sem contaminar o holdout. |
| Pesquisa | `hypothesis-lab` | Hipóteses falsificáveis e matriz de evidências independentes. |
| Pesquisa | `mechanistic-interpretability` | Protocolo de intervenções neurais e medidas pareadas de patching. |
| Pesquisa | `agentic-rl-lab` | Contrato de ambiente, validação de rollouts e retornos descontados. |

## Instalação local

Requer Python 3.12+. Instalador e helpers usam apenas a biblioteca padrão. Para os wrappers, defina `AAES_PYTHON` com o caminho completo se o alias `python` não resolver.

```text
python scripts/manage.py list
python scripts/manage.py install --target codex
python scripts/manage.py install --target claude --group essential
python scripts/manage.py install --target codex --skill skill-orchestrator
python scripts/manage.py verify --target codex
python scripts/manage.py update --target codex --skill process-verifier
python scripts/manage.py remove --target codex --skill trajectory-analyzer
python scripts/manage.py export
```

Sem seleção, o comando opera no catálogo inteiro. Repita `--skill` para selecionar várias skills. Grupos: `routing`, `essential`, `autonomy`, `advanced`. Use `--destination` para um caminho de descoberta específico ou um destino isolado. O padrão Codex é `~/.agents/skills`; perfis que usam `~/.codex/skills` podem indicar esse caminho explicitamente. O padrão Claude Code é `~/.claude/skills` (ou `CLAUDE_CONFIG_DIR/skills`). PowerShell: `./scripts/manage.ps1`. Bash/POSIX: `sh scripts/manage.sh`.

No Codex, experimente `$skill-orchestrator Só recomende skills para investigar este trace`. No Claude Code, use `/skill-orchestrator`. A instalação individual do orquestrador inclui o catálogo; para despacho, o host precisa disponibilizar a skill recomendada. Para outros agentes, use as pastas ou os ZIPs exportados.

## Validação e limites

```text
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python evals/score_routing.py
python -m unittest discover -s tests -v
```

[Arquitetura](docs/ARCHITECTURE.md) · [Compatibilidade](docs/COMPATIBILITY.md) · [Segurança](docs/SECURITY.md) · [Relatório](evals/reports/release.md) · [Melhorias](docs/REVIEW.md)

A instalação não exige APIs, pesos, GPU, banco externo ou um framework de agentes. Patching real, treinamento e ações externas dependem de ferramentas, isolamento e permissões do host. Uma skill ou decisão de preflight não é barreira de segurança. O piloto comportamental não estabelece ganho geral de eficácia. Nenhum código do AIWorkbench foi copiado; nenhuma licença de redistribuição foi declarada.
