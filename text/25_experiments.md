
# Experiments {#sec:experiments}

The majority of experiments discussed in this chapter revolve around simulations of the combination of a crane (modeled as a double pendulum) and a CMG array.
The simulations reveal the various interactions between the systems and the challenges that arise from them.
Prior to this, the first section covers the validation of the 2D and 3D double pendulum models as well as the chosen $PD\alpha$ controller's performance in dampening the 2D model.
The latter three sections of this chapter cover the simulated robot tasks, their integration into the pendulum-CMG simulations as well as the preliminary hardware prototype.
Apart from the 3D double pendulum model, the experiments utilize a setup limited to a single axis of pendulum motion (see @Fig:prototype-sketch).

## Pendulum Simulation

### 2D Model

Some of the interaction that occurs within a double pendulum has already been shown in @Sec:2dpendulum, with the lower pendulum causing an overlay of higher frequency oscillations.
The @Fig:distmass-impact-animation and @Fig:distmass-impact-plot show how the rotational inertia of the lower mass changes the interaction of the two parts of the pendulum.

![Difference between a double pendulum with two point masses and one where the lower mass is modeled as a distributed mass.](./figures/impact-of-rotational-inertia.gif){ #fig:distmass-impact-animation short-caption="Comparison of point and distributed mass double pendulum"}

![Angles and angular velocity comparison of point mass and distributed mass pendulum.](./figures/dp-2d-distmass-inertias.svg){ #fig:distmass-impact-plot short-caption="Comparison of point and distributed mass double pendulum (plot)"}

It is significant that the lower link pushes the upper link considerably more, instead of only hanging below it.
This is important, as a rope cannot transmit such a force.
This means that the CMG platform should use stiff links instead of ropes to attach to the hook of the crane.
This also points to a limitation of the model, as the upper link is modeled as a rod, not as a flexible rope.
Therefore, in strong oscillations a difference in behavior between our model and the real world should be expected.

### 3D Model

The following are simulations of the 3D pendulum aimed at validating them through comparison with the 2D model.
By exciting the 3D model in a single plane, the results become comparable.

In @fig:3D-projected-large-exitation it can be seen that the motion remains in the plane of excitation as would be expected.
It should be noted that the movement is not identical to that of the 2D model, due to the fact that minuscule numerical errors lead to noticeable changes in a chaotic system such as a double pendulum (see discussion in appendix @sec:2d-pointmass-eom).
This is also most probably the reason that once the plane of excitation is rotated (@Fig:3D-projected-large-exitation-diagonal), the motion breaks out of the plane at some point.

![Large excitation of double pendulum modeled with equations of motion derived using projected angles. From left to right: front, side and top view. Note how the path begins to differ strongly when compared to the simulation using the 2D model. This is a prime example of how minor changes can cause large differences in chaotic systems such as a double pendulum.](figures/double_pendulum_3d_large_exitation.gif){ #fig:3D-projected-large-exitation short-caption="Comparison of 2D and 3D double pendulum"}

![Large out of plane excitation of the same pendulum. From left to right: front, side and top view. Note how the small inaccuracies cause motion outside of the original plane of excitation. These deviations quickly become chaotic for larger excitations.](figures/double_pendulum_3d_Large_Exitation-diagonal.gif){ #fig:3D-projected-large-exitation-diagonal short-caption="3D double pendulum after out of plane excitation"}

In the case of the 3D model with distributed mass, another effect occurs.
In @Fig:distmass-sim-gh the pendulum was given a 2D excitation but the mass was also given an angular velocity around the axis of suspension.
The break from the 2D plane occurs immediately, which is most likely due to the impact of gyroscopic reaction from the interaction of pendulum motion and inertia around the axis of suspension.

![Simulation of a distributed mass hanging from a point mass. Initial excitation lies in a plane, but the mass is also given an angular velocity. Note how the pendulum breaks out the of the plane, most likely due to gyroscopic effects.](./figures/distmass-sim-gh.gif){ #fig:distmass-sim-gh short-caption="Impact of distributed mass on double pendulum"}

### Dampening Controller

In @Sec:dampening-controller it was seen that a rudimentary PD$\alpha$ controller was able to dampen the double pendulum.
Now the same controller was applied to a selection of models whose parameters have been set to reflect the given laboratory setup, a small fast deployment crane and a large tower crane.
The lower links are modeled as having a load attached to them according to the inertia estimates in @Fig:inertia-data.
Note that this is a worst case scenario, as it assumes the maximum crane load and also the largest excitation.
The largest excitation estimate does not stem from the maximum load, but instead from a jib rotation at maximum speed with the load hanging from the very tip of the crane.
In reality, the load capacity at the tip is significantly lower than the maximum load (see @Fig:crane-data).

These models are then each excited by 10°, which roughly fits the various base-rate estimates (see @Fig:crane-base-rates).
In @Fig:crane-dampening-comparison-animation and @Fig:crane-dampening-comparison-plot it can be seen how the controller works for all cranes, dampening the motion over the course of a few oscillations.
This is predominantly due to the fact that the control gains are being scaled with the inertia of the lower link (see @Fig:crane-dampening-comparison-torques).
This results in up to 50.000 Nm of torque being applied to dampen the largest crane.
While technically possible, it is questionable whether this is economically sensible.
It can also be seen that the requirements with regard to torque dynamics and workspace scale with the torque requirements. 

![Dampening of three different model cranes using the same PD$\alpha$ controller. From left to right: approximate dimensions of the lab setup, a small fast deployment crane and a large tower crane. The parameters are taken from @Fig:crane-data and @Fig:inertia-data. Controller setting: $k_P=1.0 \cdot I_2, k_D=4.0 \cdot I_2, \alpha=0.5$. Initial excitation is 10°, approximating the determined base rates (see @Fig:crane-base-rates)](./figures/crane-dampening-comparison.gif){ #fig:crane-dampening-comparison-animation short-caption="Dampening of example cranes"}

![Angles and velocities of the cranes during the dampening comparison.](./figures/dp-2d-distmass-controller.svg){ #fig:crane-dampening-comparison-plot short-caption="Dampening of example cranes (plot)"}

![Torque used in dampening of the above cranes.](./figures/dp-2d-distmass-controller-torques.svg){ #fig:crane-dampening-comparison-torques short-caption="Torque usage during dampening"}

Were one to use a CMG-array incapable of providing the desired torque the dampening would take longer to stabilize the crane, but importantly it would still work.
This is due to the oscillatory nature of the dampening problem.
As the crane oscillates back and forth, the torque required to dampen it changes direction.
So recalling the nature of the torque workspace of a CMG array, it can be seen that the CMGs will try to provide the desired torque until they reach the edge of the workspace i.e. saturate.
As the pendulum begins to swing back, the direction of the target torque reverses and the CMG array has its entire workspace in front of it and can once again provide torque.
This is part of the behavior that will be investigated in the following section.

The code used for the above simulations can be found in the appendix in @Sec:2d-dp-wcontroller.

## Pendulum-CMG Interaction

As the 2D model only requires torque production around a single axis for stabilization, a model of this array will be attached to the double pendulum to investigate the interactions between CMGs and the pendulum.
The following section therefore briefly introduces the steering law and singularity avoidance for the SPCMG.
Subsequently the interaction of said singularity avoidance with the dampening controller is simulated.

### Scissored Pair CMGs Steering and Singularity Avoidance { #sec:spcmg-steering }

The SPCMG is tasked with producing the torque that is to be applied to the lower link of the double pendulum.
Since the control input of the SPCMG is the speed of its gimbal motors, a steering law is required to translate the desired torque into a gimbal speed.

![Abstract model of a scissored pair control moment gyroscope.](./figures/spcmg-principle.svg){ #fig:spcmg-steering short-caption="Model of scissored pair CMG (SPCMG)"}

Looking at an abstract view of the SPCMG (@Fig:spcmg-steering) and given that the design of the mirrored pair dictates that $\delta = \delta_1 = \delta_2$ and $h_r = h_1 = h2$, the torque produced by the array can be easily determined:

\begin{align}
h_{net} &= 2h_r\sin(\delta)\\
\tau &= \dot{h_{net}} = 2\dot{\delta}h_r\cos(\delta)
\end{align}

Ergo, the steering law is ($W$ denoting a target value):

\begin{equation}
\dot{\delta_W} = \frac{\tau_W}{2h_r\cos(\delta)}
\end{equation}

From this steering law, it is obvious that $-90° < \delta < 90°$  must be ensured to avoid dividing by zero and hence also avoid the singularity of the array.
Since in reality the gimbals have limited acceleration ($\ddot{\delta}_{max}$), $\dot{\delta}_W=0$ must be overridden with sufficient breaking distance ($\delta_{BD}$) to the singularity.
In the following $Y$ denotes the current state of the gimbals.

\begin{align}
\delta_{BD} =& \frac{\dot{\delta}^2_Y}{2\ddot{\delta}_{max}} \\
\dot{\delta}'_W =&
  \begin{cases}
      0, & \text{if} \quad \delta_{max} - (\delta_{BD} + |\delta_Y|) \leq 0 \quad \text{and} \quad \delta_Y \cdot \dot{\delta}_W \geq 0 \\
      \dot{\delta}_W, & \text{otherwise}
  \end{cases}
\end{align}

The conditional tests for two factors:

1. Does breaking have to be initiated given the current speed and position?
2. Is the desired gimbal speed causing movement towards the singularity?

The latter condition is important, since there might be a case where the gimbal speed set by the steering law moves away from the singularity and it would not make sense to override this speed with zero.

### SPCMGs Steering during Dampening

First the steering law and singularity avoidance must be validated.
In @Fig:spcmg-avoidance-animation there is a double pendulum approximating to the given lab setup.
The difference between the two simulations lies in the velocity of their gyroscopes (1000 rpm and 5000 rpm respectively).
It can be seen that the dampening is effective for both cases, but the lower gyroscope speed leads to the CMGs having a smaller torque workspace.
So the behavior outlined in the previous section on the dampening controller can be clearly observed here.
As the pendulum oscillates, the SPCMG alternates between its two singularities, repeatedly producing torque in between, to dampen the oscillation.

The difference in final gimbal angles (see @Fig:spcmg-avoidance-1000rpm-plot and @Fig:spcmg-avoidance-5000rpm-plot) once the respective models have come to rest is of note.
The slow gyroscopes result in an end state closer to the center of the SPCMGs workspace.
This is due to the asymmetric torque targets that result from the much faster dampening in the model with the faster gyroscopes.
This points to some interesting questions regarding control optimized to position the CMGs in an advantageous position within their workspace.

![Comparison of SPCMG singularity avoidance with different gyroscope speeds (1000 rpm and 5000 rpm). The narrow cylinder pointing out of the disc indicates the direction of the angular momentum vector of the gyroscope.](./figures/spcmg-avoidance-animation.gif){ #fig:spcmg-avoidance-animation short-caption="SPCMG singularity avoidance at different gyroscope speeds"}

![Behavior of the singularity avoidance mechanism for the scissored pair configuration. Note that the speed of the gyroscopes and the maximum acceleration of the gimbals have been set to extremely low values to better illustrate the singularity avoidance.](./figures/spcmg-avoidance-1000rpm-plot.svg){ #fig:spcmg-avoidance-1000rpm-plot short-caption="SPCMG singularity avoidance at 1000 rpm"}

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum acceleration of the gimbals is lower than the maximum attainable with the prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the axis torque introduced by the gimbaling motion (see discussion in following section).](figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot short-caption="SPCMG singularity avoidance at 5000 rpm"}

### Dynamics of CMG attached to Pendulum { #sec:cmg-pendulum-interaction }

Recalling the various components of the CMG's torque discussed in @Sec:cmg-dynamics, these components (@Fig:cmg-torque-components-plot) and totals (@Fig:cmg-torque-totals-plot ) can be plotted for the 2D pendulum simulations.

![Components of torque produced by a single CMG in a SPCMG array dampening the motion of a double point mass pendulum.](./figures/cmg-torque-components-plot.svg){ #fig:cmg-torque-components-plot short-caption="Torque components produced by single CMG during dampening"}

![Total torques experienced by the platform and gimbal motor due to a single CMG in a SPCMG (same simulation as @Fig:cmg-torque-components-plot).](./figures/cmg-torque-totals-plot.svg){ #fig:cmg-torque-totals-plot short-caption="Total torque acting on platform and motor"}

There are several observations that can be made from the above plots.
First, there are a few SPCMG specific behaviors.
In this model the desired torque output should be produced around the Z-axis.
As the two gyroscopes rotate in opposite directions, the output torque in Z is the sum of the respective output of the two CMGs.
The gimbal rotates around the Y-axis, ergo this is where the gimbal motor torque acts.
As the CMGs move from their center position towards the singularities, the torque being produced increasingly acts around the X-axis instead of the desired Z-axis.
This is why as the singularity is approached, the gimbals speed up to maintain the output around the Z-axis.
Inversely, the reaction torque stemming from the base rate of the lower link interacting with the gyroscopes inertia is strongest when the CMGs are in the center position and goes to zero as they approach the singularity.
Note how the maximum reaction torque occurs as the pendulum passes through the vertical for the second time, as here the base rate is highest and the CMGs are also roughly in their center position.

In the case of the SPCMG, both the motor torques and reaction torques cancel out, which is why the above figures plot an individual CMG.
In other arrays the interactions will be more complex, but similar in principle.

Several observations can be made that are relevant for sizing and arranging these CMGs:

1. Regarding the gimbal motor sizing, the reaction torque due to the base rate dominates the torque requirements for the gimbal motor.
2. The torque required to overcome the inertia of the gimbal assemblies might be on the low side.
   This is firstly due to bearing and gearing friction not being taken into account, but more importantly the dampening control does not require highly dynamic gimbal motions.
3. As previously noted, the reaction torque due to gimbal rotation in negligible, so it will not be included in the sizing considerations.

### Impact of Reaction Torque on the Gimbal Motor { #sec:torque-issue }

As the reaction torque dominates the gimbal axis, the interaction of the base rate with the dampening motions of the gimbals requires a deeper discussion.
The interaction is visualized in @Fig:torque-issue and @Fig:torque-issue-zero.
The intricacies of this interaction stem from simultaneous oscillations of both the pendulum and gimbal.

When the dampening control causes the zero crossings of the pendulum and the gimbals to align, it creates the maximum reaction torque around the gimbal axis.
This is illustrated in @Fig:torque-issue.
However, the direction of the reaction torque is in line with the desired gimbal rotation, as it produces a torque that counters the pendulum's motion.
The @Fig:torque-issue-zero illustrates how control is maintained over the experienced reaction torque via control of the gimbal position.
In the extreme case of the gimbal aligning the gyroscope's axis with the rotation of the pendulum, the reaction torque will always be zero, regardless of the magnitude of the base rate.
The consequences of this interaction are discussed in the sizing section (@Sec:sizing_for_cranes).

![Interaction of the pendulum motion with the CMGs can lead to strong reaction torques depending on the gimbal angle. The blue arrow is the angular momentum of the gyroscope, it therefore remains constant. The green arrow is the angular velocity that the CMG experiences due to the pendulum's oscillations, i.e. the base rate. The red arrow is the cross product of these two vectors, i.e. the reaction torque around the gimbal axis. The magnitude of the reaction torque experienced by the gimbal assembly is denoted by its color (green being zero, red being the maximum). The semicircular bar denotes in color the reaction torque that the gimbal axis would experience at the other gimbal angles given the current base rate.](./figures/torque_issue.gif){ #fig:torque-issue short-caption="Interaction of pendulum motion and CMG"}

### Gimbal Motor Model

The performance of the SPCMG, or any CMG array, is dependent upon the characteristics of the gimbal motors.
To ensure realistic torque production, the model limits both velocity and acceleration of the simulated gimbals.
Their jerk is not limited.

## Robot Tasks

As described in the modeling chapter, a set of robot paths and both the inverse kinematics as well as a real robot can be used to obtain axis values for the paths.
Having run the paths at several speeds, the axis values can be fed into the multi body simulation of the robot to obtain the torques and forces acting at the base of the robot.

![Multi-body robot simulation of the four corners task using values from KUKA|prc. Note how the unlimited acceleration in the inverse solution leads to unrealistically high forces and torques.](./figures/robot-sim-prc.png){ #fig:robot-sim-prc short-caption="Robot simulation based on KUKA|prc axis values"}

![Multi-body robot simulation of the four corners task using values of a real robot obtained via mxAutomation.](./figures/robot-sim-mxa.png){ #fig:robot-sim-mxa short-caption="Robot simulation based on real robot motion"}

@Fig:robot-sim-prc shows the axis values, base forces and torques as well as the torque dynamics and workspace for a simulation using the axis values from KUKA|prc.
As previously noted, the axis values produced by KUKA|prc produce unrealistic values as they assume unlimited acceleration.
Moving to the simulations based on the real axis values (@Fig:robot-sim-mxa), the much smoother axis values are obvious.
It should be mentioned here that more realistic robot simulation tools exist.

![Comparison of the base torques for the same path performed at two different speeds. At low speeds the longer time spent out of balance requires a larger momentum envelope while higher robot speeds require greater gimbal agility to achieve the momentum dynamics.](./figures/robot-load-speedcomparison-plot.jpg){#fig:robot-load-speedcomparison-plot short-caption="Torques at robot base at different speeds"}

Comparing the values of the same path run at different speeds (@Fig:robot-load-speedcomparison-plot) several observations can be made.
Two types of torque from the robot have to be dealt with: the torque caused by its movement and that caused by its center of mass moving out from underneath the base.
The latter lower results in the angular momentum values (Nms) that can be seen for the faster robot, as it spends less time out of balance.
On the other hand, the faster robot motion leads to higher torques and more importantly higher torque dynamics.
This is one area where it might be possible to optimize robot paths to accommodate the capabilities of the CMGs (see discussion of space robots in @Sec:space-cmg-sota).

Should processes cause the robot, load or kinematic system in general hanging from the platform to be out of balance for a longer period of time, adding a sliding or pivoting weight to the platform could be beneficial.
This would not only reduce the workspace requirements of the CMGs, but could also be used to desaturate the CMGs, as it would provide a low agility but infinite source of torque. 

Note that the CMGs cannot directly compensate the forces acting at the robot's base (see @Sec:external-forces).
Also, the above model and simulations to do not include forces and torques produced by the process itself.
So, for example, the force needed to press a drill into a wall is not included.

## Simulated Process Compensation { #sec:robot-comp}

To ascertain the principle feasibility of stabilizing a robot with CMGs, the robot model is attached to the pendulum-SPCMG model.
The base frame of the robot model is attached to the frame in the center of the SPCMG platform so that it moves with the platform.
A second copy of the robot model is placed in the same position, but with its base fixed in space.
The torques simulated at the base of this latter robot model are fed into the equations of motion of the double pendulum.
They therefore act in addition to any torques produced by the CMGs.
The same robot torque values are also fed into the control loop for the CMGs as described in the previous section on controller design (@Sec:controller-design).
As such a simulation does not include any external forces, it should ideally lead to the CMGs perfectly compensating the torques produced by the robot and lead to a static platform.

![Simulation a robot hanging from the SPCMG platform. The left shows how robot deviates from the desired path (transparent robot) as its motion causes the pendulum to swing. The right shows the active compensation by the SPCMGs. Their torque output is informed by a simulated robot model in addition to the pendulum angles. Note how the limited acceleration of the gimbals prohibits the CMGs from perfectly compensating the robot.](./figures/robot_comp.gif){#fig:robot-comp-animation short-caption="Simulation of robot hanging from SPCMG platform"}

![Comparison of the robot's endeffector position while hanging from the pendulum with the programmed target value for simulations with and without compensation by the CMGs.](./figures/robot_compensation.svg){#fig:robot-comp-plot short-caption="Simulation of robot hanging from SPCMG platform" short-caption="Target deviation with/without SPCMG stabilization"}

The @Fig:robot-comp-animation and @Fig:robot-comp-plot illustrate the impact of the CMG stabilization on the robot's path accuracy.
In the animation, the fixed robot is displayed as a transparent overlay.
It can be observed that the CMG stabilization significantly improves the accuracy of the robot, but does not succeed in maintaining perfect stability.
This is due to the limited gimbal acceleration, which prohibits the CMGs from perfectly following sharp accelerations of the robot arm.

A further challenge to CMG stabilization of the robot's motion can also be seen in the above simulations.
As soon as the robot arm moves its center of mass out from under the center of mass of the pendulum, the CMGs have to constantly rotate to produce the necessary torque to compensate this.
Even in the relatively short path simulated here, the CMGs move close to their singularity, where they would no longer be able to produce the torque necessary to maintain the stable position.

These simulations therefore aptly illustrate both the potential of CMG stabilization for robot motion as well as its challenges.
Robot stabilization necessitates careful matching of robot trajectories to the gimbal agility and momentum envelope of the CMGs.
For instance, in the case above, path optimization could reduce the acceleration spikes in the robot's movement, thereby improving the path accuracy without requiring stronger gimbal motors.
Likewise, by moving the robot arm to the left side between targets the CMGs would be moved away from the singularity, thereby providing greater momentum workspace for subsequent operations.

Limited gimbal acceleration, forces from the robot and other external sources as well as sensor and model inaccuracies will ensure that perfect stability will never be attainable.
Additional compensation mechanisms for processes should therefore be considered.
Aside from adding thrusters to create compensating forces, the process path accuracy might be able to be improved by using the robot or other kinematic systems to compensate the error.
This would take careful control engineering so as not to exacerbate the error by introducing further forces and highly dynamic torques.
Given the availability of the crane and robot model, it could be possible to create a predictive controller that compensates the pendulum motion in coordination with the dampening control of the CMGs or even the crane.

## Hardware Experiments

### Prototype Setup

Development of the first hardware prototype began early on and ran alongside the remaining project.
The goal was to validate the theoretical work rapidly to avoid unprofitable efforts.
The size of the prototype was intended to be large enough to handle the torques of the smaller robots of the lab while requiring only a modest hardware budget.

The plan was to begin with a SPCMG array that could be suspended so as to limit the motion to a single plane i.e. 2D motion (see @Fig:prototype-sketch).
Later the intention was to extend the array to a four CMG roof array.
Given the limited manufacturing facilities, the design uses as many readily available and low cost components as possible.

![Hardware SPCMG prototype with attached robot. Gyros are in the aluminum cases with the gyro motors mounted on their sides. The gimbal motors hang underneath the gyros. The motor controller and power supply are mounted underneath the platform. The gyro controller, IMU and communication interface for these are mounted on top. Note that the rope suspension was rotated by 90° for the picture.](./figures/KR3_seitlich.jpg){ #fig:prototype-sideview short-caption="Hardware prototype of SPCMG platform with robot"}

![CMGs used in the hardware prototype. The design has only two custom parts (gyro wheel, mounting flange) with the rest being catalog components (incl. made to measure shafts).](./figures/CMG-sidebyside.jpg){ #fig:cmg-plans short-caption="Plans of CMGs used in prototype"}

@Fig:prototype-sideview shows the completed SPCMG prototype with the KR3 robot hanging underneath.
The gyroscopes are housed in the aluminum cases and have their motors attached to the side with risers to accommodate the couplings.
The gimbal assembly consists of a single bearing block that holds the axle that is clamped into a block attached to the inside of the gyroscope case (see @Fig:cmg-plans).
This setup leads to only two parts per CMG having to be machined: the gyroscope's rotor and the mounting bracket for the gimbal.

The gimbal motors are the same as the gyroscope motors, but geared down to provide higher torque.
The gimbals require position readings and accurate velocity control.
Therefore the gimbal motors have optical encoders attached and are attached to EPOS-70 controllers.
The controllers are programmable via a USB interface and are controlled via CAN bus  from a PC running Simulink Desktop Realtime using a USB-CAN adapter.
See @Fig:hw-list for the main components used in the prototype.

The gyroscopes require a simpler speed controller as they should not experience any dynamic loads.
Therefore DEC-40 development boards were used attached to a custom PCB with an ATTiny microcontroller (see @Fig:cmg-pcb) that provides a serial interface for speed and direction of the gyroscopes.
The same PCB and interface provide communication to the BNO055 inertial measurement unit.

![Main hardware components used in the prototype.](./figures/hw-list.png){ #fig:hw-list short-caption="Prototype hardware component list"}

The CMGs are attached to a welded steel frame that was sized to also later accommodate four CMGs.
The controller and power supplies are mounted to a board inside the frame.
The frame is suspended from two hooks in the ceiling.

![Custom PCB holding the microcontroller, gyro speed controllers, CAN and Ethernet jacks.](./figures/cmg-pcb.jpg){ #fig:cmg-pcb short-caption="Custom PCB used in prototype"}

For the SPCMG to work as intended, it is necessary to maintain symmetry between the two gyroscopes.
This is generally achieved by linking the two gimbals mechanically and using a single actuator to drive them.
The use of a mechanical linkage is simple to implement and offers the added benefit of dealing with the reaction torque caused by motion of the base system (see discussion in @Sec:cmg-dynamics).

Given that it was intended that the prototype should later be extended to a four CMG roof array, it was decided to enforce the SPCMG symmetry with a control loop.
The controller applies a proportional gain of the difference in angle between the two gimbals to the desired gimbal velocity.
By enforcing the symmetry with a control loop it is also possible to perform experiments regarding zero-torque maneuvers to align the gyroscope axes with the axis of rotation.
This is of interest for applications where a manual rotation of the platform should not result in a reaction torque and interference by the CMGs.

### Initial Experiments with the Prototype

The @Fig:dampening-hardware shows some first dampening experiments with the hardware prototype.
The top of the video shows the system being excited with the gyroscope axis oriented parallel to the axis of rotation and the control loop deactivated.
The lower half of the video shows the system given a similar excitation, but with the PD$\alpha$ controller active.
It can be seen how the motion of the gimbals dampens the initial pendulum motion.

![Dampening experiments on hardware prototype.](./figures/Dampening-1000rpm.gif){ #fig:dampening-hardware short-caption="Dampening experiment with hardware prototype"}

Yet, also a multitude of problematic issues can be observed.
Firstly, the initial pendulum motion is dampened, but an out of plane pendulum motion is created.
There are several reasons for this:

- points of suspension are too close together to prevent out of plane motion
- SPCMGs cannot compensate out of plane motion
- the control loop is not precise/agile enough to maintain perfect gyroscope symmetry

The asymmetric motion of the gimbals produces minor torques out of alignment with the in-plane pendulum motion.
The inability of the SPCMG or method of suspension to compensate these torques leads to the behavior seen in @Fig:dampening-hardware.
The dampening also takes considerable time and once it is completed slightly erratic gimbal motions can be observed.

While these initial results are somewhat disappointing, they show the fundamental validity of the approach.
More importantly, they highlight some of the hardware issues that still need to be overcome.
These are discussed in the subsequent section.

### Hardware Issues and Recommendations

The following is a list of issues encountered as well as recommendations for improving the setup.

The attempt at creating a fast-spinning piece of hardware with little to no machining was for the most part successful.
Nevertheless the CMGs are very loud and a recent reassembly showed that some of the gyroscope bearings have suffered and started to stick.
This is partially due to the axle having the wrong thread, leading to standard locknuts not fitting.
Should one manufacture/order new axles, slight changes could also create more space in the case, which would ease assembly.

Furthermore, during tests two of the gyroscope couplings broke.
This was probably due to misalignment of the motor and gyroscope.
Having acquired a 3D-printer, it was possible to rework the gyroscope motor mount to improve the alignment process (@Fig:gyro-mount).
The sticky bearings and misaligned axis are also likely reasons for the gyroscopes taking different periods of time to reach their set speed.

The integrated speed readout via the microcontroller has proven very useful.
The custom PCB has also increased the reliability of the prototype by introducing high quality plugs.
These not only make disassembly much easier, but also reduce the uncertainty from loose/unreliable connections, making debugging easier.

![Redesigned mount for the gyroscope. Note how the motor can be removed without affecting the alignment of the mount, making it easier to align the gyroscope's shaft with the motor. The coupling is also 3D-printed, since the original broke, most likely due to misalignment.](./figures/gyro-mount.jpg){ #fig:gyro-mount short-caption="3D printed mount and coupling for gyroscopes"}

The speed controllers are not able to bring the motors to their maximum velocity expressed by the datasheet.
It was also necessary to adjust their velocity measurement by validating the velocities with a tachometer.
Both of these issues deserve deeper investigation.

The CAN communication with the gimbals works well, but took a long time to set up.
The required commands were extracted from the datasheets and implemented in Simulink.
One major issue is the ability to interface with CAN from Simulink.
The various CAN adapters supported by Simulink do not have driver support for all modes of Simulink (Desktop Realtime, Realtime) and can be quite expensive or require a dedicated target PC if sensor values are to be monitored simultaneously.

Given these issues and price points of the industrial grade motors, interface cards and software products, it might make sense to look elsewhere for solutions.
Since the start of the project, open-source hardware solutions such as the ODrive have emerged.
The ODrive can combine lower cost hobby brushless motors, that have become very powerful due to drones, e-scooters etc., with encoders to create much more affordable servos.
Together with belt drives or cycloidal gears, backlash free drives could be produced using mostly 3d-printed and off-the-shelf low-cost parts.
Generally speaking, the prototype could probably be replicated at lower cost if greater use were made of printed parts and consumer grade hardware.

Alternatives to Simulink and specialized target PCs for projects such as this one are also emerging.
The microcontroller on our custom PCB is probably sufficient to create a UDP to CAN bridge.
As such our reworked PCB also accommodates ethernet as well as CAN hardware.
The interested reader is pointed towards:

- [Modelica](https://www.modelica.org/), [xcos](https://www.scilab.org/software/xcos) and [X2C](https://x2c.lcm.at/)
- [OpenRTDynamics](https://openrtdynamics.github.io/)
- [GRiSP](https://www.grisp.org/) and [Nerves](https://nerves-project.org/)