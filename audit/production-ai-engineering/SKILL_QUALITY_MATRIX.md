# Matriz de qualidade por skill

Escala: 0 ausente, 1 conceitual, 2 parcial, 3 funcional em casos limitados, 4 robusta no escopo medido, 5 validada amplamente. **N/V** = evidência insuficiente. Colunas: fidelidade científica **F** 15%, operação **O** 20%, qualidade funcional **Q** 20%, robustez **R** 15%, integração **I** 10%, generalização **G** 10%, eficiência **E** 5%, documentação **D** 5%. **Sem nota ponderada**: generalização e outras dimensões essenciais não foram medidas. As classificações tratam de escopo local, sem promoção a produção.

| Skill | Estado verificável | F | O | Q | R | I | G | E | D | Evidência ou restrição |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| agent-first-harness | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | H01: repositório novo e recibo de outra revisão; sem CI real. |
| agent-computer-interface | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | A01/A02: 6 argumentos e contrato ambíguo; recuperação por modelo N/V. |
| repository-context-architecture | PARTIALLY IMPLEMENTED | 3 | 3 | 3 | 2 | N/V | N/V | N/V | 3 | H02/H03: link comum detectado, link com título perdido. |
| kv-cache-aware-context | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | C01: prefixo local; provedor e custo N/V. |
| context-compaction-recovery | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | C02: perda de escopo, erro e artefato; retomada do agente N/V. |
| inference-serving-architect | FUNCTIONALLY VERIFIED, só estimador | 3 | 2 | 3 | 3 | N/V | N/V | N/V | 3 | I01: pressão de memória modelada; nenhuma GPU. |
| agent-evals-engineer | PARTIALLY IMPLEMENTED | 3 | 3 | 2 | 2 | N/V | N/V | N/V | 3 | E01/E02 corretos; E03 aceita reutilização de evidência. |
| trajectory-review-engine | PARTIALLY IMPLEMENTED | 3 | 3 | 3 | 2 | 3 | N/V | N/V | 3 | T01/T02: integração existente com spans; falha intercalada. |
| evaluator-optimizer-loop | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | E04: preserva melhor artefato verificado e respeita orçamento. |
| durable-execution-engine | FUNCTIONALLY VERIFIED, um operador | 3 | 3 | 3 | 2 | 3 | N/V | N/V | 3 | D01: recuperação; D02: corrida fora do escopo. |
| brain-tool-runtime-separation | FUNCTIONALLY VERIFIED, demo | 3 | 3 | 3 | 3 | 3 | N/V | N/V | 3 | S01 e teste de composição local; host credenciado N/V. |
| agent-tool-interface-design | FUNCTIONALLY VERIFIED | 3 | 3 | 3 | 3 | N/V | N/V | 3 | 3 | Catálogos 10/100/1000; bytes e latência locais. |
| capability-security-architect | FUNCTIONALLY VERIFIED, descritores | 3 | 3 | 3 | 3 | N/V | N/V | N/V | 3 | S02: validade e atenuação; emissão de credenciais N/V. |
| prompt-injection-boundaries | PARTIALLY IMPLEMENTED | 2 | 2 | 2 | 2 | 2 | N/V | N/V | 3 | S03/S04 passam; S05 omite origem privada e recebe `allow`. |
| runtime-verification-engine | FUNCTIONALLY VERIFIED, replay | 3 | 3 | 3 | 3 | 3 | N/V | N/V | 3 | S06/S07 e composição local; enforcement credenciado N/V. |

Os IDs apontam para [resultados brutos](evidence/independent-results.json). As linhas baseiam-se em evidência local nova e na regressão existente, não em produtividade atribuída à skill.
