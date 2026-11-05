# Validação inicial

| Camada | Resultado |
| --- | --- |
| Estrutura e referências | 5 skills validadas. |
| Política determinística | 40 casos: precision@3 e recall@3 = 1,00; seleção desnecessária e omissão = 0; restrições esperadas e ordem exata = 100%. |
| Execução local | 11 testes de dependências, conflitos, gates, traces, comparação pareada, instalação e exportação. |
| Instaladores | 5/5 em destino Codex via PowerShell e 5/5 em destino Claude via Git Bash, com verificação de hashes. 5 ZIPs gerados. |
| Teste independente | Um pedido em PT de recomendação com dois timeouts e sem acesso ao ledger selecionou `process-verifier`, modo de planejamento e sem despacho. A confirmação ficou inconclusiva. |
| Benchmark de eficácia | Não executado. Não há ganho mensurado sobre uma execução sem skills. |

As 40 classificações semânticas são fornecidas aos testes. Os números descrevem a política sobre as fixtures; não medem compreensão de linguagem natural. Tempo médio local observado: aproximadamente 0,014 ms por caso para o ranking, sem chamadas adicionais a modelos; não inclui classificação do host, I/O, prompt ou custo de execução. O teste independente é uma amostra, sem baseline e sem medição de desempenho.
