
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

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum accelleration of the gimbals lower than the maximum attainable with our prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the out of axis torque introduced by the gimballing motion (see discussion in @Sec:cmg-dynamics)figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot }

## CMG Variables

The SPCMG used in this work has the following properties:

Property                       Symbol                  Size   Unit
----------------------------  --------------------- -------   -----
Density of Gyroscope Disc      $\rho_{gyro}$          7,9      $\text{g}/\text{cm}^3$
Gyroscope Speed                $\omega_{gyro}$        5000       rpm
Inner Gyro Radius              $r_1$                  4          cm
Outer Gyro Radius              $r_2$                  7          cm
Gyro Thickness                 $d$                    3          cm
Max. Gimbal Speed              $\dot{\delta}_{max}$   400         rpm
Max. Gimbal Accelleration      $\ddot{\delta}_{max}$  42494       rpm/s

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


## Other Stuff Looking for a Home

- Workspace of a Roof-Array
- spin up times
- robot tasks and their forces
- gimbal simulation model and validation
- physical demonstrator
- simulink model re: steering law
- IMU sensor
