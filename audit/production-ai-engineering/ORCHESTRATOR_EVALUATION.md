# Avaliação do orquestrador

Reproduza com [run_audit.py](run_audit.py). Os 81 casos novos em [fixtures](fixtures/) foram construídos e rotulados antes de executar o roteador. O arquivo de resultados guarda o SHA-256 da concatenação dos shards na ordem dos nomes. Foram cobertos desenvolvimento, debugging, ACI, harness, contexto, inferência, avaliação, durabilidade, segurança, composições, ambiguidade, disponibilidade, orçamento, falta de autorização e abstenção. Os rótulos foram predefinidos pelo auditor sem olhar as previsões; não houve segundo avaliador independente desta amostra.

| Métrica estruturada | Resultado |
| --- | --- |
| Seleção em ordem | 81/81 |
| Precisão e recall macro @3 | 1,00 / 1,00 |
| Omissões e seleções desnecessárias | 0 / 0 |
| Restrições e política esperadas, onde aplicável | 65/66 |
| Justificativa estrutural | 81/81 |
| Ativação nativa a partir de texto livre | N/V |

**audit-079:** uma invocação explícita pede análise de inferência sem configuração. Seleção `inference-serving-architect` em modo `plan` é correta, mas `host_may_dispatch_within_scope` mistura carregar uma skill de planejamento com autorizar execução. O caminho no [roteador](../../skills/skill-orchestrator/scripts/route.py#L137) permite a modalidade explícita mesmo quando `dispatchable` é falso. O teste não executou ação. Separe `may_load_skill` e `may_execute` no contrato e teste ambos com insumos faltantes.

Os 100 casos anteriores também passaram (64 + 36). A avaliação nova é condicional às classificações fornecidas. Ela não prova que um modelo descobre a intenção, escolhe a skill nativamente ou é eficiente em contexto. Próximo teste: classificador/host em sessões limpas, rótulos cegos e ferramentas observadas no trace.
