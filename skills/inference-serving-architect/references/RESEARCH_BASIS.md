# Research basis

Primary reference: [NVIDIA Dynamo, Disaggregated Serving and Overall Architecture](https://docs.nvidia.com/dynamo/components/router/disaggregated-serving).

Dynamo documents distinct prefill and decode pools, placement and KV transfers. The helper models conventional transformer KV only; it is not a server or a benchmark and cannot size MLA or hybrid architectures without a different memory model.
