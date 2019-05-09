
# Experiments

## Pendulum Simulation

### 2d Model

We've already seen some of the interaction that occurs with a double pendulum in @Sec:2dpendulum, with the lower pendulum causing higher frequency oscillations to be overlaid.
In @Fig:distmass-impact-animation and @Fig:distmass-impact-plot we can see how the rotational inertia of the lower mass changes the interaction of the two part of the pendulum.

![Difference between an double pendulum with two point masses and one where the lower mass is modeled as a distributed mass.](./figures/impact-of-rotational-inertia.gif){ #fig:distmass-impact-animation }

![Angles and angular velocity comparison of point mass and distributed mass pendulum.](./figures/dp-2d-distmass-inertias.svg){ #fig:distmass-impact-plot }

We can see a strong impact of the rotational inertia of the lower link, which changes the movement of the system.
Of note is how the lower link now pushes the upper link a lot more, instead of only hanging below it.
This is important as a rope cannot transmit such a force.
So the CMG platform should probably use rods, instead of ropes to attach to the hook of the crane.
Also, this points to a limitation of the model, as the upper link is modeled as a rod, not a flexible rope.
In strong oscillations we should therefore expect to see a difference in behavior between our model and the real world.

### 3d Model

Now lets look at some simulations of our 3d pendulum.
Just to validate the model let us create some 2d excitations.
In @fig:3d-projected-large-exitation we see that the motion remains in the plane of excitation as we would expect.
Note that the movement is not identical to that of the 2d model, due to the fact that minuscule numerical errors lead to noticeable changes in a chaotic system such as a double pendulum (see discussion in appendix @sec:2d-pointmass-eom).
This is also most likely the reason that once we rotate the plane of excitation (@Fig:3d-projected-large-exitation-diagonal) the motion breaks out of the plane at some point.

![Large exitation of double pendulum modelled with equations of motion derived using projected angles. From left to right: front, side and top view. Note how the path begins to differ strongly when compared to the simulation using the 2D model. This is a prime example of how minor changes can cause large differences in chaotic systems like a double pendulum.](figures/double_pendulum_3d_large_exitation.gif){ #fig:3d-projected-large-exitation }

![Large out of plane exitation of double pendulum modelled with equations of motion derived using projected angles. From left to right: front, side and top view. Note how the small inaccuracies cause motion outside of the original plane of exitation. These deviations quickly become chaotic for larger exitations.](figures/double_pendulum_3d_Large_Exitation-diagonal.gif){ #fig:3d-projected-large-exitation-diagonal }

As we move to the 3d model with distributed mass another effect occurs.
In @Fig:distmass-sim-gh the pendulum was given a 2d excitation but also the mass was given an angular velocity around the axis of suspension.
The break from the 2d plane occurs immediately, which is most likely due to the impact of gyroscopic reaction due to the pendulum motion and the inertia around the axis of suspension.

![Simulation of a distributed mass hanging from a point mass. Initial excitation lies in a plane, but the mass is also given an angular velocity. Note how the pendulum breaks out the of the plane. Most likely due to gyroscopic effects.](./figures/distmass-sim-gh.gif){ #fig:distmass-sim-gh }

### Dampening Controller

In @Sec:dampening-controller we saw that a rudimentary PD$\alpha$ controller was able to dampen our double pendulum.
We now apply the same controller to a selection of models whose parameters have been set to reflect our lab setup, a small fast deployment crane and a large tower crane.
The lower links are modeled as having a load attached to them according to our inertia estimates (see @Fig:inertia-data).
Note that this is quite a worst case scenario, as we are assuming the maximum crane load and also the largest excitation.
The largest excitation estimate does not stem from the maximum load, but instead from a jib rotation as maximum speed with the load attached at the very tip of the crane.
The load capacity at the tip is significantly lower than the maximum load (see @Fig:crane-data).

These models are then each excited by 10°, which is an approximation of the various base-rate estimates (see @Fig:crane-base-rates).
In @Fig:crane-dampening-comparison-animation and @Fig:crane-dampening-comparison-plot we can see how the controller proves effective for each crane, dampening the motion in the course of a few oscillations.
This is predominantly due to the fact that we are scaling the control gains with the inertia of the lower link.
This results in up to 50.000 Nm of torque being applied to dampen the largest crane.
While probably possible, it is questionable whether this is economically sensible.

![Dampening of three different model cranes using the same PD$\alpha$ controller. From left to right: approximate dimensions of our lab setup, a small fast deployment crane and a fairly large tower crane. The parameters are taken from @Fig:crane-data and @Fig:inertia-data. Controller setting: $k_P=1.0 \cdot I_2, k_D=4.0 \cdot I_2, \alpha=0.5$. Initial excitation is 10°, approximating the determined base rates (see @Fig:crane-base-rates)](./figures/crane-dampening-comparison.gif){ #fig:crane-dampening-comparison-animation }

![Angles and velocities of the cranes of the dampening comparison.](./figures/dp-2d-distmass-controller.svg){ #fig:crane-dampening-comparison-plot }

![Torque used in dampening of the above cranes.](./figures/dp-2d-distmass-controller-torques.svg){ #fig:crane-dampening-comparison-torques }

What would happen if equip a CMG-array that is capable of providing the desired torque?
Of course the dampening will become less effective, but importantly it will still work.
This is due to the oscillating nature of our problem.
As the crane oscillates back and forth the torque required to dampen it changes direction.
So recalling the nature of the torque work space of a CMG array we can see that the CMGs will try to provide the desired torque until they reach the edge of the workspace i.e. saturate.
As the pendulum begins to swing back the direction of the target torque reverses and the CMG array has its entire workspace in front of itself and can provide torque again.
This is part of the behavior that we will look into in the following section.

\todo{update torque plot to include sum and gradient}
\todo{discuss Nms and Nm/s in context of dampening}

The code used for the above simulations can be found in the appendix in @Sec:2d-dp-wcontroller.

## Pendulum-CMG Interaction

As our prototype uses an SPCMG array we will attach a model of said array to our double pendulum to look into the interactions between the CMGs and the pendulum.
For this I would like to briefly introduce the steering law and method of singularity avoidance employed by the SPCMG.
Subsequently we will look at how said singularity avoidance interacts with the dampening controller and as well as the dynamics of the CMG as it interacts with the pendulum.

### Scissored Pair CMGs Steering and Singularity avoidance { #sec:spcmg-steering }

The SPCMG is tasked with producing the torque we wish to apply to the lower link of the double pendulum.
Since the control input of the SPCMG is the speed of its gimbal motors we require a steering law to translate the desired torque in to a gimbal speed.

![Abstract model of a scissored pair control moment gyroscope.](./figures/spcmg-steering.png){ #fig:spcmg-steering }

Looking at an abstract view of the SPCMG (@Fig:spcmg-steering) and given that the design of the mirrored pair dictates that $\delta = \delta_1 = \delta_2$ and $h_r = h_1 = h2$ the torque produced by the array can be easily determined:

\begin{align}
h_{net} &= 2h_r\sin(\delta)\\
\tau &= \dot{h_{net}} = 2\dot{\delta}h_r\cos(\delta)
\end{align}

Ergo the steering law is (*W* denotes a target value):

\begin{equation}
\dot{\delta_W} = \frac{\tau_W}{2h_r\cos(\delta)}
\end{equation}

From this steering law it is obvious that we must ensure that $-90° < \delta < 90°$ to avoid dividing by zero and hence the singularity of the array.
Since in reality our gimbals have limited accelleration ($\ddot{\delta}_{max}$) we must override $\dot{\delta}_W=0$ with sufficient breaking distance ($\delta_{BD}$) to the singularity.
In the following *Y* denotes the current state of the gimbals.

\begin{align}
\delta_{BD} =& \frac{\dot{\delta}^2_Y}{2\ddot{\delta}_{max}} \\
\dot{\delta}'_W =&
  \begin{cases}
      0, & \text{if} \quad \delta_{max} - (\delta_{BD} + |\delta_Y|) \leq 0 \quad \text{and} \quad \delta_Y \cdot \dot{\delta}_W \geq 0 \\
      \dot{\delta}_W, & \text{otherwise}
  \end{cases}
\end{align}

The conditional tests for two factors:

1. do we have to break given current speed and position?
2. is the desired gimbal speed moving us towards the singularity?

The latter condition is important, since we might have a case where the gimbal speed set by the steering law moves us away from the singularity and it wouldn't make sense to override this speed with zero.

### SPCMGs Steering Dampening

First let us validate the steering law and singularity avoidance.
In @Fig:spcmg-avoidance-animation we see a double pendulum approximating our lab setup.
The difference between the two models shown, lies in the velocity of their gyroscopes (1000 rpm and 5000 rpm respectively).

We can see that the dampening is effective for both cases, but the lower gyroscope speed leads to the CMGs having a smaller torque workspace.
So we can clearly observe the behavior outlined in our previous section on the dampening controller.
As the pendulum oscillates the SPCMG alternates between its two singularities, but in between is able to repeatedly produce torque to dampen the oscillation.

It is interesting to see the difference in final gimbal angles (see @Fig:spcmg-avoidance-1000rpm-plot and @Fig:spcmg-avoidance-5000rpm-plot), once the respective models have come to rest.
The slow gyroscopes result in an end state closer to the center of the SPCMGs workspace.
This is due to the asymmetric torque targets, due to the much faster dampening in the model with the faster gyroscopes.
This points to some interesting questions regarding control optimized to position the CMGs in an advantageous position within their workspace.

![Comparison of SPCMG singularity avoidance with different gyroscope speeds (1000 rpm and 5000 rpm). The narrow cylinder pointing out of the disc indicates the direction of the angular momentum vector of the gyroscope.](./figures/spcmg-avoidance-animation.gif){ #fig:spcmg-avoidance-animation }

![Behavior of the singularity avoidance mechanism for the scissored pair configuration. Note that the speed of the gyroscopes and the maximum acceleration of the gimbals have been set to extremely low values to better illustrate the singularity avoidance.](./figures/spcmg-avoidance-1000rpm-plot.svg){ #fig:spcmg-avoidance-1000rpm-plot }

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum acceleration of the gimbals lower than the maximum attainable with our prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the out of axis torque introduced by the gimbaling motion (see discussion in @Sec:cmg-dynamics)](figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot }

### Dynamics of CMG attached to Pendulum

- base rates vs. pendulum length vs. gyro inertia
- reaction torque vs. array design vs. CMG orientation
- explain why passive stabilization is not possible

## Robot Tasks

\missingfigure{selected robot task}


![Comparison of the base torques for the same path performed and two different speeds. At low speeds the longer time spent out of balance require a larger momentum envelope while higher robot speeds require greater gimbal agility to achieve the momentum dynamics.](./figures/robot-load-speedcomparison-plot.jpg){#fig:robot-load-speedcomparison-plot}


We can distinguish between three types of torque:

- torque from robot motion and its own inertia
- process forces transmitted from the tool to the base
- torque from imbalance

Conclusions:

- trade off between Nm/s and Nms due to time spent out of balance
- it might make sense to add sliding weight to keep COG inline with rope

## Simulated Process Compensation

\missingfigure{Video of spcmg with robot underneath, with and without forces}

\missingfigure{path deviation due to forces of robot}

- simulated base forces and torques
- deviation from path

## Hardware Experiments

### Prototype Setup

![CMGs used in the hardware prototype. The Design has only two custom parts (gyro wheel, mounting flange) with the rest begin off the shelf components (incl. made to measure shafts).](./figures/CMG-sidebyside.jpg){ #fig:cmg-plans }

![Hardware SPCMG prototype with robot attached to it. Gyros are in the aluminum cases with the gyro motors mounted on their sides. The gimbal motors hang underneath the gyros. The motor controller and power supply are mounted underneath the platform. The gyro controller, IMU and communication interface for these are mounted on top. Note that the rope suspension was rotated by 90° for the picture.](./figures/KR3_seitlich.jpg){ #fig:prototype-sideview }

\missingfigure{Image of custom PCB, case and controllers}

\missingfigure{gyro motor alignment mount}

- CMG Design
- Array
- performance values
- Motor Control
- Sensors
  - filters
- Issues
- Recommendations

### Scissor Constraint

For the SPCMG to work as intended we need to maintain the symmetry between the two giros.
This is usually achieved by linking the two gimbals mechanically and using a single actuator.
The use of a mechanical linkage is simple to implement and offers the added benefit of dealing with the reaction torque caused by motion of the base system (see discussion in @Sec:cmg-dynamics)

Given that our prototype should later be extended to a four CMG roof array we opted to enforce the SPCMG symmetry with a control loop.
The controller applies a proportional gain of the difference in angle between the two gimbals to the desired gimbal velocity.

### Tuning Controller on Hardware

\missingfigure{video of dampening hardware prototype}

\missingfigure{plots of dampening hardware prototype}

- validation of PDalpha controller
- tuning of parameters
