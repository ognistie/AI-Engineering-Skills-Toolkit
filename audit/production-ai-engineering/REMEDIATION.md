# Revalidação da auditoria — AAES 0.2.0

Os seis desvios reproduzidos na [auditoria anterior](EXECUTIVE_SUMMARY.md) foram tratados. A [evidência antes da correção](evidence/independent-results.json) continua arquivada. A [nova execução](evidence/remediation-results.json) registra os mesmos cenários com os contratos corrigidos.

| Caso | Correção e resultado observado |
| --- | --- |
| S05 · proveniência | A proposta não define a linhagem: o executor fornece vínculo de controle, destino, origens e digest. Omissão de origem, artefato trocado e ausência de vínculo são negados; um artefato público legítimo continua permitido. |
| E03 · avaliação | O protocolo congela IDs e usa ledger confiável fora das tentativas. Evidência de outro trial, referência duplicada e run reutilizado são inválidos. O controle de 3/4 continua produzindo pass@1=.75, pass@2=1 e pass^2=.50. |
| audit-079 · orquestração | Invocação explícita sem configuração pode carregar a skill para planejar, mas não sinaliza despacho; com todos os insumos, a recomendação de execução continua disponível. |
| D02 · retomada | Uma invocação concorrente é recusada antes de tocar no journal. O primeiro operador termina em `done`, com um efeito e sem erros. O bloqueio é local e liberado no fim do processo. |
| T02 · trajetória | Leituras intercaladas não limpam a janela de falhas de outra operação. Sucesso da mesma operação ou mudança de estado limpa a janela. |
| H03 · documentação | Links com título e destinos entre ângulos são verificados; exemplos em fences continuam ignorados. |

## Verificações

- **61 testes unitários e de integração**; **100 casos de roteamento existentes** e **81 casos de auditoria**. Os **66 checks aplicáveis de política** passaram na auditoria.
- **28/28 controles independentes** e **28 ZIPs** conferidos byte a byte contra os arquivos de origem. Instalação e verificação locais em PowerShell e Git Bash, com destinos temporários.
- O CI executa os controles da auditoria com `--require-clean`; novas divergências falham o job.

```sh
python -B audit/production-ai-engineering/run_audit.py --repo . --out audit/production-ai-engineering/evidence/recheck.json --require-clean
```

As garantias continuam limitadas: a autorização real depende do host derivar linhagem, conferir o digest dos bytes efetivamente enviados e proteger o ledger de desfechos. O lock cobre operadores cooperativos num filesystem local; não há fencing distribuído. As avaliações não medem ativação nativa, eficácia de modelos ou desempenho de GPU.
