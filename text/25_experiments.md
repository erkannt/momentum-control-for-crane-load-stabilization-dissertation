
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
This is predominantly due to the fact that we are scaling the control gains with the inertia of the lower link (see @Fig:crane-dampening-comparison-torques).

This results in up to 50.000 Nm of torque being applied to dampen the largest crane.
While probably possible, it is questionable whether this is economically sensible.
We can also see that the requirements with regard to torque dynamics and workspace scale with the torque requirements.

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

### SPCMGs Steering during Dampening

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

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum acceleration of the gimbals lower than the maximum attainable with our prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the out of axis torque introduced by the gimbaling motion (see discussion in following section)](figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot }

### Dynamics of CMG attached to Pendulum

Recalling the various components of the CMG's torque discussed in @Sec:cmg-dynamics we can plot these components (@Fig:cmg-torque-components-plot) and totals (@Fig:cmg-torque-totals-plot ) for our 2d pendulum simulations.

![Components of torque produced by a single CMG in a SPCMG array dampening the motion of a double pointmass pendulum.](./figures/cmg-torque-components-plot.svg){ #fig:cmg-torque-components-plot }

![Total torques experienced by the platform and gimbal motor due to a single CMG in a SPCMG (same simulation as @Fig:cmg-torque-components-plot)](./figures/cmg-torque-totals-plot.svg){ #fig:cmg-torque-totals-plot }

There a several observations that can be made from the above plots.
First there are a few fairly SPCMG specific behaviors.
In our model the desired torque output should be produced around the Z-axis.
As the gyroscopes rotations are mirrored the output torque in Z is the sum of the respective output of the two CMGs.
The gimbal rotates around the Y-axis, ergo this is where the gimbal motor torque acts.
As the CMGs move from their center position towards the singularities, the torque being produces increasingly acts around the X-axis instead of the desired Z-axis.
This is why as we approach the singularity the gimbals speed up to maintain the Z-output.
Inversely the reaction torque stemming from the baserate of the lower link interacting with the gyroscopes inertia is strongest when the CMGs are in the center position and goes to zero as they approach the singularity.
Note how the maximum reaction torque occurs as the pendulum passes through vertical the second time, where the baserate is highest and also the CMGs are roughly in their center position.

In the case of the SPCMG both the motor torques and reaction torques cancel out, which is why we only are looking at a single CMG.
In other arrays the interactions will be more complex, but similar in principle.

We can also make several observations of relevance to sizing and arranging our CMGs.
Regarding the gimbal motor sizing the reaction torque due to the base rate dominates the torque requirements for the gimbal motor.
The torque required to overcome the gimbal assemblies inertia might be on the low side.
For one we are not taking bearing and gearing friction into account, but more importantly the dampening control doesn't require highly dynamic gimbal motions.
As previously noted the reaction torque due to gimbal rotation in negligible, so we will not include it in our sizing considerations.

## Robot Tasks

As described in the modeling chapter we have a set of robot paths and can use both the inverse kinematics as well as a real robot to obtain axis values for the paths.
Having run the paths at several different speeds, we can feed the axis values into the multi body simulation of the robot to obtain the torques and forces acting at the base of the robot.

\todo{rerun and check robot sims; produce nicer plots}

![Multi-body robot simulation of the four corners task using values from KUKA|prc. Note how the unlimited acceleration in the inverse solution leads to unrealistically high forces and torques.](./figures/robot-sim-prc.png){ #fig:robot-sim-prc }

![Multi-body robot simulation of the four corners task using values of a real robot obtained via mxA.](./figures/robot-sim-mxa.png){ #fig:robot-sim-mxa }

In @Fig:robot-sim-prc we see the axis values, base forces and torques as well as the torque dynamics and workspace for a simulation using the values from KUKAprc.
As previously noted, the axis values produced by KUKAprc can't be used for our simulations as they assume unlimited acceleration.
Moving to the simulations based on the real axis values (@Fig:robot-sim-mxa) we can immediately see the much smoother axis values.

![Comparison of the base torques for the same path performed at two different speeds. At low speeds the longer time spent out of balance require a larger momentum envelope while higher robot speeds require greater gimbal agility to achieve the momentum dynamics.](./figures/robot-load-speedcomparison-plot.jpg){#fig:robot-load-speedcomparison-plot}

Comparing the values of the same path run at different speeds (@Fig:robot-load-speedcomparison-plot) we can make several observations.
We have to deal with two types of torque from the robot: the torque caused by its movement and that caused by its center of mass moving out from underneath the base.
This is why we see lower Nms values for the faster robot, as it spends less time out of balance.
On the other hand the faster robot motion leads to higher torques and more importantly higher torque dynamics.
So this is one area where one might optimize robot paths to accommodate the capabilities of the CMGs.

Should one have processes that cause the robot, load or kinematic in general to be out of balance for a longer duration, it might make sense to add a sliding or pivoting weight to the platform.
This would not only reduce the workspace requirements of the CMGs, but could also be used to desaturate the CMGs, as it would provide a unagile but infinite source of torque. 

Remember that the CMGs will not be able to compensate the forces acting at the robot's base.
Also, the above model and simulations to do not include forces and torques produced by the process itself.
So for instance the force needed to press a drill into a wall is not included.

## Simulated Process Compensation

\missingfigure{Video of spcmg with robot underneath, with and without forces}
![Simulation of the SPCMG compensating the motion of a KR3 robot. The pendulum is constrained to 2d motion.](https://via.placeholder.com/800x200?Video+of+SPCMG+compensating+the+robot)

\missingfigure{path deviation due to forces of robot}
![Deviation of the robots endeffector with and without the SPCMG compensation.](https://via.placeholder.com/800x200?Plot+of+path+error+of+robot)

Depending on the settings for the gyroscope's speed and gimbals maximum acceleration the SPCMG is able to perfectly match the torques acting at the robots base.
Give the inaccuracies of our model, signal as well as processing delays and the all the inaccuracies of the physical setup a perfect compensation is highly unlikely.
The imperfections in the torque compensation act in addition to the forces (which we can't compensate using CMGs) and cause the robot to swing.
Here the previously discussed dampening controller kicks in and begins to assist in the dampening of the robot.

Given that we will never be able to compensate the forces with the CMGs and most likely will have errors in the torque compensation it makes sense to consider additional compensation mechanisms for processes.
Aside from adding thrusters to create compensating forces, one might be able to improve the process path accuracy by using the robot/kinematic to compensate the error.
This would take careful control engineering so as not to exacerbate the error by introducing further forces and highly dynamic torques.
Given the availability of the crane and robot model one could imagine a predictive controller that compensates the pendulum motion in coordination with the dampening control of the CMGs or even the crane.

## Hardware Experiments

### Prototype Setup

Development of a first hardware prototype began early on an accompanied most of the project.
The hope was to rapidly validate our theoretical work to avoid dead ends.
The size of the prototype was supposed to be large enough to handle the torques of our smaller robots and otherwise as compact as possible to limit the budget.

The plan was to begin with a SPCMG array that could be suspended so as to limit the motion to a single plane i.e. 2d motion.
Later it should be possible to extend the array to a four CMG roof.
Also given the youth of the chair and lack of facilities we designed the prototype to use as many off the shelf and low cost components as possible.

![Hardware SPCMG prototype with robot attached to it. Gyros are in the aluminum cases with the gyro motors mounted on their sides. The gimbal motors hang underneath the gyros. The motor controller and power supply are mounted underneath the platform. The gyro controller, IMU and communication interface for these are mounted on top. Note that the rope suspension was rotated by 90° for the picture.](./figures/KR3_seitlich.jpg){ #fig:prototype-sideview }

![CMGs used in the hardware prototype. The Design has only two custom parts (gyro wheel, mounting flange) with the rest begin off the shelf components (incl. made to measure shafts).](./figures/CMG-sidebyside.jpg){ #fig:cmg-plans }

In @Fig:prototype-sideview we can see the completed SPCMG prototype with the KR3 robot hanging underneath.
The gyroscopes are housed in the aluminum cases and have their motors attached the to side with risers to accommodate the couplings.
The gimbal assembly consists of a single bearing block that holds the axle that is clamped into a block attached to the inside of the gyroscope case (see @Fig:cmg-plans).
This setup leads to only two parts per CMG having to be machined: the gyroscopes rotor and the mounting bracket for the gimbal.

The gimbal motors are the same as the gyroscopes motors, but geared down to provide higher torque.
We need position readings of the gimbals and also need accurate velocity control.
Therefore the gimbal motors have optical encoders attached and are attached to EPOS-70 controllers.
The controllers are programmable via a USB interface and are controlled via CAN bus from a PC running Simulink Desktop Realtime using a USB-CAN adapter.
See @Fig:hw-list for the main components used in the prototype.

The gyroscopes require only a fairly simple speed controller as they shouldn't experience any dynamic loads.
Therefore we use DEC-40 development boards attached to a custom PCB with an ATTiny microcontroller (see @Fig:cmg-pcb) that lets us set speed and direction over a USB serial interface.
The same PCB and interface provide us with communication to the BNO055 inertial measurement unit.

\missingfigure{List of hardware components}

The CMGs are attached to a welded steel frame that was sized to also later accommodate four CMGs.
The controller and power supplies are mounted to a board inside the frame.
The frame is suspended from two hooks in the ceiling.

\missingfigure{Image of custom PCB, case and controllers}

For the SPCMG to work as intended we need to maintain the symmetry between the two giros.
This is usually achieved by linking the two gimbals mechanically and using a single actuator.
The use of a mechanical linkage is simple to implement and offers the added benefit of dealing with the reaction torque caused by motion of the base system (see discussion in @Sec:cmg-dynamics)

Given that our prototype should later be extended to a four CMG roof array we opted to enforce the SPCMG symmetry with a control loop.
The controller applies a proportional gain of the difference in angle between the two gimbals to the desired gimbal velocity.

### Hardware Issues and Recommendations

The following is a list of issues we encountered as well as recommendation for improving the setup (if we could do things over ...).

The attempt at creating a fast-spinning piece of hardware with little to no machining kind of worked.
The CMGs are very loud and a recent reassembly showed that some of the gyroscope bearing have suffered somewhat and started to stick.
This is partially due to the axle having the wrong thread cut (typo in our order), leading to the locknut not being able to fit.
Slight changes to the axle should also create more space in the case.
As we are currently running to rotors per gyro it is a tight squeeze and when the axle comes loose we grind up against the case.

We managed to break two of our couplings.
This is mostly likely due to misalignment of the motor and gyroscope axis.
Having acquired a 3d-printer we have reworked the gyroscope motor mount to ease with alignment (@Fig:gyro-mount).
The sticky bearings and misaligned axis are also the most likely culprits for the gyroscopes taking different amounts of time to reach their set speed.
The speed readout via the microcontroller has been invaluable in ensuring sensible test runs.
The custom PCB has also provided us with a much more reliable prototype due to the addition of high quality plugs.
These not only make disassembly much easier, but also reduce the uncertainty from loose/unreliable connections, making debugging a lot easier.

\missingfigure{gyro motor alignment mount}

The speed controllers are not able to bring the motors to their maximum velocity put forth by the datasheet.
We also had to adjust the velocity measurement by validating the velocities with a tachometer.

The CAN communication with the gimbals is nice, once it is set up.
It required a lot of datasheet digging to set up the required commands though.
One major issue is the ability to interface with CAN from Simulink.
The various CAN adapters supported by Simulink do not have driver support for all modes of Simulink (Desktop Realtime, Realtime) and can quickly get pricey or require a dedicated target PC if you also wish to monitor sensor values simultaneously.
We have lost multiple days to Simulink driver issues.

Given these issues and pricepoints attached to the industrial motors and Mathworks products it might make sense to look elsewhere for solutions.
Since the start of the project opensource hardware solutions such as the ODrive have emerged.
With an ODrive one can combine much lower cost hobby brushless motors, that have become very powerful ubiquioutus due to drones, e-scooters etc., with encoders to create highspeed/highpower servors for a fraction of industrial solutions.
Together with beltdrives or cycloidal gears one would be able to produce backlash free drives to a project like ours, using mostly 3d-printed parts.

Generally speaking, the ubiquity of low-cost 3d-printers is a game changer and our prototype could probably be replicated at lower if one were to make greater use of printed parts.

Alternatives to Simulink and specialized target PCs for projects like our are also emerging.
Even the microcontroller on our custom PCB is most likely enough to create a UDP to CAN bridge.
It as been shown that UDP is sufficient for most realtime communication and is supported by nearly every software and hardware platform.
As such our reworked PCB also accommodates an ethernet as well as CAN connector.
The interested reader is pointed towards:

- Modelica / xcos
- TUB thing
- Nerves and Grispr

### Tuning Controller on Hardware

\missingfigure{video of dampening hardware prototype}

\missingfigure{plots of dampening hardware prototype}

- validation of PDalpha controller
- tuning of parameters
