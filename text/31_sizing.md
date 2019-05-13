
# Sizing CMGs for Cranes

## Input Parameters

- determine Nms
  - duration of robot tasks
  - duraton of pick and place vs. wind loads???
- determine Nm/s
  - agility of robot
  - swing reqs???
- determine baserate
- derive gimbal torque requirements:
  - from dynamics
  - from reaction torques
- tradeoff between passive stabilisation and gimbal sizing???

## Sizing Workflow

TBD?: $\frac{\omega_{gimbal}}{\omega_{system}} = \frac{\tau_{system}}{\tau_{gimbal}}$

### Dampening Behavior

![Simulation of dampening with different sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-controller-limited-momentum.gif){ #fig:limited-momentum-animation}

![Lower link angle, torque used and position in momentum envelope for dampening with different sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-2d-distmass-limited-momentum.svg){ #fig:limited-momentum-plot}

## Feasability Analysis

- gimbal torques
- gyro speeds and inertias
- size and weight of setup

## Other Stuff

- spinup times