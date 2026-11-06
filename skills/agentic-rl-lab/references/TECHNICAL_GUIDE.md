# Technical guide

`python scripts/rollouts.py input.json`

```json
{
  "environment": {
    "allowed_actions": [
      "search",
      "finish"
    ],
    "step_limit": 3,
    "gamma": 0.5,
    "cost_weight": 0.1,
    "terminal_reward": {
      "success": 1,
      "failure": 0,
      "timeout": 0,
      "unsafe": -1
    }
  },
  "episodes": [
    {
      "id": "ep1",
      "initial_state": "s0",
      "steps": [
        {
          "id": "t1",
          "state": "s0",
          "action": "search",
          "next_state": "s1",
          "outcome": "continue",
          "cost": 1
        },
        {
          "id": "t2",
          "state": "s1",
          "action": "finish",
          "next_state": "done",
          "outcome": "success",
          "cost": 0
        }
      ]
    }
  ]
}
```

The environment owns state, outcome and transition IDs. Use a reset(seed, task) boundary returning the initial observation and step(action) returning next observation, trusted outcome, cost and ID. Include a terminal record for timeouts; never infer success from policy text. An out-of-allowlist action must terminate as unsafe. The scorer rejects continued work after termination, missing terminal outcomes, discontinuous states and duplicate transitions.

Reward per step is terminal reward (zero when continuing) minus weighted cost. Return-to-go is the discounted reward sum from each step; it is not a causal effect estimate. Use the same environment and held-out tasks for a fixed policy baseline. If a trainer is authorized, connect its collector to the environment-generated transitions, keep training and evaluation environments separate, and evaluate repeated seeds. This package includes no trainer.

### Reward and state integrity

If the environment exposes canonical successful states, set `environment.success_states` to the exact state IDs. The scorer rejects either direction of a disagreement between the outcome and that set. For general state spaces perform the equivalent assertion in the trusted environment, and retain a separate measurement of objective attainment. A forbidden tool is a terminal unsafe outcome and should not disappear into the average. Try a policy that emits finish repeatedly or imitates a success token; a trusted transition and state should be necessary for reward.
