# Arquitetura

## Referência e decisões

O [AIWorkbench](https://github.com/BielmFranco/AIWorkbench) (`f353213`) separa entrypoints, recursos sob demanda, ZIP por skill e validação determinística de avaliação comportamental. Sua documentação organiza roteamento por resultado; o diretório `shared/` é de manutenção. AAES aplica esses princípios com implementação independente. O instalador AAES acrescenta propriedade por recibo, hashes, backups, grupos e detecção de modificações. O [toolkit escolhido para publicação](https://github.com/ognistie/AI-Engineering-Skills-Toolkit) estava vazio quando o trabalho começou.

O contrato portátil segue a [especificação Agent Skills](https://agentskills.io/specification). `SKILL.md` é a fonte das descrições de descoberta; os detalhes ficam em referências internas e helpers executáveis. O registry do orquestrador é a fonte de capacidades, riscos, pré-requisitos, conflitos, custos relativos, ferramentas e modos. Nenhuma skill precisa importar arquivos fora da sua pasta.

## Caminho de execução

1. O agente hospedeiro interpreta o objetivo, risco, complexidade e restrições do pedido.
2. O roteador combina capacidades e dependências, ordena candidatos por disponibilidade de evidência, custo e risco, e pode abster-se. O resultado explica lacunas e restrições. Classificação e despacho dependem do host; o helper não os simula.
3. O host carrega apenas as skills necessárias. Helpers são programas locais, sem chamadas a provedores. SQLite é opcional e serve apenas ao checkpoint e à referência de reserva do guardião.
4. Testes determinísticos verificam os contratos e arquivos gerados. O piloto com agentes compara respostas a cenários; não mede taxa de sucesso em produção.

Para adicionar uma skill, crie uma pasta portátil, registre as capacidades e acrescente casos de roteamento adjacentes e de resultado. O núcleo não precisa conhecer o nome da skill. Operações com mais de um trabalhador exigem recursos disjuntos ou exclusão explícita, autorização do host e evidência de que o custo de coordenação compensa.

A implementação entrega as 13 skills, instaladores, empacotamento, fixtures e avaliação local. Integrações distribuídas e treinamento de modelos continuam opcionais; os protocolos descrevem como conectá-los sem exigir infraestrutura para uso normal.
