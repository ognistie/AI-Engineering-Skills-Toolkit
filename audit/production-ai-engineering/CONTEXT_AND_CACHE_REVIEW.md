# Contexto, compactação e cache

[Manus](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) relata práticas de prefixos estáveis, serialização consistente e estado restaurável. Em C01, as chaves em outra ordem preservam um segmento canônico; mudar a ordem das ferramentas quebra a correspondência do primeiro segmento. A função não simula o tokenizer ou implementação do provedor e não infere hits sem observações.

C02 gravou um artefato em scratch, verificou a restauração exata, então removeu o modo somente leitura e o erro pendente e alterou os bytes. O helper detectou as três mudanças. Isso valida a verificação de um checkpoint; não mede se um modelo retoma corretamente depois de compactação real. Resumos não são autoridade, e persistência de efeitos continua no journal separado.

Para medir: controle modelo, tokenizer, região e forma da requisição. Use pares com prefixos estável/instável e repetições alternadas cold/warm. Colete tokens de entrada, cache e cobrança, TTFT, custo na mesma unidade e qualidade da tarefa. Meça a retomada depois de compactar em pontos iguais. Hoje hits, faturamento, latência do provedor e redução de contexto sem perda de precisão estão N/V.
