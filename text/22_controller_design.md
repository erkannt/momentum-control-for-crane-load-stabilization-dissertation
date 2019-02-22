
# Controller Design

To design a control system for our cmg-crane system we will look at the flow of information for the three application scenarios previously described.
From these we will analyse possible controllers for the various scenarios and how one might integrate the various control strategies.

## Overall Flow of Information

Let us look at the three applications in ascending control complexity:

1. dampening
2. part rotation
3. process compensation

![Control flow for pendulum dampening](./figures/dampening-controller.png){ #fig:dampening-controller width=100% }

In @Fig:dampening-controller we have a very straightforward control loop.
The desired state of the pendulum ($P_W$) ist that all angles are zero.
Any difference ($P_E$) from this as measured by the sensor ($P_M$) is fed as input into the controller.
The controller sets a desired torque ($\tau_W$) which the CMG controller tries to achieve.
The resulting torque ($\tau_Y$) then affects our pendulum resulting in the pendulum state $P_Y$.

The challenge in this loop is finding a suitable controller.
This will be covered in @Sec:dampening-controller.
We will see in the experiments performed with our physical prototype that sensor noise and delays in the actuation of the CMGs add further challenges.

![Control flow for part rotation](./figures/rotation-controller.png){ #fig:rotation-controller }

In @Fig:rotation-controller we have a similar setup to our dampening control loop.
Here the desired state is a certain rotational position around the Z-axis or yaw-axis ($\theta_{23}$, see @Fig:crane-8dof)
This would be the case e.g. when the rotation of the part is a programmed action.
Alternatively one could also use a certain rotational velocity as a desired state ($\dot{\theta_{23}}$).
This would be the case in a remote control scenario, where an operator would control the rotation manually.

As also pointed out in @LeeAnalysisFieldApplicability2012 the inertia of the part to be rotated obviously has a major impact on the torque required to perform the rotation.
Therefore this control loop utilises our knowledge regarding the torque output by the CMGs and the measured rotation speed to estimate the inertia of the part.
This should improve the performace of the controller when used for programmed rotations but also ensure a consistent remote control experience for the operator as their speed control will be similar regardless of the part being handled.

![Control flow for the compensation of process torques](./figures/process-controller.png){ #fig:process-controller width=100% }

Finally @Fig:process-controller shows the more complex flow of information for the compensation of process torques.
At is base lies the basic damping controller which is needed to compensate any oscillations that result from torques and forces that the CMG was not able to compensate.

In addition to the desired pendulum state $P_W$ we now also have a desired robot state $R_W$.
The robot could be an actual industrial robot or any other form of kinematic attached to the CMG plattform.
The robot has its own motion controller that outputs motion commands ($R_S$).
These of course cause our robot to move which results in forces ($F_Y$) and torques ($\tau_Y$) that are experienced by the plattform/pendulum.

The torque created by the robot acts in addition to the torque created by the CMGs.
We therefor also pipe the robots motion commands into a model of our robot that lets us simulate the torque that we can expect from the robot.
This value is subtracted from the torque target set by the dampening controller and our CMGs should therefor ideally fully compensate any torque produced by the robot.
Since part of the torque at the robots base stems simply from the pull of gravity on the robots joints we also have to pipe the current plattform angle into our robot model.

Since our CMGs won't be perfect and in any case can't compensate forces we have to assume that the robots motion will cause the pendulum to swing.
This is why we feed the measured position of the robot ($R_M$) and the pendulum ($P_M'$) into a second simple model that provides us with the actual position of the robot endeffector ($R_M'$).
This position is subtracted from the target position coming from the path planning, so that the robot controller may attempt to compensate the error.

The above diagrams also show how these three different control tasks can be easily integrated with each other.
By adding the estimator from the dampening controller to the process controller we can achieve a single control loop for all our applications (@Fig:integrated-controller).
What remains is the challenge of implementing the dampening/rotation controller in a manner that actually produces stable behaviour for all application scenarios and ideally under a wide range of parameters and uncertainties.

![Integrated controller](./figures/integrated-controller.png){ #fig:integrated-controller }

## Review of Controller Designs

- for cranes in general
- underactuated systems
- parameter estimation / uncertainty

## Dampening Controller { #sec:dampening-controller }

We design a controller for the basic 2D pendulum model (see @Sec:2dpendulum) using the scheme proposed by @HoangSimpleEnergybasedController2014 for underactuated mechanical systems.

The difference between a uncontrolled system, proportional control, PD-control and PD-control that is informed by the state of both the upper and lower link is illustrated in @Fig:controller-comparison-animation and @Fig:controller-comparison-plot.

![Comparison of various control regimes for a douple pendulum with a control torque applied to its lower link. From left to right: a) no control torque b) $k_P  = 10$ c) $k_P = 1, k_D = 4$ d) $k_P = 1, k_D = 4, \alpha = 0.5$](./figures/controller-comparison-animation.gif){ #fig:controller-comparison-animation }

![Swing angles (in degrees) of the two links ($\theta_1$ and $\theta_2$) of double pendulum with various control regimes applied.](./figures/controller-comparison-plot.svg){ #fig:controller-comparison-plot }
