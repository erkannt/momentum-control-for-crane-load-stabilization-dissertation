
# Modeling the Crane-CMG-Application Systems

> "The problem is, we don't understand the problem." -- Paul MacCready

To develop sizing guidelines we need to develop two types of models that let us:

1. derive abstracted inputs to our sizing
2. simulate the designed system to
  a. understand its behavior
  b. inform and validate our sizing

These models need to cover our three application scenarios for the CMG-crane system:

1. compensation of process torques
2. rotation of loads being lifted by the crane
3. dampening of the pendulum motion of the crane

Overall these models should thereby provide us with means to abstract crane parameters in a way relevant to the sizing of CMGs.
From the other side of our system we need to generate ways to obtain an understanding of the requirements of our processes e.g. part rotation and robot motion.
Then to link crane and application we require a model of the crane-CMG-application system.

To understand the basic input parameters we will use industry guidelines, norms and technical data provided by crane manufacturers.
The process loads produced by a robot will be determined using real robot motions and multi-physics simulation packages.
To understand the interaction of a CMG array with crane we will model it as a double pendulum system, apply the formulation of CMG dynamics (see @Sec:cmg-dynamics) to it and create interfaces to apply outside forces.

## Parameter Space of Construction Cranes { #sec:crane-params }

Given the construction focus of this work and the fact that their parameter spaces have a large overlap with other crane designs we will only consider tower cranes for crane parameter space.
@Fig:lbc-cranes shows a selection of tower cranes manufactured by Liebherr.
Beginning with the compact, bottom slewing cranes we go to the highest load cranes via two intermediate steps.

