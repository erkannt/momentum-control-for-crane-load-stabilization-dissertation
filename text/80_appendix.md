
# Appendix

## Scissored Pair CMGs

### SPCMG Steering Law {#sec:spcmg-steering}

The SPCMG is tasked with producing the torque we wish to apply to the lower link of the double pendulum.
Since the control input of the SPCMG is the speed of its gimbal motors we require a steering law to translate the desired torque in to a gimbal speed.

![Abstract model of a scissored pair control moment gyroscope.](./figures/spcmg-steering.png){ #fig:spcmg-steering }

Looking at @Fig:spcmg-steering and given that the design of the mirrored pair dictates that $\delta = \delta_1 = \delta_2$ and $h_r = h_1 = h2$ the torque produced by the array can be easily determined:

\begin{align}
h_{net} &= 2h_r\sin(\delta)\\
\tau &= \dot{h_{net}} = 2\dot{\delta}h_r\cos(\delta)
\end{align}

Ergo the steering law is (*W* denotes a target value):

$$
\dot{\delta_W} = \frac{\tau_W}{2h_r\cos(\delta)}
$$

### Singularity Avoidance

From this steering law it is obvious that we must ensure that $-90° < \delta < 90°$ to avoid dividing by zero and hence the singularity of the array.
Since in reality our gimbals have limited accelleration ($\ddot{\delta}_{max}$) we must override $\dot{\delta}_W=0$ with sufficient breaking distance ($\delta_{BD}$) to the singularity.
In the following *Y* denotes the current state of the gimbals.

$$
\delta_{BD} = \frac{\dot{\delta}^2_Y}{2\ddot{\delta}_{max}}
$$

$$
    \dot{\delta}'_W =
    \begin{cases}
        0, & \text{if} \quad \delta_{max} - (\delta_{BD} + |\delta_Y|) \leq 0 \quad \text{and} \quad \delta_Y \cdot \dot{\delta}_W \geq 0 \\
        \dot{\delta}_W, & \text{otherwise}
    \end{cases}
$$

The conditional tests for two factors:

- do we have to break given current speed and position?
- is the desired gimbal speed moving us towards the singularity?

The latter condition is important, since we might have a case where the gimbal speed set by the steering law moves us away from the singularity and it wouldn't make sense to override this speed with zero.

### Scissor Constraint

For the SPCMG to work as intended we need to maintain the symmetry between the two giros.
This is usually achieved by linking the two gimbals mechanically and using a single actuator.
The use of a mechanical linkage is simple to implement and offers the added benefit of dealing with the reaction torque caused by motion of the base system (see discussion in @Sec:cmg-dynamics)

Given that our prototype should later be extended to a four CMG roof array we opted to enforce the SPCMG symmetry with a control loop.
The controller applies a proportional gain of the difference in angle between the two gimbals to the desired gimbal velocity.

![Comparison of SPCMG singularity avoidance with different gyroscope speeds (1000 rpm and 5000 rpm). The narrow cylinder pointing out of the disc indicates the direction of the angular momentum vector of the gyroscope.](./figures/spcmg-avoidance-animation.gif){ #fig:spcmg-avoidance-animation }

![Behaviour of the singularity avoidance mechanism for the scissored pair configuration. Note that the speed of the gyroscopes and the maximum accelleration of the gimbals have been set to extremly low values to better illustrate the singularity avoidance.](./figures/spcmg-avoidance-1000rpm-plot.svg){ #fig:spcmg-avoidance-1000rpm-plot }

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum accelleration of the gimbals lower than the maximum attainable with our prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the out of axis torque introduced by the gimballing motion (see discussion in @Sec:cmg-dynamics)](figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot }

## CMG Variables

@Fig:cmg-data lists the properties of the SPCMG used in this work.

![Properties of the SPCMG with associated symbols and units.](./figures/cmg-data.png){ #fig:cmg-data }

The angular momentum of the gyroscope can be determined as follows:

\begin{align}
\text{h} &= I\omega \\
&= \frac{\pi\rho\text{d}}{2} (r_2^4 - r_1^4) * \omega
\end{align}

Some useful conversions to SI-Units:

\begin{align}
\text{rpm} \cdot \frac{\pi}{30} &= \text{rad}/s \\
\text{g}/\text{cm}^3 \cdot 1000 &= \text{kg}/\text{s}
\end{align}

## Equations of Motion and Simulation using Python

\todo{improve docstrings in python code}
\todo{move to better code include pandoc filter}
\todo{fit 70chars onto A4 page (reduce fixed font size)}

### 2D Pointmass Double Pendulum { #sec:2d-pointmass-eom}

Prior to obtaining the equations of motion for more complex cases, I obtained those of a pointmass double pendulum.
The following code uses the SymPy Python library which allows us to perform symbolic calculations.
The code also validates our results against known equations of motion.

!include code/double-pendulum-2d-lagrangian.py

Subsequently we can copy the resulting equations into a second program to simulate the pendulum.
Note how even though we are using symbolically identical equations, the simulation results begin to differ after a while.
This is a lovely example of numerical inaccuracy in computers and also how minimal changes in a chaotic system  like a double pendulum can cause increasingly large differences in behavior.

!include code/double-pendulum-2d-simulation.py

![Validation of the equations of motion generated using the above SymPy code against those taken from @HillLearningScientificProgramming2016. Note how symbolically equal equations can lead to different result due to numerical inaccuracies in computers.](figures/cas-lit-comparison.svg){ #fig:cas-lit-comparison }

### 2d Pointmass and Distributed Mass

The following code derives the equations of motion for a double pendulum where the second pendulum is a distributed mass.
Note that this assumes that the rotational inertia `I2` is provided relative to the axis of rotation lying in `m1`.

!include code/double-pendulum-2d-distmass-lagrangian.py

!include code/double_pendulum-2d-distmass-eom.txt

### 2d Double Pendulum with Controller { #sec:2d-dp-wcontroller }

The following code extends the python simulation to include the PD$\alpha$ controller by including it in the equations of motion.
It also allows for the visualization of the load as a moving and rotating box.
The code was also cleaned up in comparison to the other simulation code.

!include code/dp-2d-distmass-controller.py

## 3D Pointmass Double Pendulum { #sec:3d-pointmass-eom}

!include code/double-pendulum-3d-simulation.py

### Spherical Coordinates

!include code/double-pendulum-3d-spherical-coords-lagrangian.py

!include code/double-pendulum-eom-3d-pointmass-spherical-coords.txt

![Comparison of 2D and 3D double pointmass pendulum given a small 2D exitation. As also discussed in @Sec:3d-pendulum the description of the kinematics using spherical coordinates leads to the model flipping between nearly identical solutions that cause major steps in the azimuthal angle. While the position of the pendulum is not visibly affected this does lead very high azimuthal angular velocities. The kinetic energy associated with these leads to the dampening of the oscillation we can observe in this plot. Note that the signs of $\theta_{1j}$ have been flipped where $|\theta_{2j}| > \frac{\pi}{10}$ to ease comparison of the two models.](figures/2d-3d-comparison-small-exitation-spherical-coords.svg){ #fig:2d-3d-comparison-small-exitation-spherical }

![Large exitation of double pendulum modelled with equations of motion derived using spherical coordinates. From left to right: front, side and top view. Note how the issues of spherical coordinates cause disturbances that quickly lead to chaotic out of plane motion.](figures/double_pendulum_3d_large_exitation_spherical.gif){ #fig:3d-spherical-large-exitation }

![Comparison of 2D and 3D double pointmass pendulum given a large 2D exitation. Note how they are identical until for roughly the first five seconds and then begin to strongly deviate as the 3D pendulum begins to leave the plane of exitation. This is due to the issues discussed in @Sec:3d-pendulum and illustrated in @Fig:3d-model-angle-issues.](figures/2d-3d-comparison-large-exitation-spherical-coords.svg){ #fig:2d-3d-comparison-large-exitation-spherical }

### Projected Angles

!include code/double-pendulum-3d-lagrangian.py

!include code/double-pendulum-3d-pointmass.txt

![3D double pendulum using projected angles under small 2D exitation. Note how we no longer have the jumps in the second angle observerd in the simulations using spherical coordinates. The motion remains entirely in the XZ-plane. Note that this is no longer the case when the planar exitation lies in a plane outside of the XZ- or YZ-plane (see @Fig:3d-projected-large-exitation-diagonal).](./figures/3d-model-angle-issues-solution.svg){ #fig:3d-model-angle-issues-solution }

![Comparison of 2D and 3D model (projected angles) of double pendulum with small planar exitation. Note the stark decrease in difference and lack of dampening when compared with the spherical coordinate model.](figures/2d-3d-comparison-small-exitation.svg){ #fig:2d-3d-comparison-small-exitation }

## 3D Distributed Mass Pendulum{ #sec:distributed-mass-eom }

!include code/double-pendulum-3d-distmass-lagrangian.py

!include code/double-pendulum-eom-3d-distmass.txt

!include code/cog-rotations.py

!include code/double-pendulum-3d-distmass-simulation.py

!include code/gh-data-import.py

## Other Stuff Looking for a Home

- Workspace of a Roof-Array
- spin up times
- robot tasks and their forces
- gimbal simulation model and validation
- physical demonstrator
- simulink model re: steering law
- IMU sensor
