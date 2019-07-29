
# Controller Design

To design a control system for our crane-CMG-robot system we will look at the flow of information for the three application scenarios previously described.
By understanding the interdependencies of the systems we can create an integrated control approach.
We will then discuss existing dampening control strategies for cranes and choose one suited for our system.

## Overall Flow of Information

Let us look at the three applications in ascending control complexity:

1. part rotation
2. dampening
3. process compensation

![Control flow for part rotation](./figures/rotation-controller.png){ #fig:rotation-controller }

In @Fig:rotation-controller we have a simple control loop for rotating a part with the CMGs, assuming that the crane is standing still.
The desired state is a certain rotational position around the yaw-axis of the platform/load.
This would be the case e.g. when the rotation of the part is a programmed action.
Alternatively one could also use a certain rotational velocity as a desired state ($\dot{\theta_{23}}$).
This would be the case in a remote control scenario, where an operator would control the rotation manually.
The controller sets a desired torque ($\tau_W$) which the CMG controller tries to achieve.
The resulting torque ($\tau_Y$) then affects our pendulum resulting in the pendulum state $P_Y$.
Any difference ($P_E$) from this as measured by the sensor ($P_M$) is fed as input into the controller.

As also pointed out in [@LeeAnalysisFieldApplicability2012] the inertia of the part to be rotated obviously has a major impact on the torque required to perform the rotation.
Therefore this control loop utilizes our knowledge regarding the torque output by the CMGs and the measured rotational acceleration to estimate the inertia of the part.
This should improve the performance of the controller when used for programmed rotations but also ensure a consistent remote control experience for the operator as their speed control will be similar, regardless of the part being handled.

![Control flow for pendulum dampening as well as rotation of parts.](./figures/dampening-controller.png){ #fig:dampening-controller width=100% }

If we no longer assume that the crane is standing still we move on to a dampening control loop (@Fig:dampening-controller).
This loop is actually nearly identical to the rotation control loop, the only difference being that we extend the desired state of the pendulum ($P_W$) so that all angles are zero, except for $\theta_{23}$, which is set to the desired rotation of the part.
The challenge in this loop is finding a suitable controller, as unlike with the rotational control loop our CMGs do not have direct control over all state variables.
If we model the crane as a double pendulum the loop in underactuated due the CMGs only having indirect control of the upper link's state.
This will be covered in greater detail in @Sec:dampening-controller.
We will see in the experiments performed with our physical prototype that sensor noise and delays in the actuation of the CMGs add further challenges.

If we recall that the rotational inertia also scales the impact of our CMG torques during dampening it becomes clear that an estimation of the rotational inertia is required for effective dampening control.

![Control flow for the compensation of process torques](./figures/process-controller.png){ #fig:process-controller }

Finally @Fig:process-controller shows the more complex flow of information for the compensation of process torques.
At its base lies the dampening/rotation controller, which is needed to compensate any oscillations that result from torques and forces that the CMG was not able to compensate.

In addition to the desired pendulum state $P_W$ we now also have a desired robot state $R_W$.
The robot could be an actual industrial robot or any other form of kinematic attached to the CMG platform.
The robot has its own motion controller that outputs motion commands ($R_S$).
These of course cause our robot to move which results in forces ($F_Y$) and torques ($\tau_Y$) that are experienced by the platform and hence the pendulum.

The torque created by the robot acts in addition to the torque created by the CMGs.
We therefor also pipe the robots motion commands into a model of our robot that lets us simulate the torque that we can expect from the robot.
The forces acting at the base of the robot result in additional torques to the lower link, which we can also feed forward to the dampening controller.
This value is subtracted from the torque target set by the dampening controller and our CMGs should therefor ideally fully compensate any torque produced by the robot.

The torque on the upper link that results from the forces acting at the base of the robot can't be directly compensating using the CMGs.
The only way to counteract the effect of this torque is by causing a rotation of the lower link.
Therefor we add a controller that tries to balance the error produced by the upper link with the error caused by the lower link moving to dampen said error.
Such a controller would most likely not be separate and would instead be integrated into the dampening/rotation controller, but we will show it as separate here to underscore its role.

Since our CMGs won't be perfect and in any case can't fully compensate the impact of external forces, we have to assume that the robots motion will cause the pendulum to swing.
This is why we feed the measured position of the robot ($R_M$) and the pendulum ($P_M'$) into a second simple model that provides us with the actual position of the robot end effector ($R_M'$).
This position is subtracted from the target position coming from the path planning, so that the robot controller may attempt to compensate the error.
We could also add additional sensors to directly measure the error of the robot endeffector.
Since part of the torque at the robots base stems simply from the pull of gravity on the robots joints, we also have to pipe the current platform angle into our robot model.

Once we move to an actual crane we have to extend the state to include the position of the crane hook in addition to its orientation.
A central controller would then set targets for both the cranes winches/gantries as well as the CMG.
Depending on how one uses the robot to compensate path deviations, this central controller might also inform the robot's controller.
Note that other external forces such as wind may also act of the platform and introduce additional error.
The sensors and controllers might be sufficient to deal with such influences, but one could also imagine additional sensors and predictive model that modify the target torques of CMGs to further increase system performance.

What remains is the challenge of finding and implementing suitable controllers.
For certain parts of the system conventional PID controllers, Kalman filters etc. will be sufficient, while other parts will require more work.
In the following we will discuss the underactuation problem and try to find a suitable controller for the dampening of dampening task. 

## Review of Controller Designs

Control of cranes as been a long running endeavor, which is obvious from the amount of publications but also commercially available systems for gantry and habour cranes in particular (see @Fig:swaycontrol-swf).
Given the price and complexity of sensors capable of tracking a hooks position, these mostly use predetermined actuation paths to reduce the creation of oscillations.
This of course if particularly well suited to cranes that perform programmed motions, but can also benefit manual control of cranes.

![Sway control in a gantry crane by SWF. Taken from [@SWFKrantechnikGmbHSWFKrantechnikLastpendeldampfung2012].](./figures/swaycontrol-swf.gif){ #fig:swaycontrol-swf }

Given flexible connection between actuators and end effector (the hook), lack of sensors and inherit flex of the cranes structure, they make for interesting control engineering problems.
The review by Abdehl-Rahman et al. [@Abdel-RahmanDynamicsControlCranes2003] is a good starting point into the literature.
One can find work focussed on improving the control of cranes without a feedback loop such as that by Singhose, Kim and colleagues [@SinghoseManipulationTowerCranes2007, @SinghoseInputShapingControl2008, @VaughanControlTowerCranes2010] who also evaluated the improved performance of operators using such systems [@KimPerformanceStudiesHuman2010].
Others have extended input shaping methods to make them more robust towards parameter changes and disturbances [@AbdullahiAdaptiveOutputbasedCommand2018].

Once one models the crane and its payload as a double pendulum, the problems become even more interesting as it becomes highly underactuated.
Under actuation simply means that we have a less actuators than degrees of freedom (see @Fig:crane-8dof).
This makes such crane models interesting to researchers dealing with such systems.
It also means that controllers for other underactuated systems are of particular interest to us.

Many different approaches to crane control have been proposed and studied covering a whole range of strategies (e.g. linear, non-linear, sliding mode, fuzzy logic etc.).
Another approach to controlling cranes and underactuated systems in general is to use energy-based controller design techniques.
These approaches model the energy of the system and changes to it due to control inputs.
By applying various techniques and theorems (i.e. Lyapunov, LaSalle invariance) one can construct controllers that are proved to be asymptotically stable.
The work by Sun et al. applies this approach to the control of the gantry in a small lab setup that emulates a double pendulum crane [@SunNonlinearAntiswingControl2018].
In this work they show how the derived controller is robust with regard to parameter changes and external disturbances.
An earlier paper by Hoang and Lee show how such controllers perform on a generic underactuated system and compare it to conventional methods (traditional PD, LQR) and more complex approaches (sliding mode control, partial feedback linearization) [@HoangSimpleEnergybasedController2014].
Their results indicate that the control approach outperforms the conventional methods and comes close to the performance of more complex methods.
The authors have subsequently also published a comparative study of several controllers for overhead cranes, derived using energy-based methods [@WonComparativeStudyEnergybased] [^predatory].

[^predatory]: While their former paper was published by Springer, this latter paper appears to be a reworked conference proceeding [@LeeEnergyBasedApproachController2013], both published by predatory publishers. The peer review of the work might therefore be of questionable quality. Nevertheless their work appears to be solid and definitely useful.

![Illustration of the under actuation of a crane. Modeled as a double pendulum of a point mass and distributed mass, adjustable rope length and a suspension point movable in a plane the crane has eight degrees of freedom. Conventionally we only have three actors to control this. By adding the CMGs we drastically reduce the under actuation.](./figures/crane-8dof.png){ #fig:crane-8dof }

## Dampening Controller { #sec:dampening-controller }

Having reviewed the existing research, we design a controller for the basic 2D pendulum model (see @Sec:2dpendulum) emulating the energy based controller designs discussed in the previous section.
These can be described as PD$\alpha$ controllers, where the PD part is as in a convention PID controller.
The $\alpha$ indicates the weighted combination of two state variables in the system, in our case these are the two angles of the two pendulum links.
With the target of both of these hanging vertical ($\theta_{[12]}=0$) this means creating a PD-controller where the error of the two angles is combined as follows:

\begin{equation}
E = \theta_2 + \alpha \theta_1
\end{equation}

The efficacy of this approach can be seen in @Fig:controller-comparison-animation and @Fig:controller-comparison-plot where we compare an uncontrolled system, proportional control, PD-control and PD$\alpha$-control that is informed by the state of both the upper and lower link.

![Comparison of various control regimes for a double pendulum with a control torque applied to its lower link. From left to right: a) no control torque b) $k_P  = 10, k_D = 0$ c) $k_P = 1, k_D = 4$ d) $k_P = 1, k_D = 4, \alpha = 0.5$](./figures/controller-comparison-animation.gif){ #fig:controller-comparison-animation }

![Swing angles (in degrees) of the two links ($\theta_1$ and $\theta_2$) of double pendulum with various control regimes applied.](./figures/controller-comparison-plot.svg){ #fig:controller-comparison-plot }

## Inertia Estimation Controller

As one cannot directly measure the rotational inertia of an object our goal is to use values from our inertial measurement unit (or other sensor tracking rotation).
Together with the current speed and position of the gimbals we then can obtain the rotational acceleration and torque experienced by the system.
Thereby we have all parts needed to calculate the rotational inertia:

\begin{equation}
\dot\omega \tau = I
\end{equation}

Since sensors are noisy and we want to avoid unnecessary jumps and hence jerks in our torque it would make sense to use some kind of state observer.
These come in various ilks, but generally take an estimate of the measurement variance as well as the historic variance of the estimation into account.

The above calculation of inertia assumes that we are trying to measure the inertia of our payload and platform around the Z-axis, while the pendulum is hanging still.
As soon as the pendulum isn't still we have to make adjustments to way the inertia is estimated.
This is because as soon as the pendulum kinetic or potential energy are not zero the acceleration it experiences also depends on said energies in addition to the torque exerted by our CMGs.
Luckily we have already developed a model of the system that can provide us with an estimate of the amount acceleration caused by these energies.
This estimate can be utilized by certain classes of estimator more complex than the ones suited for our estimation at rest.

The benefits of included such an estimator are twofold:
For one it allows for a unification of the dampening and rotation controller.
More importantly it would make the controller robust to changes in the inertia of the platform/payload.
This is critical to making such a system useful and usable in the real world, as it creates a flexibility in application.
Furthermore it creates a more consistent user experience as operator inputs result in similar motions as the estimator adjusts the control response.


## Considerations for the 3d Case

The move from a 2d model to a 3d model brings many challenges.
While most of these lie outside the scope of this work, there are a few considerations that can already be made at this stage.

One of these is how to move the dampening controller from 2d to 3d.
While the principle control approach will most likely hold true for the move, the question arises as to the target and calculation of the error.
For the 2d case the target at error are simply $\theta_i = 0$ and $\theta_i$, respectively.
In the 3d case we have the reference frame/coordinate system at the center of mass of the payload which is also the reference frame for our CMGs torque.
Given the current reference frame as determined by the sensors and a target reference frame (and maybe rotational velocities at that frame) one needs to find a measure of the error between the two and how to process them in the controller.

This is luckily covered by what is known as *attitude control* for air- and spacecraft.
Given that CMGs are not uncommon in spacecraft, some attitude control systems (ACS) might even make special considerations for CMGs.
It will be interesting to see how one might combine attitude control techniques with those for crane control.
Especially since certain issues in ACS, such as singularities arising from the chosen error indicator disappear given the kinematic constraints of the crane-CMG system [@OzgorenComparativeStudyAttitude2019].
Furthermore, since the inertia of spacecraft might also vary with time as they e.g. deploy their solar panels, a decent body of work exists that deals with the estimation of inertia and design of inertia-free controllers.
