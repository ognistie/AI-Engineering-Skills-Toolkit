# Fidelidade científica e simplificações

Fontes primárias consultadas: [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/), [Manus Context Engineering](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus), [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents), [Writing effective tools](https://www.anthropic.com/research/writing-tools-for-agents), [Agent Skills](https://agentskills.io/specification), [Temporal Event History](https://docs.temporal.io/encyclopedia/event-history), [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/), [Inspect AI scorers](https://inspect.aisi.org.uk/scorers.html), [CaMeL paper](https://arxiv.org/abs/2503.18813) e [implementação](https://github.com/google-research/camel-prompt-injection). A URL Dynamo `latest/_sections/architecture.html` do prompt respondeu 404; a revisão usou [Overall Architecture](https://docs.nvidia.com/dynamo/latest/knowledge-base/overview), [vLLM](https://docs.vllm.ai/en/latest/features/disagg_prefill/) e [SGLang](https://docs.sglang.io/advanced_features/pd_disaggregation.html).

| Skill | Mecanismo fiel dentro do escopo | Aproximação ou lacuna |
| --- | --- | --- |
| agent-first-harness | Instruções e feedback navegáveis, inspirados em OpenAI | Manifesto e recibos declarados; não prova legibilidade nem sucesso de comandos. |
| agent-computer-interface | Ferramenta como contrato utilizável; erros acionáveis e validação | Subconjunto plano de JSON Schema; recuperação e escolha pelo modelo N/V. |
| repository-context-architecture | Contexto sob demanda com documentos canônicos | Índice declarado e regex; não entende semântica de Markdown nem desatualização por conteúdo. |
| kv-cache-aware-context | Prefixos estáveis e ordenação de ferramentas, como no Manus | Bytes determinísticos não são tokens, hit do provedor ou cobrança. |
| context-compaction-recovery | Estado restaurável e artefatos externos à janela | Compara campos conhecidos; não prova retomada autônoma ou autorização. |
| inference-serving-architect | Orçamento de KV para atenção convencional e topologia de prefill/decode | Aritmética; sem medição de throughput, scheduler ou custos de comunicação reais. |
| agent-evals-engineer | Separa julgamento de texto e desfecho; pass@k e pass^k distintos | Amostragem finita sobre registros; falta vincular cada evidência à tentativa congelada. |
| trajectory-review-engine | Analisa eventos e resultados com ordem de spans opcional | Padrões consecutivos não garantem causalidade e perdem repetições intercaladas. |
| evaluator-optimizer-loop | Feedback, rubrica fixa, melhor artefato verificado e parada | Decide o próximo passo; não executa avaliador/otimizador nem mede ganho. |
| durable-execution-engine | Distingue replay do journal e reconciliação do efeito | Sem fencing distribuído; demo SQLite é de operador único. |
| brain-tool-runtime-separation | Valida ações num executor separado do texto do modelo | Callbacks de demonstração; autorização e efeitos dependem do host. |
| agent-tool-interface-design | Descoberta seletiva antes de expor esquemas | Tags exatas preclassificadas; não é recuperação semântica nem PTC real. |
| capability-security-architect | Atenuação por subconjunto e validade temporal | Descritores confiáveis e produto cartesiano; não emite token nem consome aprovação. |
| prompt-injection-boundaries | União de rótulos sobre origens listadas e controle ativo fixo | Não propaga linhagem automaticamente. Ao confiar na lista da proposta, diverge da fronteira de informação do CaMeL. |
| runtime-verification-engine | Replay determinístico, ordem, rejeição e gasto cumulativo | Analisa sequência fornecida; ausência de integração obrigatória impede garantia de bloqueio real. |

Os mecanismos locais demonstram utilidade limitada; nenhuma alegação de ganho publicado foi transferida ao AAES.
