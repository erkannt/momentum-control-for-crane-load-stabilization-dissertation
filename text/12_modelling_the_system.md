
# Modelling the CMG-Crane System

## What needs to be modelled

To develop sizing guidelines we need to develop two types of models that let us:

- derive abstracted inputs to our sizing
- understand how the various systems interact and influence our sizing

Overall these models should help us understand the following questions:

- requirements from the applications
  - robot motion >>> simulate and understand base torques
  - part rotation >>> essentially slew rate >>> what are relevant rot. inertia sizes
- parameter space of construction cranes
  - dimensions (rope length, hook load)
  - expected pendulum motion
- requirements for stabilisation
  - how can CMG i.e. torque be used to compensate swinging?
  - does the CMG provide passive stabilisation?
- what governs the baserate of the CMGs attached to the crane?

To understand the basic parameters for the model we will use industry guidelines, norms and technical data provided by crane manufacturers.
The process loads produced by a robot will be determined using real robot motions and multi-physics simulation packages.
To understand the interaction of a CMG array with crane we will model it as a double pendulum system and apply the formulation of CMG dynamics ($\frac{^NdH}{dt}$) to it.

## Parameter Space of Construction Cranes

- range of heights vs. hook loads vs. rotation rates
- note: some hooks are extra heavy to overcome basic rope drag
- permitted swinging
- permitted wind loads >>> part sizes >>> rotational inertia
- capability of control engineering for swing prevention (Lastpendeldämpfung)

## Requirements from Robot Tasks

- design paths with GH/KUKA prc
- use mxA for recording
- execute on real robot >>> obtain axis values >>> simulate base torques and forces

## Double Pendulum

Two models used: 2D and 3D

2D model provides:

- easier understanding of behaviour and control approaches
- a lot of crane control theory uses 2D case, now we can compare
- role of base Forces from robot on plattform stability
- base rates from pendulum motion
- smaller hardware invest, but we can still validate
  - gimbal behaviour
  - controller design
  - sensor noise etc.
  - communication setup
  - indentify hardware issues before proceeding
  - sidestep complex CMG singularities and steering laws

3D model needed for:

- gyroscopic reaction torque from base rate >>> needed for gimbal torque sizing
- role of roof angle re: reaction torque
- base rates from yaw motions of CMG
- yaw control of tranported parts (biggest use case outside of robot stabilisation)

### The 2D Model

#### Point-Mass Double Pendulum

Most rudimentary model: double pendulum modelled as massless rods with point masses.
Equations of motion commonly known e.g. @HillLearningScientificProgramming2016:

![2D double pendulum as point masses on rigid, massless rods. Taken from @HillLearningScientificProgramming2016](./figures/double-pendulum-geometry.png){ heigh=4cm }

The Langrian ($\mathcal{L} = KE - PE$) being

$\mathcal{L} =  \tfrac{1}{2}(m_1+m_2)l_1^2\dot{\theta}_1^2 + \tfrac{1}{2}m_2l_2^2\dot{\theta}_2^2 + m_1l_1l_2\dot{\theta}_1\dot{\theta}_2\cos(\theta_1 - \theta_2) + (m_1+m_2)l_1g\cos\theta_1 + m_2gl_2\cos\theta_2.$

the following equations of motion can be obtained from the Euler-Langrange Equations ($\frac{\mathrm{d}}{\mathrm{d}t}\left(\frac{\partial\mathcal{L}}{\partial \dot{q}_i}\right) - \frac{\partial \mathcal{L}}{\partial q_i} = 0$):

$$\ddot{\theta}_1 = \frac{m_2g\sin\theta_2\cos(\theta_1-\theta_2) - m_2\sin(\theta_1 - \theta_2)(l_1\dot{\theta}_1^2\cos(\theta_1 - \theta_2) + l_2\dot{\theta}_2^2) - (m_1+m_2)g\sin\theta_1}{l_1(m_1 + m_2\sin^2(\theta_1-\theta_2))},$$  
$$\ddot{\theta}_2 = \frac{(m_1+m_2)(l_1\dot{\theta}_1^2\sin(\theta_1-\theta_2) - g\sin\theta_2 + g\sin\theta_1\cos(\theta_1-\theta_2))+m_2l_2\dot{\theta}_2^2\sin(\theta_1-\theta_2)\cos(\theta_1-\theta_2)}{l_2(m_1 + m_2\sin^2(\theta_1-\theta_2))}$$

