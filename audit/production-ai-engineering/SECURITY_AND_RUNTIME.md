# Segurança e runtime

Foram usados apenas arquivos sintéticos, SQLite temporário e callbacks sem efeito externo. A separação de controle e dados vem do [CaMeL](https://arxiv.org/abs/2503.18813); o AAES é uma demonstração de política e não replica um interpretador com proveniência.

| Prova | Resultado |
| --- | --- |
| S01, S08 | Campo de autoridade na proposta e texto de ticket hostil devolvido por uma ferramenta não autorizaram callbacks. |
| S02 | Atenuação legítima permitida; ampliação de efeitos e validade expirada negadas. |
| S03, S04 | União de origens pública/privada bloqueou sink público; mudar controle ativo foi negado. |
| **S05** | Com controle de exportação ativo, o artefato derivado de público + privado recebeu `allow` quando a proposta omitiu a origem privada. |
| S06, S07 | Violação de quota manteve estado anterior; publicar sem aprovação foi bloqueado. |
| D02 | Concorrência fora do escopo do demo deixou estado e efeito divergentes. |

O **S05** é um bloqueador para usar a decisão como autorização de exportação. Derive a linhagem do artefato final no executor a partir do estado do runtime. Valide origem, autorização e vínculo entre parâmetros canônicos e chamada; negue linhagem incompleta. O campo `executed:false` confirma que não ocorreu exfiltração real. A união de rótulos de entradas declaradas é correta apenas quando a lista é completa e confiável.

Portabilidade e isolamento são fatos separados. O [instalador](../../scripts/test_installers.py) foi executado em destinos temporários e conferiu os ZIPs. As novas ferramentas rodam localmente com a biblioteca padrão; isso não testa dependências do host, isolamento do processo, credenciais, callbacks com privilégios, verificação temporal distribuída ou comportamento nativo de Claude Code/Codex. Não conecte os demos a serviços reais como mecanismo único de segurança.
