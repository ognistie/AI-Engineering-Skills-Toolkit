# AAES 0.1.0: evidências de publicação

| Camada | Resultado observado |
| --- | --- |
| Estrutura, registry e referências | 13 skills válidas no catálogo e no validador do Skill Creator. |
| Política determinística | 64 casos PT/EN com classificações fornecidas: precisão e recall macro @3 de 1,00; seleção desnecessária e omissão de 0%; ordem e restrições esperadas de 100%. |
| Testes locais | 22 testes. Cobrem contratos, tarefas offline, autorização concorrente, recuperação, instalação e ZIP. |
| Instalação e exportação | 13/13 instaladas e verificadas em destinos isolados Codex (PowerShell) e Claude Code (Git Bash); 13 ZIPs comparados byte a byte com as fontes. Os oito helpers novos foram exercitados a partir das cópias instaladas. |
| Comportamento com agentes | [Piloto pareado](../behavioral/paired-pilot.md): 13 cenários, uma resposta com e outra sem AAES por cenário. Nenhuma ação real de ferramenta ou inferência de ganho geral. |

As métricas do roteador testam o ranking depois da classificação, sem chamadas adicionais a modelos. Não medem a compreensão de linguagem natural do host, o custo total de inferência ou a seleção automática em produção. Os testes de instalação no filesystem são distintos da descoberta pela UI de cada host. Patching em um modelo real, treinamento e execução distribuída não foram rodados.

A lista priorizada de lacunas está em [Revisão e melhorias](../../docs/REVIEW.md).
