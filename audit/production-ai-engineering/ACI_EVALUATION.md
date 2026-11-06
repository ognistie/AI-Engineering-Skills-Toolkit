# Revisão de Agent-Computer Interface

**Escopo e referência.** [Anthropic: writing effective tools](https://www.anthropic.com/research/writing-tools-for-agents) separa ergonomia do contrato e avaliação com agentes. Aqui, o [linter](../../skills/agent-computer-interface/scripts/check.py) valida uma ferramenta; a [descoberta](../../skills/agent-tool-interface-design/scripts/check.py) limita quais contratos ficam visíveis.

| Controle | Evidência |
| --- | --- |
| A01: seis chamadas | Dois argumentos válidos aceitos. Booleano, enum inválido, campo obrigatório ausente e argumento extra rejeitados. Classificação correta 6/6 neste fixture. |
| A02: nome idêntico, descrição divergente e erro sem ação | `duplicate_tool` e `unactionable_error_contract`. |
| A03: ferramenta pertinente não autorizada | Abstenção; não substitui por ferramenta com intenção diferente. |
| A10/A100/A1000: catálogos progressivos | 3/3 escolhas exatas com intenção previamente rotulada, 50 bytes expostos em cada tamanho. |
| S01: proposta em lote com campo de autorização não previsto | Rejeição anterior a qualquer callback simulado. |

A autorização de efeitos pertence ao executor. O contrato plano não mede payloads reais, nomes semanticamente quase iguais, recuperação após falha, ou efeitos ocultos do host. O teste de duplicação usa colisão literal. Em próximo ensaio, introduza ferramenta indisponível, respostas longas e erros recuperáveis/não recuperáveis com as mesmas tarefas por variante; meça acerto de seleção, taxa de argumentos válidos, recuperação e tokens no trace. Os resultados de tempo e bytes locais estão em [benchmark](BENCHMARK_RESULTS.md).
