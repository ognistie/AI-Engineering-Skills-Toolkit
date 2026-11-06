# Research basis

Primary reference: [CaMeL, Defeating Prompt Injections by Design (2025)](https://arxiv.org/abs/2503.18813).

CaMeL separates trusted control from data handling under capabilities. The executor demo prevalidates all actions, delegates policy to a trusted callback, and only dispatches inert handlers. It is not a sandbox or a faithful CaMeL reproduction.
