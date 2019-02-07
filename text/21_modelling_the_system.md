
# Modelling the CMG-Crane System

## What needs to be modelled

To develop sizing guidelines we need to develop two types of models that let us:

1. derive abstracted inputs to our sizing
2. simulate the designed system to validate and inform our sizing

These models need to cover our three application scenarios for the CMG-crane system:

1. compensation of process torques
2. rotation of loads being lifted by the crane
3. dampening of the pendulum motion of the crane

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
- base rates due to pendulum motion

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

### The 2D Model { #sec:2dpendulum }

#### Point-Mass Double Pendulum

Most rudimentary model: double pendulum modelled as massless rods with point masses.
Equations of motion commonly known e.g. @HillLearningScientificProgramming2016:

![2D double pendulum as point masses on rigid, massless rods.](./figures/2d-pendulum.png)

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

### Pendulum with Distributed Mass

### The 3D Model

![Model of a double pendulum in three dimensions with a fixed point of suspension. Note that the upper link is modelled as having only two degrees of freedom.](./figures/crane-8dof.png){ #fig:crane-8dof }

## Adding the CMGs

Given the equations of motion with regard to $\ddot{\theta}_i$ we can apply control torque $\tau$ as follows:

$$\ddot{{\theta}'}_1 = \ddot{\theta}_1$$  
$$\ddot{{\theta}'}_2 = \ddot{\theta}_2 + \tau$$
