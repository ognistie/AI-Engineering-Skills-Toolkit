# Auditoria independente — Production AI Engineering

Este é o registro **antes da correção**. Veja a [revalidação](REMEDIATION.md) e os resultados comparativos.

**Base:** checkout local AAES, HEAD `3b4b938` com a expansão não publicada. O [resultado bruto](evidence/independent-results.json) guarda hashes dos arquivos realmente auditados. O escopo é o das 15 skills novas e suas fronteiras com as 13 anteriores. Não foi alterado código de skills.

## Veredito

As 15 têm mecanismos executáveis. Os testes originais passaram (55 testes, 100 casos estruturados, 28 instalações e ZIPs em dois wrappers Windows). A auditoria nova teve **23/28** verificações funcionais conformes; cinco resultados divergem das expectativas, incluindo limites deliberadamente testados fora do escopo documentado. A seleção estrutural concordou em **81/81** novos casos; **65/66** verificações aplicáveis de política passaram. Nenhum desses números mede seleção nativa, eficácia de um modelo ou segurança de produção.

- **Funciona:** validar argumentos locais, verificar estado compactado, comparar prefixos serializados, estimar memória KV, calcular pass@k/pass^k com evidência bem formada e reconciliar um efeito simulado em operador único. Os casos de controle e seus resultados estão no [artefato executável](functional.py).
- **Bloqueios para uso privilegiado:** [S05](ROOT_CAUSE_ANALYSIS.md) mostra que uma proposta que omite uma origem privada pode receber `allow`; não há execução real nessa demonstração. A seleção explícita do orquestrador sinaliza despacho com insumo faltante. Conectar essas saídas diretamente a um executor cria risco.
- **Bloqueio para usar a métrica como gate:** o avaliador aceita a mesma referência para várias tentativas e entrega 100% mesmo quando só há uma evidência distinta. Os estimadores corretos não corrigem esse problema de procedência.
- **Limites operacionais:** o demo durável é de operador único; um experimento concorrente deixou um efeito existente em estado `ready`. O detector de loops perde timeouts intercalados por leituras, e o verificador de Markdown não reconhece links com título.
- **Valor imediato:** ACI e compaction são úteis como verificadores locais de escopo claro. Avaliação, orquestração e segurança têm alto potencial, mas dependem dos gates prioritários. Inferência e cache oferecem planejamento e instrumentação; ganhos de GPU, latência e cobrança não foram demonstrados.

## Respostas e evidência

| Pergunta | Onde verificar |
| --- | --- |
| Fidelidade, simplificações, erros conceituais e ferramentas faltantes | [Fidelidade científica](SCIENTIFIC_FIDELITY.md) e [matriz por skill](SKILL_QUALITY_MATRIX.md) |
| Sobreposição, integração, portabilidade, robustez e qualidade funcional | [Matriz](SKILL_QUALITY_MATRIX.md), [execução durável](DURABLE_EXECUTION_REVIEW.md) e [segurança](SECURITY_AND_RUNTIME.md) |
| Precisão de roteamento, restrições e custo adicional | [Orquestrador](ORCHESTRATOR_EVALUATION.md), [ACI](ACI_EVALUATION.md) e [benchmark](BENCHMARK_RESULTS.md) |
| Generalização, causalidade, desempenho do modelo e produção | Ainda N/V; veja o [protocolo](BENCHMARK_RESULTS.md) |
| Causas, recomendações, testes de aceitação e dez prioridades | [Causas](ROOT_CAUSE_ANALYSIS.md) e [roadmap](IMPROVEMENT_ROADMAP.md) |

As capacidades devem continuar separadas por contrato: ACI valida uma interface, descoberta limita a exposição de um catálogo; journal mantém estado, recuperação decide sobre efeitos, compactação verifica continuidade de contexto; spans temporais e análise semântica se complementam. Reutilize contratos e fixtures entre elas. Nenhuma duplicação justifica remover uma skill durante esta auditoria.

## Reproduzir

Na raiz do AAES, com Python 3.12+:

```sh
python -B audit/production-ai-engineering/run_audit.py --repo . --out audit/production-ai-engineering/evidence/recheck.json
```

O script reavalia os probes contra o código atual; o [resultado histórico](evidence/independent-results.json) preserva a execução anterior. O runner grava a evidência separadamente e verifica que o conteúdo das skills, ferramentas, instaladores Python e ZIPs não mudou. Use `--require-clean` para tornar as divergências bloqueantes.