When solving these through numerical integration one obtains the known chaotic motion @Fig:chaotic-dp.

![Chaotic motion of a double pendulum.](./figures/double_pendulum.gif){ #fig:chaotic-dp }

In our crane-CMG scenario we shouldn't encounter angles and velocities sufficient to create such chaotic motion outside of catastrophic failure events.
Nevertheless the douple-pendulum makes sense as a basis for our models for two reasons:

- large payloads and their motions
- CMGs control motion by exerting torque

The first point is obvious but requires us to extend the model from a point-mass to a distributed mass model (at least for the second mass i.e. the payload).
We will do this in a later section since the stabilisation and controlled movement of payloads is one of the goals of this work.

The second point can already be illustrated by the mass-point model.
In @Fig:dp-oscillations-animation and @Fig:dp-oscillations we can see how for small angles and velocities the double pendulums position is close to a regular pendulum.
But looking at the velocity and especially the acceleartion we can see the interaction between the two parts of the pendulum.

to be continued ...

![Oscillations of a double pendulum at small angles and velocities.](./figures/dp-oscillations-animation.gif){ #fig:dp-oscillations-animation }

![Oscillations of a double pendulum at small angles and velocities showing a) how the position for such parameters comes close to and simple pendulum and b) how the two parts of the pendulum interact.](./figures/dp-oscillations.svg){ #fig:dp-oscillations }




### Torque Control

Given the equations of motion with regard to $\ddot{\theta}_i$ we can apply control torque $\tau$ as follows:

$$\ddot{{\theta}'}_1 = \ddot{\theta}_1$$  
$$\ddot{{\theta}'}_2 = \ddot{\theta}_2 + \tau$$

We design a controller using the scheme proposed by @HoangSimpleEnergybasedController2014 for underactuated mechanical systems.

The difference between a uncontrolled system, proportional control, PD-control and PD-control that is informed by the state of both the upper and lower link is illustrated in @Fig:controller-comparison-animation and @Fig:controller-comparison-plot.

![Comparison of various control regimes for a douple pendulum with a control torque applied to its lower link. From left to right: a) no control torque b) $k_P  = 10$ c) $k_P = 1, k_D = 4$ d) $k_P = 1, k_D = 4, \alpha = 0.5$](./figures/controller-comparison-animation.gif){ #fig:controller-comparison-animation }

![Swing angles (in degrees) of the two links ($\theta_1$ and $\theta_2$) of double pendulum with various control regimes applied.](./figures/controller-comparison-plot.svg){ #fig:controller-comparison-plot }

#### Distributed-Mass Double Pendulum

TBD

## Control Moment Gyroscope

### SPCMG Steering Law

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

#### Singularity Avoidance

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

#### Scissor Constraint

For the SPCMG to work as intended we need to maintain the symmetry between the two giros.
This is usually achieved by linking the two gimbals mechanically and using a single actuator.
The use of a mechanical linkage is simple to implement and offers the added benefit of dealing with the reaction torque caused by motion of the base system (see discussion in ???).

Given that our prototype should later be extended to a four CMG roof array we opted to enforce the SPCMG symmetry with a control loop.
The controller applies a proportional gain of the difference in angle between the two gimbals to the desired gimbal velocity.

![Comparison of SPCMG singularity avoidance with different gyroscope speeds (1000 rpm and 5000 rpm). The narrow cylinder pointing out of the disc indicates the direction of the angular momentum vector of the gyroscope.](./figures/spcmg-avoidance-animation.gif){ #fig:spcmg-avoidance-animation }

![Behaviour of the singularity avoidance mechanism for the scissored pair configuration. Note that the speed of the gyroscopes and the maximum accelleration of the gimbals have been set to extremly low values to better illustrate the singularity avoidance.](./figures/spcmg-avoidance-1000rpm-plot.svg){ #fig:spcmg-avoidance-1000rpm-plot }

![Singularity avoidance mechanism for the scissored pair configuration at higher gyroscope speed. Note that the maximum accelleration of the gimbals lower than the maximum attainable with our prototype. This not only helps illustrate the singularity avoidance mechanism but also reduces the out of axis torque introduced by the gimballing motion (see discussion in ???)](./figures/spcmg-avoidance-5000rpm-plot.svg){ #fig:spcmg-avoidance-5000rpm-plot }