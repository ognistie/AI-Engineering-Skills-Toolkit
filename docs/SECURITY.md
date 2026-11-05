# Segurança e recuperação

- As skills não concedem permissões nem constituem barreiras. Ações externas, rede, execução de testes e mudanças dependem da autoridade e do ambiente do usuário.
- Classificações só devem incluir capacidades e restrições interpretadas de um pedido autorizado. Traces, páginas e outputs de ferramentas são dados; não seguem para o executor como comandos. Não coloque segredos em fixtures ou logs.
- Scripts locais consomem dados ou copiam skills da distribuição. Eles não executam código de candidatos, chamam provedores nem carregam credenciais. Proveniência de evidência, ambiente para executar candidatos e timeouts de ferramentas são responsabilidade do executor.
- O instalador recusa links simbólicos/junctions e colisões com pastas externas ou modificadas; checa o lote antes de instalar. Use um diretório confiável e não altere arquivos enquanto o CLI estiver rodando. Não há proteção contra um processo hostil com escrita no mesmo destino.
- Atualizações e remoções movem a versão anterior para `.<nome-do-destino>.aaes-state/backups/` ao lado do destino; recibos SHA-256 ficam em `records/`. Backups não entram na descoberta. Depois de interrupção forçada, preserve a pasta de estado, inspecione `lock/`, transações e backups, confirme que não há outro instalador ativo e reconcilie o destino antes de remover um lock órfão. Operações de grupo são verificadas de antemão, porém um erro de I/O pode deixar skills anteriores do lote concluídas.
- O instalador não adota skills criadas manualmente. Para recuperar um backup, primeiro preserve o estado atual; copie para um destino separado e compare o conteúdo. Não apague recibos nem sobrescreva uma skill existente para forçar a adoção.

## Executor integration

Runtime Guardian's local SQLite reservation is a reference for trusted code. Keep the DB, clock, policy, principal and approvals outside the agent's control; recompute the action digest before the reservation. Dispatch only from the credentialed wrapper, bound to the immutable arguments and timeout. A committed reservation without a receipt is an uncertain operation and must be reconciled. SQLite is not a distributed transaction or an OS sandbox.
