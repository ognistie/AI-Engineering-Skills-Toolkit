# Dez melhorias priorizadas

Esforço relativo: P = pequeno, M = médio, G = grande. Benefícios são esperados, sem projeção quantitativa.

| Prioridade | Problema, evidência e causa | Alteração e arquivos | Esforço / benefício / risco | Aceitação |
| --- | --- | --- | --- | --- |
| P0 | S05: origem privada omitida porque é auto declarada | `prompt-injection-boundaries/scripts/check.py` e contrato do executor: vincular linhagem e payload imutáveis | M / bloqueia omissão / adaptação do host | Omissão, replay e declassificação implícita não disparam exportação; público legítimo passa. |
| P0 | E03: referência reutilizada não é ligada ao trial | `agent-evals-engineer/scripts/check.py`: protocolo de trials prévio e estado final assinado pelo coletor | M / evita falso sucesso / migração de evidência | Duplicata, trial desconhecido e evidência editada ficam inválidos; E01 não muda. |
| P1 | audit-079: invocação explícita salta gate | `skill-orchestrator/scripts/route.py` e schema: separar carregamento e execução | P / decisões sem ambiguidade / consumidores antigos | Caso 079 não despacha; plano continua disponível; execução válida passa. |
| P1 | D02: ausência observada enquanto o proprietário age | `durable-execution-engine/scripts/demo.py` e journal: lock/lease e fencing, ou recusa concorrência | M / estado recuperável / lock órfão | Barreira concorrente e crash nas duas janelas, sem falso no-effect. |
| P1 | T02: sucesso alheio reseta janela | `trajectory-review-engine/scripts/check.py`: janela por operação e estado | P / menor perda de detecção / falsos positivos | Três timeouts intercalados detectados e progresso real não sinalizado. |
| P1 | Replay local ainda não prova gate do host | `brain-tool-runtime-separation`, `runtime-verification-engine` e adaptador alvo: gate obrigatório por ação | G / efeito vinculado ao estado / integração com concorrência | Transição inválida ou proposta fora do escopo gera zero chamadas credenciadas em sandbox. |
| P2 | H03: parser perde link com título | `repository-context-architecture/scripts/check.py`: ampliar parser ou evidenciar sintaxe não coberta | P / menos falsos negativos / dependência se usar biblioteca | Corpus inclui títulos, âncoras e fences sem marcar links válidos. |
| P2 | ACI só mede schemas locais e seleção por tag | `agent-computer-interface`, `agent-tool-interface-design` e novos fixtures de host | M / escolha e recuperação mensuráveis / viés do dataset | Comparar A/B/C com ferramentas semelhantes, falhas e respostas longas; observar traces. |
| P2 | Cache e GPU têm apenas proxies e estimativas | `kv-cache-aware-context`, `inference-serving-architect` e adaptadores de telemetria | G / capacidade e custo observáveis / custo e hardware | Benchmark autorizado com cache cold/warm, TTFT, vazão, memória e cobrança, com qualidade pareada. |
| P3 | Eficácia geral e generalização N/V | `evals/`: suíte cega de tarefas inéditas, braços A/B/C/D | G / evidência de produtividade / contaminação | Revisões fixas, repetições, verificadores independentes e métricas com incerteza por tarefa. |

As correções foram recomendadas, não aplicadas. Preserve o contrato de portabilidade e reexecute estes controles depois de cada mudança.
