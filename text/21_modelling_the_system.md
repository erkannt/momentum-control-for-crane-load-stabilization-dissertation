
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

![Cranes used to estimate parameter space of construction cranes. From left to right (increasing payload): L1-24, 71 EC-B, 380 EC-B, 1000 EC-B. ](./figures/cranes.png)

| Name          |  Height [m]|  Reach [m]|  max Load [kg]|  max Load at Tip [kg]|  Translational Speed [m/min]|  Rotational Speed [rpm]|
|---------------|------------|-----------|---------------|----------------------|-----------------------------|------------------------|
| L1-24 (230V)  | 19         | 25        | 2500          | 900                  | 22                          | 0.5                    |
| 71 EC-B 5     | 45         | 50        | 4220          | 1000                 | 63                          | 0.8                    |
| 380 EC-B 16   | 83         | 75        | 15660         | 3000                 | 95                          | 0.8                    |
| 1000 EC-B 125 | 96         | 31.5      | 125000        | 24600                | 100                         | 0.6                    |

## Requirements from Robot Tasks

- design paths with GH/KUKA prc
  - lift against wall
  - array below/beside robot
  - single path below/beside robot
- use mxA for recording
- execute on real robot >>> obtain axis values >>> simulate base torques and forces

![Robot paths programmed using the KUKA|prc plugin for Rhino/Grasshopper.](./figures/robot-path-planning.jpg){#fig:robot-path-planning}

![Axis values simulated by KUKA|prc. Note the sharp corners resulting from unlimited accelleration/jerk values making these values ill-suited to simulate the forces and torques at the robot base.](./figures/kuka-prc-axis-values.jpg){#fig:robot-axis-values}

![Body simulation of the KR3. The masses of the axes have been estimated from the total mass of the robot and the volume of the respective axes.](./figures/kr3-simmechanics-vis.jpg){#fig:kr3-simmechanics}

## Modelling the Crane

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

### Review of Available Crane Models

- crane in essence a pendulum but:
  - tendon is flexible
  - suspension point also exhibits dynamics
  - load exhibits own dynamics
- for this work we shall ignore:
  - flexibility of tendon
  - crane structure dynamics
  - stretch and varying length of tendon
- and instead inlude:
  - load/CMGs as distributed mass with dynamics
  - ergo we need a double pendulum, since otherwise the torque would act at suspension point of the tendon which is way to unrealistic

The following sections will develop this model from a two-dimensional double pendulum to a three-dimensional double pendulum and subsequently go from two point masses to a point mass and a distributed mass.
The generation of equations of motion and subsequent numerical integration are achieved using Python.
The code builds on the educational example of Christian Hill @HillLearningScientificProgramming2016, the three-dimensional model extends the work of O'Conner and Habibi @OConnorGantryCraneControl2013.
I hope that this extended discussion and availability of source code will aid others in extending the model to their needs, espescially when coming from other disciplines.

### Basic Double Pendulum { #sec:2dpendulum }

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

![Oscillations of a double pendulum at small angles and velocities.](./figures/dp-oscillations-animation.gif){ #fig:dp-oscillations-animation }

![Oscillations of a double pendulum at small angles and velocities showing a) how the position for such parameters comes close to a simple pendulum and b) how the two parts of the pendulum interact.](./figures/dp-oscillations.svg){ #fig:dp-oscillations }

### The 3D Model { #sec:3d-pendulum }

![Model of a pointmass double pendulum in three dimensions with a fixed point of suspension.](./figures/crane-8dof.png){ #fig:crane-spherical }

If we extend our pointmass model to three dimension we require two angles to describe the location of each point.
In the 3D model of the double pendulum (@Fig:crane-spherical) $\theta_{i1}$ are the polar angles and $\theta_{i2}$ the azimuthal angles.
This model can be extended to include basic crane dynamics by making the $x_0$ and $y_0$ coordinates of the suspension point as well as $l1$ variable.

To convert to carthesian coordinates:

\begin{align}
x_0 = & 0 \\
y_0 = & 0 \\
z_0 = & 0 \\
\\

x_1 = & l_1 \cdot \sin(\theta_{11}) \cdot \cos(\theta_{12}) \\
y_1 = & l_1 \cdot \sin(\theta_{11}) \cdot \sin(\theta_{12}) \\
z_1 = & -l_1 \cdot \cos(\theta_{11}) \\
\\

x_2 = & x_1 + l_2 \cdot \sin(\theta_{21}) \cdot \cos(\theta_{22}) \\
y_2 = & y_1 + l_2 \cdot \sin(\theta_{21}) \cdot \sin(\theta_{22}) \\
z_2 = & z_1 - l_2 \cdot \cos(\theta_{21}) \\
\end{align}

The Langrangian can once again be determined from the kinetic and potential energies:

\begin{align}
PE = & m_1 \cdot g \cdot z_1 + m_2 \cdot g \cdot z_2 \\
KE = & ^1/_2 \cdot m_1 \cdot \dot{x}_1^2 + \dot{y}_1^2 + \dot{z}_1^2 + \\
     & ^1/_2 \cdot m_2 \cdot \dot{x}_2^2 + \dot{y}_2^2 + \dot{z}_2^2  \\
\mathcal{L} = & KE - PE
\end{align}

From this we can obtain the Euler-Lagrange equations for $\theta_{ij}$ and subsequently solve them for $\dot{\theta}_{ij}$.
Given their complexity this is done using a computer algebra system.
See appendix @Sec:3d-pointmass-eom for the resulting equations and SymPy code used to obtain them.

Sadly the use of spherical coordinates to describe the kinematic contraints of the system leads to numerical issues during simulation.
The issues arise due to the fact that we can arrive at the same coordinates, if we flip the azimuthal angle by 180° and flip the sign of the polar angle (@Fig:3d-model-angle-issues).
While such jumps do not cause issues regarding the position of the pendulum, the spikes in angular velocity that they cause incorrectly represent the kinetic energy in the system.
The effect of this can vary depending of the exitation/inital conditions of the simulation (see @Fig:2d-3d-comparison-large-exitation and @Fig:2d-3d-comparison-small-exitation in the appendix).

![3D double pendulum using spherical coordinates, under small 2D exitation, illustrating the issues of the use of spherical coordinates. Note how  $\theta_{i2}$ jumps in steps of 180° causing $\theta_{i1}$ to remain negative as well as major spikes in angular velocity. These cause an erronous dampening of the pendulum.](./figures/3d-model-angle-issues.svg){ #fig:3d-model-angle-issues }

To alleviate this we can change the description of the kinematic constraints to use projected angles instead of spherical coordinates.
This approach follows that of @OConnorGantryCraneControl2013, where the authors derive the equations of motion for a double pendulum with an attached distributed mass.

![Model of a pointmass double pendulum in three dimensions with a fixed point of suspension, using projected angles instead of spherical coordinates.](./figures/crane-model-projected-angles.png){ #fig:crane-projected-angles }

Given the use of projected angles the cartesian expressions become:

\begin{align}
x_0 = & 0 \\
y_0 = & 0 \\
z_0 = & 0 \\
\\

x_1 = &  l_1 \cdot \sin(\theta_{11}) \\
y_1 = &  l_1 \cdot \cos(\theta_{11}) \cdot \sin(\theta_{12}) \\
z_1 = & -l_1 \cdot \cos(\theta_{11}) \cdot \cos(\theta_{12}) \\
\\

x_2 = & x_1 + l_2 \cdot \sin(\theta_{21}) \\
y_2 = & y_1 + l_2 \cdot \cos(\theta_{21}) \cdot \sin(\theta_{22}) \\
z_2 = & z_1 - l_2 \cdot \cos(\theta_{21}) \cdot \cos(\theta_{22}) \\
\end{align}

## Adding the CMGs

Given the equations of motion with regard to $\ddot{\theta}_i$ we can apply control torque $\tau$ as follows:

$$\ddot{{\theta}'}_1 = \ddot{\theta}_1$$  
$$\ddot{{\theta}'}_2 = \ddot{\theta}_2 + \tau$$
