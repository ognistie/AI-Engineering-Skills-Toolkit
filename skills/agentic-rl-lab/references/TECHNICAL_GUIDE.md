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
