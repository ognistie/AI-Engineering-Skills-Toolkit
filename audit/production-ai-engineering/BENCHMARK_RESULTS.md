# Benchmarks e limites

## Controles executados

- Linha de base: [55 testes](evidence/baseline-tests.txt), [100 casos estruturados anteriores](evidence/production-routing.txt) (36 novos da expansão + [64 de legado](evidence/legacy-routing.txt)) e [controles sintéticos](evidence/controls.txt).
- Distribuição: [PowerShell](evidence/powershell-install.txt) e [Git Bash](evidence/git-bash-install.txt) verificaram 28 skills instaladas e 28 ZIPs cada, em Windows e destinos temporários.
- Auditoria nova: 23/28 verificações funcionais, 81/81 seleções estruturadas e 65/66 políticas aplicáveis. Os cinco desvios funcionais incluem uma corrida fora do escopo documentado. Não trate esta amostra como taxa de sucesso de agentes ou estimativa de prevalência.
- Desfecho crítico local: D01 reconciliou uma vez; D02, com dois operadores, não preservou consistência. S08 bloqueou uma tentativa construída a partir de texto hostil; S05 retornou uma autorização indevida sem executar o efeito.

## Microbenchmark determinístico

O [resultado bruto](evidence/independent-results.json) registra 11 medições por tamanho do helper de descoberta, excluindo setup. Comparação de **representação**, não de modelos: serializar o catálogo inteiro usa 1.310 / 13.999 / 141.798 bytes para 10 / 100 / 1.000 contratos; a shortlist da intenção rotulada expôs 50 bytes em cada tamanho. Uma seleção exata por tamanho; nenhum token, preço, tempo remoto ou qualidade inferido. As medianas locais estão no JSON e não são metas de latência.

## Comparação com modelos: NÃO EXECUTADA nesta auditoria

O piloto anterior com quatro tarefas e braços A/C é [histórico](../../docs/production-engineering/EVAL_RESULTS.md), sem evidência de ganho e sem medidas de custo. Não há novo endpoint autorizado/pinado, captura de uso ou GPU neste trabalho. Não foram instalados softwares, usados serviços pagos ou iniciados testes custosos.

| Braço previsto | Condição |
| --- | --- |
| A | Agente sem skills. |
| B | Instruções genéricas equivalentes, sem utilitário específico. |
| C | Skill alvo e seus utilitários. |
| D | Combinação justificada (por exemplo, ACI + runtime), somente onde necessária. |

Antes de rodar: congele modelo, ferramentas, permissões, orçamento, revisão, estado inicial, família de tarefas e avaliador. Faça repetições independentes e compare intervalos por tarefa. Registre taxa de sucesso, latência, tokens, custo por tentativa e por tarefa bem-sucedida, recuperação, violações e variabilidade. Separe resultados sintéticos, endpoints e topologias. Não extrapole estimativas locais para produção.
