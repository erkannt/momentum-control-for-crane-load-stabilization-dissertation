
# Controller Design

To design a control system for our cmg-crane system we will look at the flow of information for the three application scenarios previously described.
From these we will analyse possible controllers for the various scenarios and how one might integrate the various control strategies.

## Overall Flow of Information

Let us look at the three applications in ascending control complexity:

1. dampening
2. part rotation
3. process compensation

![Control flow for pendulum dampening](./figures/dampening-controller.png){ #fig:dampening-controller width=100% }

![Control flow for part rotation](./figures/rotation-controller.png){ #fig:rotation-controller }

![Control flow for the compensation of process torques](./figures/process-controller.png){ #fig:process-controller width=100% }


## Dampening Controller

We design a controller for the basic 2D pendulum model (see @Sec:2dpendulum) using the scheme proposed by @HoangSimpleEnergybasedController2014 for underactuated mechanical systems.

The difference between a uncontrolled system, proportional control, PD-control and PD-control that is informed by the state of both the upper and lower link is illustrated in @Fig:controller-comparison-animation and @Fig:controller-comparison-plot.

![Comparison of various control regimes for a douple pendulum with a control torque applied to its lower link. From left to right: a) no control torque b) $k_P  = 10$ c) $k_P = 1, k_D = 4$ d) $k_P = 1, k_D = 4, \alpha = 0.5$](./figures/controller-comparison-animation.gif){ #fig:controller-comparison-animation }

![Swing angles (in degrees) of the two links ($\theta_1$ and $\theta_2$) of double pendulum with various control regimes applied.](./figures/controller-comparison-plot.svg){ #fig:controller-comparison-plot }