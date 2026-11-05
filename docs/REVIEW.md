# Revisão e melhorias

## Corrigido antes da publicação

- **Roteamento:** modo de execução não sinaliza despacho se faltarem insumos. Modos offline, leitura e sem delegação removem as ferramentas incompatíveis, com testes para os limites.
- **Autoridade:** o guardião vincula aprovação a pedido, escopo, conteúdo e revisão de política. A referência local reserva cota e consome aprovação em uma transação; o teste concorrente comprova apenas uma reserva. O relógio confiável é consultado depois da aquisição do lock.
- **Recuperação:** a retomada exige reconciliação quando o efeito externo é desconhecido. O teste reabre o banco, bloqueia um replay sem evidência e só avança com a operação correta.
- **Pesquisa:** o arquivo Pareto rejeita violações por repetição e não recebe holdout; patching mede controles e exclui gaps instáveis; RL preserva desfechos inseguros sem dar crédito à declaração do modelo.

## Melhorias com benefício e próximo teste

| Prioridade | Melhoria | Evidência necessária |
| --- | --- | --- |
| Alta | Medir a seleção automática em Codex e Claude Code, incluindo ambiguidade e negativa. | Traces reais por host e modelo, seleção observada e ações registradas; comparar com as 64 classificações de desenvolvimento. |
| Alta | Fazer um estudo pareado, cego e com várias sementes. | Dataset retido, revisão de modelo e host fixada, custos reais, concordância de avaliadores e intervalo por tarefa. O piloto atual não mede ganho geral. |
| Alta para produção | Integrar o guardião a um executor credenciado e o checkpoint ao estado externo. | Testes de bypass, revisão de política durante execução, revogação e reconciliação após falha entre reserva e efeito. A reserva local não encerra essa análise. |
| Média | Validar os protocolos especializados com artefatos reais. | Um experimento de patching com controles em modelo aberto e rollouts de um simulador; registrar diferenças de versão, hardware e resultados. |
| Média | Definir licenciamento e política de releases. | Decisão do mantenedor; não há código de terceiros copiado. |