![Cranes used to estimate parameter space of construction cranes. From left to right (increasing payload): L1-24, 71 EC-B, 380 EC-B, 1000 EC-B. ](./figures/cranes.png){ #fig:lbc-cranes }

![Key parameters of the selected example cranes L1-24, 71 EC-B, 380 EC-B, 1000 EC-B.](./figures/crane-data.png){ #fig:crane-data }

\todo{obtain hook weights of example cranes}

From the data-sheets of the these cranes we can obtain the parameters relevant to our models (see @Fig:crane-data).
We are predominantly interested in the parameters that let us estimate the base rate of the CMGs induced by the motion of the crane as this determines the magnitude of the gyroscopic reaction torque that our gimbal motors need to compensate (see @Sec:cmg-dynamics).
The translational movements of the hook/platform don't contribute to the base rate but as we will see later, the period of the crane-rope/pendulum is of interest here.
Since the period of a pendulum depends on the length of the pendulum the height of the crane will serve as an approximation of lift height and as such as our pendulum length.

The oscillations of a crane tendon can be assumed to be sufficiently small to assume isochronism, that is the frequency is constant while the amplitude changes.
Now while neither the amplitude of the oscillation nor the mass of the pendulum affect the frequency of the oscillation, they do affect the maximum angular velocity.
We can intuitively grasp this if we consider the potential and kinetic energy of a pendulum.

In the zero crossing where the pendulum is aligned with gravity the potential energy is zero while the kinetic energy and hence the velocity is highest (see @Fig:pendulum-velocity)
When the pendulum is at its highest points the inverse is true.
As the potential energy is dependent upon the mass of the pendulum we add the maximum payload of the cranes to the parameter list.

![Illustration of the velocity and acceleration of a pendulum. CC-BY-SA, Wikipedia User Ruryk](./figures/oscillating_pendulum-ccbysa-ruryk.gif){ #fig:pendulum-velocity }

To estimate the amplitude of the oscillations we can either turn to rules and regulations for the safe operation of cranes that specify a maximum allowed amplitude \todo{Rules and regs re: crane oscillations}.
Or we can derive it from the maximum crane load, pendulum length and translational velocity caused by slewing the jib or moving the trolley.
To determine the translational velocity caused by slewing we also require the jib length i.e. reach of the crane the the maximum load at the tip of the jib:

\begin{align}
v_{trolley} =& N_T / 60 \\
v_{jib} =& N_R \frac{2\pi r}{60} \\
\omega =& v \cdot l \\
h_{\text{max}} =& \frac{mv^2}{2mg} \\
\theta_{\text{max}} =& \cos{^-1}\left ( \frac{l-h_{\text{max}}}{l} \right )
\end{align}

With $v$ being the translational speed of the hook, $N_T$ the trolley speed in m/min, $N_R$ the jib's rotational speed in rpm, $r$ the reach of the jib, $\omega=\dot\theta$ the angular velocity of the pendulum i.e. base rate of the hook, $l$ the length of the pendulum, $h$ the elevation of the hook relative to its lowest position and $\theta$ the angle of the pendulum.

![Base rates and maximum excitation of the selected example cranes L1-24, 71 EC-B, 380 EC-B, 1000 EC-B from the above derivations.](./figures/crane-base-rates.png){ #fig:crane-base-rates }

Note that all of the above assumes a regular pendulum.
As we will see in the following section it might be necessary to model the crane as a double pendulum.
Here the hook and payload would be considered as separate masses, hence we include the hook weight in the table of crane parameters.
Note that some hooks are purposely heavy to overcame the rope-drag of the crane pulley when no load is attached.

## Modeling the Crane

While a CMG model will always have to be three-dimensional when it comes to cranes we will begin with a 2d model before moving to 3d models.
A 2d model is not only easier to develop, but more importantly also easier to visualize, plot and understand.
While simpler it still helps us understand critical parts of the cranes behavior and develop control approaches.
Often the insights from a lower dimensional model can help us in the design of the higher dimensional ones.

For our case we can attach a 3d SPCMG model to a 2d crane, as the SPCMG produces its torque along a constant axis.
This lets us understand the basic principles of the CMGs as they interact with the crane, while keeping the model still relatively simple.
We can also study the effect of process torques and forces, by constraining them to the 2d case.

We can continue this mixed approach of a SPCMG and 2d crane into a first hardware prototype.
By building the crane as a swing that hangs from two ropes spanned, we can roughly constrain the motion to a single plane.
This reduces the hardware invest for the first prototype by requiring two instead of four CMGs and still lets us validate CMG behavior.
It also limits the number of components that could cause issues while developing the controller, sensor and communication systems.

### Review of Available Crane Models

The essence of a crane, a hook/load hanging from a rope, is a pendulum.
But unlike the basic point-mass pendulum we know from high-school physics a crane has several important differences.
Most importantly the suspension point of the rope exhibits its own dynamics, causing excitation of the pendulum.
These can stem from controlled movement of the trolley, jib or gantry but beyond this the entire crane structure often exhibits significant flex.
Then the rope itself might actually be a set of ropes, is not rigid and also stretches under load.
The load hanging from a cranes hook is also often so large that it possesses significant inertia leading to its own set of dynamic behavior that interacts with the crane.
And finally we of course have external forces such as wind as well as drag or dampening behavior.

Since all models are wrong, the question is which ones are useful.
For our system we are interested in understanding the interaction of the crane with the CMGs.
As the CMG acts on the crane by exerting torque on its payload, we clearly should model the payload/CMGs as an additional distributed mass hanging from the crane.
While one of our applications is the dampening of pendulum motion of the crane that most of often is induced by moving the crane, we will not model the pendulums suspension point as movable.
We will for now assess the dampening capabilities by inducing a pendulum motion through the chosen initial conditions.
We will also ignore the dynamics of the crane structure itself as well as the flexibility of the cranes rope.

\missingfigure{Illustration of 2d hardware setup}

When one reviews the existing crane models (see [@Abdel-RahmanDynamicsControlCranes2003] for a review until 2003) one finds a large variety of models that focus on different aspects or different crane types.
This lets us copy, mix and adapt to create a model suited for our purpose.
It also means that our CMG-focused model could be extended relatively easily.

The following sections will develop this model from a two-dimensional double pendulum to a three-dimensional double pendulum and subsequently go from two point masses to a point mass and a distributed mass.
The generation of equations of motion and subsequent numerical integration are achieved using Python.
The code builds on the educational example of Christian Hill [@HillLearningScientificProgramming2016], the three-dimensional model extends the work of O'Conner and Habibi [@OConnorGantryCraneControl2013].
I hope that this extended discussion and availability of source code will aid others in extending the model to their needs, especially when coming from other disciplines.

### Basic Double Pendulum { #sec:2dpendulum }

Most rudimentary model: double pendulum modeled as massless rods with point masses.
Equations of motion commonly known e.g. [@HillLearningScientificProgramming2016]:

![2D double pendulum as point masses on rigid, massless rods.](./figures/2d-pendulum.png)

The Langrangian ($\mathcal{L} = KE - PE$) being

\begin{align}
\mathcal{L} = & \tfrac{1}{2}(m_1+m_2)l_1^2\dot{\theta}_1^2 + \tfrac{1}{2}m_2l_2^2\dot{\theta}_2^2 + m_1l_1l_2\dot{\theta}_1\dot{\theta}_2\cos(\theta_1 - \theta_2) \\
& + (m_1+m_2)l_1g\cos\theta_1 + m_2gl_2\cos\theta_2
\end{align}

the following equations of motion can be obtained from the Euler-Lagrange Equations:

\begin{align}
0 = & \frac{\mathrm{d}}{\mathrm{d}t}\left(\frac{\partial\mathcal{L}}{\partial \dot{q}_i}\right) - \frac{\partial \mathcal{L}}{\partial q_i} \\
\ddot{\theta}_1 = & \frac{{m_2g\sin\theta_2\cos(\theta_1-\theta_2) - m_2\sin(\theta_1 - \theta_2)(l_1\dot{\theta}_1^2\cos(\theta_1 - \theta_2) + l_2\dot{\theta}_2^2)}{ - (m_1+m_2)g\sin\theta_1}}
    {l_1(m_1 + m_2\sin^2(\theta_1-\theta_2))}  \\
\ddot{\theta}_2 = & \frac{{(m_1+m_2)(l_1\dot{\theta}_1^2\sin(\theta_1-\theta_2) - g\sin\theta_2}{ + g\sin\theta_1\cos(\theta_1-\theta_2))+m_2l_2\dot{\theta}_2^2\sin(\theta_1-\theta_2)\cos(\theta_1-\theta_2)}}{l_2(m_1 + m_2\sin^2(\theta_1-\theta_2))}
\end{align}

When solving these through numerical integration one obtains the known chaotic motion @Fig:chaotic-dp.

![Chaotic motion of a double pendulum.](./figures/double_pendulum.gif){ #fig:chaotic-dp }

In our crane-CMG scenario we shouldn't encounter angles and velocities sufficient to create such motion outside of catastrophic failure events.
Nevertheless the double-pendulum makes sense as a basis for our models for several reasons:

- large payloads and their motions
- CMGs control motion by exerting torque

The first point is obvious but requires us to extend the model from a point-mass to a distributed mass model (at least for the second mass i.e. the payload).
We will do this in a later section since the stabilization and controlled movement of payloads is one of the goals of this work.

The second point can already be illustrated by the point-mass model.
In @Fig:dp-oscillations-animation and @Fig:dp-oscillations we can see how for small angles and velocities the double pendulums position is close to a regular pendulum.
But looking at the velocity and especially the accelerations we can see the interaction between the two parts of the pendulum.
We can expect the impact of the lower pendulum to increase as we move to a distributed mass.

![Oscillations of a double pendulum at small angles and velocities.](./figures/dp-oscillations-animation.gif){ #fig:dp-oscillations-animation }

![Oscillations of a double pendulum at small angles and velocities showing a) how the position for such parameters comes close to a simple pendulum and b) how the two parts of the pendulum interact.](./figures/dp-oscillations.svg){ #fig:dp-oscillations }

Until now the model has been using a point mass for both links.
When we replace the lower mass with a distributed mass, we need to add a term to the kinetic energy to capture the rotational energy of the moving mass:

\begin{equation}
KW_{\omega} = \tfrac{1}{2} I \omega^2
\end{equation}

Since our point of rotation does not lie in the center of mass of our distributed mass (picture the platform hanging below the hook), the rotational inertia is not simply that of the mass.
Instead we must apply the parallel axis theorem also known as Huygens-Steiner theorem:

\begin{equation}
I = I_{CoM} + mr^2
\end{equation}

With $I_{CoM}$ being the inertia of our mass around its center of mass, $r$ the distance from this center of mass to the axis of rotation and $m$ the mass of our object.

### The 3D Model { #sec:3d-pendulum }

![Model of a point-mass double pendulum in three dimensions with a fixed point of suspension.](./figures/crane-spherical.png){ #fig:crane-spherical }

If we extend our point-mass model to three dimension we require two angles to describe the location of each point.
In the 3D model of the double pendulum (@Fig:crane-spherical) $\theta_{i1}$ are the polar angles and $\theta_{i2}$ the azimuthal angles.
This model can be extended to include basic crane dynamics by making the $x_0$ and $y_0$ coordinates of the suspension point as well as $l1$ variable.

To convert to cartesian coordinates:

\begin{align}
x_0 = & 0 \\
y_0 = & 0 \\
z_0 = & 0 \\
x_1 = & l_1 \cdot \sin(\theta_{11}) \cdot \cos(\theta_{12}) \\
y_1 = & l_1 \cdot \sin(\theta_{11}) \cdot \sin(\theta_{12}) \\
z_1 = & -l_1 \cdot \cos(\theta_{11}) \\
x_2 = & x_1 + l_2 \cdot \sin(\theta_{21}) \cdot \cos(\theta_{22}) \\
y_2 = & y_1 + l_2 \cdot \sin(\theta_{21}) \cdot \sin(\theta_{22}) \\
z_2 = & z_1 - l_2 \cdot \cos(\theta_{21}) \\
\end{align}

The Langrangian can once again be determined from the kinetic and potential energies:

\begin{align}
PE = & m_1 \cdot g \cdot z_1 + m_2 \cdot g \cdot z_2 \\
KE = & ^1/_2 \cdot m_1 \cdot \dot{x}_1^2 + \dot{y}_1^2 + \dot{z}_1^2 \\
     & + ^1/_2 \cdot m_2 \cdot \dot{x}_2^2 + \dot{y}_2^2 + \dot{z}_2^2  \\
\mathcal{L} = & KE - PE
\end{align}

From this we can obtain the Euler-Lagrange equations for $\theta_{ij}$ and subsequently solve them for $\dot{\theta}_{ij}$.
Given their complexity this is done using a computer algebra system.
See appendix @Sec:3d-pointmass-eom for the resulting equations and SymPy code used to obtain them.

Sadly the use of spherical coordinates to describe the kinematic constraints of the system leads to numerical issues during simulation.
The issues arise due to the fact that we can arrive at the same coordinates, if we flip the azimuthal angle by 180° and flip the sign of the polar angle (@Fig:3d-model-angle-issues).
While such jumps do not cause issues regarding the position of the pendulum, the spikes in angular velocity that they cause incorrectly represent the kinetic energy in the system.
The effect of this can vary depending of the excitation/initial conditions of the simulation (see @Fig:2d-3d-comparison-large-exitation-spherical and @Fig:2d-3d-comparison-small-exitation in the appendix).

![3D double pendulum using spherical coordinates, under small 2D excitation, illustrating the issues of the use of spherical coordinates. Note how  $\theta_{i2}$ jumps in steps of 180° causing $\theta_{i1}$ to remain negative as well as major spikes in angular velocity. These cause an erroneous dampening of the pendulum.](./figures/3d-model-angle-issues.svg){ #fig:3d-model-angle-issues }

To alleviate this we can change the description of the kinematic constraints to use projected angles instead of spherical coordinates.
This approach follows that of [@OConnorGantryCraneControl2013], where the authors derive the equations of motion for a double pendulum with an attached distributed mass that has two degrees of rotational freedom.
The following extends this to a full three degrees of freedom, to not only closer model realistic crane load motion but also to accommodate our use-case of load rotation.

![Model of a point-mass double pendulum in three dimensions with a fixed point of suspension, using projected angles instead of spherical coordinates.](./figures/crane-model-projected-angles.png){ #fig:crane-projected-angles }

\todo{Projected angle double pendulum figure}

Given the use of projected angles the cartesian expressions become:

\begin{align}
x_0 = & 0 \\
y_0 = & 0 \\
z_0 = & 0 \\
x_1 = &  l_1 \cdot \sin(\theta_{11}) \\
y_1 = &  l_1 \cdot \cos(\theta_{11}) \cdot \sin(\theta_{12}) \\
z_1 = & -l_1 \cdot \cos(\theta_{11}) \cdot \cos(\theta_{12}) \\
x_2 = & x_1 + l_2 \cdot \sin(\theta_{21}) \\
y_2 = & y_1 + l_2 \cdot \cos(\theta_{21}) \cdot \sin(\theta_{22}) \\
z_2 = & z_1 - l_2 \cdot \cos(\theta_{21}) \cdot \cos(\theta_{22}) \\
\end{align}

Assuming a point-mass pendulum the Langrangian would be the same as before:

\begin{align}
PE = & m_1 \cdot g \cdot z_1 + m_2 \cdot g \cdot z_2 \\
KE = & ^1/_2 \cdot m_1 \cdot \dot{x}_1^2 + \dot{y}_1^2 + \dot{z}_1^2 + \\
     & ^1/_2 \cdot m_2 \cdot \dot{x}_2^2 + \dot{y}_2^2 + \dot{z}_2^2  \\
\mathcal{L} = & KE - PE
\end{align}

Since we want to model the lower mass (our platform and load) as a distributed mass we have to add the kinetic energy of the rotating mass to our Langrangian.
For this we need to express the rotational velocities and inertia of the mass in a common reference frame.
We define this to be the center of gravity hanging a distance $l_2$ from our point-mass $m_1$.
Should the center of gravity change due to e.g. robot motion this difference will be modeled as an external torque acting upon the platform.
The inertia tensor in this reference frame then is:

\begin{align}
  I_{m2} =
    \begin{bmatrix}
      I_{xx} & 0 & 0 \\
      0 & I_{yy} & 0 \\
      0 & 0 & I_{zz} \\
    \end{bmatrix}
    _{X_3Y_3Z_3}
\end{align}

The rotations required to transform the reference frame $X_2Y_2Z_2$ that is aligned with our world axes to the reference frame $X_3Y_3Z_3$ also let us obtain the rotational velocities $\omega_{X_3Y_3Z_3}$ from our projected angle velocities $\dot{\theta}_{2j}$.

![Sequence of rotations to transform the world aligned reference frame to the reference frame of our distributed mass.](./figures/cog-rotations.png){ #fig:cog-rotations }

\todo{CoG rotations figure}
\todo{Improve coordinate system notation}

The rotations illustrated in @Fig:cog-rotations can be expressed as:

\begin{align}
R_{2 \rightarrow 3} = & R_Y(\theta_{21})R_X(\theta_{22})R_Z(\theta_{23}) \\
= &
\left[\begin{matrix}\cos{\left (\theta_{21} \right )} & 0 & - \sin{\left (\theta_{21} \right )}\\0 & 1 & 0\\\sin{\left (\theta_{21} \right )} & 0 & \cos{\left (\theta_{21} \right )}\end{matrix}\right]
\left[\begin{matrix}1 & 0 & 0\\0 & \cos{\left (\theta_{22} \right )} & - \sin{\left (\theta_{22} \right )}\\0 & \sin{\left (\theta_{22} \right )} & \cos{\left (\theta_{22} \right )}\end{matrix}\right]
\left[\begin{matrix}\cos{\left (\theta_{23} \right )} & - \sin{\left (\theta_{23} \right )} & 0\\\sin{\left (\theta_{23} \right )} & \cos{\left (\theta_{23} \right )} & 0\\0 & 0 & 1\end{matrix}\right]
\end{align}

This lets us express the required rotational velocities as follows. Note that we use $-\theta_{21}$ as its direction is opposite to that of the right-hand-rule.

\begin{align}
  \omega_3 = & R_{2 \rightarrow 3} \omega_{X_{2}} + R_{2 \rightarrow 3} \omega_{Y_{2}} + \omega_{Z_{3}} \\
  = & R 
    \begin{bmatrix}
      \dot\theta_{22} \\ 0 \\ 0
    \end{bmatrix} +
  R 
    \begin{bmatrix}
      0 \\ -\dot\theta_{21} \\ 0
    \end{bmatrix} +
  \begin{bmatrix}
    0 \\ 0\\ \dot\theta_{23}
  \end{bmatrix} \\
  \omega_{X_{3}} = &
    -\dot{\theta}_{21} ( -\sin{\theta_{21}} \sin{\theta_{22}} \cos{\theta_{23}} - \sin{\theta_{23}} \cos{\theta_{21}} ) \\
    & + \dot{\theta}_{22} (-\sin{\theta_{21}} \sin{\theta_{22}} \sin{\theta_{23}} + \cos{\theta_{21}} \cos{\theta_{23}})\\
  \omega_{Y_{3}} = & -\dot{\theta}_{21} \cos{\theta_{22}} \cos{\theta_{23}} \\
    & + \dot{\theta}_{22} \sin{\theta_{23}} \cos{\theta_{22}}\\
  \omega_{Z_{3}} = & -\dot{\theta}_{21} (-\sin{\theta_{21}} \sin{\theta_{23}} + \sin{\theta_{22}} \cos{\theta_{21}} \cos{\theta_{23}}) \\
    & + \dot{\theta}_{22} (\sin{\theta_{21}} \cos{\theta_{23}} + \sin{\theta_{22}} \sin{\theta_{23}} \cos{\theta_{21}}) \\
    & + \dot{\theta}_{23}
\end{align}

The Lagrangian then becomes:

\begin{align}
\mathcal{L} = & (KE + KE_\omega) - PE \\
KE_\omega = & ^1/_2 \cdot \omega_3 \cdot I_{m2} \cdot \omega_3 \\
= & ^1/_2 ( I_{XX} \cdot \omega^2_{X_3} + I_{YY} \cdot \omega^2_{Y_3} + I_{ZZ} \cdot \omega^2_{Z_3}) \\
\end{align}

The equations of motion can then once again be obtained from our computer algebra system.
These can be used for the numerical simulation.
Since the 3D plotting of Matplotlib is slightly limited I switched to Rhino/Grasshopper for visualization (@Fig:sim-gh).
For this the state-vectors of the simulation are transformed to cartesian points for the masses as well as an X- and Y-vector for the reference frame of our mass.
See the appendix (@Sec:distributed-mass-eom) for equations of motion and all code.

![Visualization of simulated 3D double pendulum with the lower mass as a distributed mass. The lower mass begins with a small angular velocity around the link axis. Visualized using Rhino/Grasshopper.](./figures/gh-screenrecording.gif){ #fig:sim-gh }

This process can be continued to add further aspects like wind or a movable point of suspension.
In the following section we will see that certain aspects can be added relatively easy by modifying the state of the the system.
Other aspects, such as a movable point of suspension would require a new Langrangian, as they introduce new terms to the kinetic or potential energy.

An alternative would be to use multi body simulation tools as are available in Modelica or Simulink.
Here individual block that contain e.g. a distributed mass or a rotary joint can be connected with each other (see @Fig:modelica-example).
Especially Modelica offers a very clean way of creating new blocks and defining their connections, so that they can interface with block of the built in library.

![Rudimentary implementation of our model in Modelica. Note that this lacks connections to input torque from the CMGs and uses a different angle description.](./figures/modelica-example.gif){ #fig:modelica-example }

## Adding the CMGs and External Excitation

The torques and forces acting upon the system can't be included in the above Langrangian as energies, instead they must be added as source terms to the resulting equations of motion.

The torque generated by the CMGs ($\tau$) changes the angular acceleration of the lower link depending on its moment of inertia.
For the two-dimensional model the necessary modifications to the equations of motion are straightforward:

\begin{align}
\ddot{{\theta}'}_1 = & \ddot{\theta}_1 \\
\ddot{{\theta}'}_2 = & \ddot{\theta}_2 + \frac{\tau}{m_2 l_2^2}
\end{align}

The three-dimensional model is slightly more complex due to our choice of angles.
The torque produced by the CMGs in expressed in the reference frame of the distributed mass.
Our $\tau_{Z}$ is aligned with the link and therefore with the axis of rotation for $\theta_{23}$, ergo having no impact on $\ddot{\theta}_{2[12]}$.
To obtain $\ddot{\theta}_{2[12]}$ we first transform $\tau_{[XY]}$ into the reference frame $XYZ_2$ using the inverse of the rotation used above.
The results are then projected onto $X_2$ and $Y_2$ to obtain $\ddot{\theta}_{22}$ and $\ddot{\theta}_{22}$ respectively.
Once again note the sign change for $\theta_{21}$.

\begin{align}
R_{3 \rightarrow 2} = & R_{2 \rightarrow 3}^T \\
\operatorname{det}R^T_{3 \rightarrow 2} = & 1 \text{, making it a valid rotation} \\
\tau^{XYZ_{2}}_{XY} 
  = & R_{3 \rightarrow 2}
    \begin{bmatrix}
      \tau_{X} \\ 0 \\ 0
    \end{bmatrix} +
  R_{3 \rightarrow 2}
    \begin{bmatrix}
      0 \\ \tau_{Y} \\ 0
    \end{bmatrix} \\
\ddot{\theta}_{21}' = & \ddot{\theta}_{21} - \tau^{XYZ_{2}}_{XY} 
    \begin{bmatrix}
      0 \\ 1 \\ 0
    \end{bmatrix} \cdot I_{YY}^{-1} \\
\ddot{\theta}_{22}' = & \ddot{\theta}_{22} + \tau^{XYZ_{2}}_{XY} 
    \begin{bmatrix}
      1 \\ 0 \\ 0
    \end{bmatrix} \cdot I_{XX}^{-1} \\
\ddot{\theta}_{23}' = & \ddot{\theta}_{23} + \tau_{Z} 
\end{align}

The application of the CMG torques can then be added to the model as follow.
Note how this encompasses _all_ torques produced by the CMG, thereby cleanly separating the crane and CMG models easing their respective developments.

\begin{align}
\ddot{\theta}_{21}' = & \ddot{\theta}_{21} - \left(
      \tau_{X} \left(-\sin{\theta_{21}} \sin{\theta_{22}} \sin{\theta_{23}}
                     + \cos{\theta_{21}} \cos{\theta_{23}}\right)
      + \tau_{Y} \left(\sin{\theta_{23}} \cos{\theta_{22}} \right )
      \right)\\
\ddot{\theta}_{22}' = & \ddot{\theta}_{22} + \left(
      \tau_{X} \left( - \sin{\theta_{21}} \sin{\theta_{22}} \cos{\theta_{23}}
                      - \sin{\theta_{23}} \cos{\theta_{21}} \right )
      + \tau_{Y} \left ( \cos{\theta_{22}} \cos{\theta_{23}} \right )
      \right )\\
\ddot{\theta}_{23}' = & \ddot{\theta}_{23} + \tau_{Z} 
\end{align}

With the torques covered, let us move to the forces.
This entails the forces from the robots motion, process forces or things such as wind.
To include the forces we must know the center of percussion or our lower pendulum link, as reaction of the system depends on where the force acts in relation to said center.
The center of percussion is the point on a pendulum where perpendicular force leads to zero reaction force at its pivot point, due to the angular and translational acceleration cancelling out (see @Fig:center-of-percussion)
For a very good explanation of this I recommend the wikipedia article [@CenterPercussion2018].
So depending on the position of the acting force and the center of percussion the force acting upon the lower link with result in a ratio of angular acceleration of the lower link and a force acting upon the pivot between the upper and the lower link.
This force will then result in an angular acceleration of the upper link.
As of this writing this has not been included in our model of the double pendulum.

![Illustration of the center of percussion and how it relates to the reaction of a pendulum given the location of a force acting upon it. CC-BY-SA 4.0, Wikipedia user Qwerty123uiop](./figures/center-of-percussion.png){ #fig:center-of-percussion }

## Payload Inertia

The payload inertia is of relevance to all of our applications.
For our models we will therefore create a set of example inertia that follow the parameter space set forth by our selected example cranes.

For each crane we will model a slab of concrete whose weight matches the maximum load of the the crane.
The proportions of the slabs will be constant.
Let us assume the density of concrete as 2,400 kg/m$^3$ and the slab proportions as 5, 0.1, 2 in X, Y, Z respectively.
Since the center of gravity of the payload wont lie in the point of rotation (the hook) we assume an offset equal to the size in Z.
Using the parallel axis theorem this gives us the inertia listed in @Fig:inertia-data.

![Example payload inertia assuming constant density (2,400 kg/m^3), proportions (5, 0.1, 2) and with a weight stemming from the max load of the associated crane. We also assume the CoG to be offset by the Z-size from the point of rotation.](./figures/inertia-data.png){ #fig:inertia-data }

## Process Torques and Forces

Given the initial motivation of this work to hang a robot from a crane, we use a robot as the model for a process generating torques and forces to be compensated by the CMGs.
Since a robot is a generic motion provider than can provide a wide set of movements, we create several paths in an attempt to create a representative set.
These paths are:

- random motion in a plane below the robot
- vertical rectangle next to the robot
- points next to the robot incl. approach and retraction

See @Fig:robot-toolpaths for animations of the toolpaths.
These should roughly correspond to positioning/compensation, a continuous task (e.g. spray-painting) and a joining task (e.g. nail gun) respectively.
The tasks were programmed using the Rhino/Grasshopper plugin KUKA|prc for a small KUKA KR industrial robot (see @Fig:robot-path-planning).
Since the programs are parametric one can easily scale them to larger robots.

![KR3 Robot used to obtain realistic axis values.](./figures/KR3.jpg){#fig:kr3}

\todo{replace KR3 picture with our own KR3}

The KUKA|prc plug-in can output the required axis values for a programmed path .
This inverse kinematic simulation is useful for solving singularity issues in the paths but does not limit the axis accelerations.
This is obvious when looking at the axis values produced by KUKA|prc in @Fig:robot-axis-values, which have very sharp corners where the robot changes direction.

While more realistic robot simulation packages exist, for our project we can simply use real axis values.
These can be easily obtained using the mxA functionality of the plugin-in, mxA being a UDP based interface for KUKA controllers.
With mxA we can stream the robot path to the controller and receive back the actual axis values.
By recording these with a time stamp we can use them as input for a multi-body simulation.

The multi-body simulation is set up using the Simmechanics package in Simulink.
The CAD files from the robot manufacturer are imported in to SolidWorks and rotational joints programmed into the assembly.
From this a Simmechanics file can be exported and adapted to receive the recorded axis values and output the torques and forces experienced at the robot base (see @Fig:kr3-simmechanics).
The inertia of the robots axes are estimated by distributing the robots mass according the volume of each axis and assumes a homogeneous density of the robot.

![Three robot paths used in our experiments.](./figures/robot-toolpaths.gif){#fig:robot-toolpaths}

![Parametric robot paths programmed using the KUKA|prc plugin for Rhino/Grasshopper.](./figures/robot-path-planning.jpg){#fig:robot-path-planning}

![Axis values simulated by KUKA|prc. Note the sharp corners resulting from unlimited acceleration/jerk values making these values ill-suited to simulate the forces and torques at the robot base.](./figures/kuka-prc-axis-values.jpg){#fig:robot-axis-values}

![Body simulation of the KR3. The masses of the axes have been estimated from the total mass of the robot and the volume of the respective axes.](./figures/kr3-simmechanics-vis.png){ #fig:kr3-simmechanics }
