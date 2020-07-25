
# Modeling the Crane-CMG Application Systems

> "The problem is, we don't understand the problem." -- Paul MacCready

Two types of models are needed to develop sizing guidelines for the crane-CMG system.
Their goals are, respectively: 

1. derivation of abstracted inputs to the sizing
2. simulation of the designed system

Simulations of the system are needed to not only validate the sizing, but also to understand the system behaviour.

The models need to cover three application scenarios for the CMG-crane system:

1. compensation of process torques
2. rotation of loads being lifted by the crane
3. dampening of the pendulum motion of the crane

Overall these models should thereby provide the means to abstract crane parameters to assist in the sizing of the CMGs.
The requirements of the processes e.g. part rotation and robot motion also need to be obtained.
Then, to link crane and application, a suitable model of the CMG system is required.

To understand the basic input parameters technical data provided by crane manufacturers is used.
The process loads produced by a robot will be determined using real robot motions and a multi-physics simulation package.
To understand the interaction of a CMG array with a crane it is modeled as a double pendulum system.
The formulation of CMG dynamics (see @Sec:cmg-dynamics) is applied to this model.
Finally an interface for the application of external forces is created.

## Parameter Space of Construction Cranes { #sec:crane-params }

Tower cranes play a central role in contruction.
This work therefore focusses on the parameter space of tower cranes.
@Fig:lbc-cranes shows a selection of tower cranes manufactured by Liebherr.
Going from the compact, bottom-slewing crane, to one of the highest load cranes, two intermediate steps are also considered

![Cranes used to estimate parameter space of construction cranes. From left to right (increasing payload): L1-24, 71 EC-B, 380 EC-B, 1000 EC-B. ](./figures/cranes.png){ #fig:lbc-cranes short-caption="Cranes used to estimate parameter space of construction cranes"}

![Key parameters of the selected example cranes L1-24, 71 EC-B, 380 EC-B, 1000 EC-B.](./figures/crane-data.png){ #fig:crane-data short-caption="Key parameters of selected sample cranes"}

From the data-sheets of these cranes the parameters relevant to the models can be obtained(see @Fig:crane-data).
The parameters that enable an estimation of the base rate of the CMGs induced by the motion of the crane are of particular interest, as this determines the magnitude of the gyroscopic reaction torque that the gimbal motors need to compensate (see @Sec:cmg-dynamics).
The translational movements of the hook/platform do not contribute to the base rate, but the period of the crane-rope/pendulum is of interest.
Since the period of a pendulum depends on the length of the pendulum, the hook height is used as stand-in for the (maximum) pendulum length.

The oscillations of a crane tendon can be assumed to be sufficiently small to assume isochronism i.e. that the frequency remains constant while the amplitude changes.
Whilst neither the amplitude of the oscillation nor the mass of the pendulum affect the frequency of the oscillation, they do affect the maximum angular velocity.
It is possible to grasp this intuitively, if one considers the potential and kinetic energy of a pendulum.

In the zero crossing where the pendulum is aligned with gravity the potential energy is zero while the kinetic energy and hence the velocity is highest (see @Fig:pendulum-velocity)
When the pendulum is at its highest points, the inverse is true.
As the potential energy is dependent upon the mass of the pendulum, the maximum payload of the cranes is added to the parameter list.

![Illustration of the velocity and acceleration of a pendulum. CC-BY-SA, Wikipedia User Ruryk](./figures/oscillating_pendulum-ccbysa-ruryk.gif){ #fig:pendulum-velocity short-caption="Illustration of velocity and acceleration of a pendulum"}

An estimate of the amplitude of the crane oscillations can be derived from the maximum crane load, pendulum length and translational velocity caused by slewing the jib or moving the trolley.
To determine the translational velocity caused by slewing, the jib length i.e. reach of the crane and the maximum load at the tip of the jib are also required:

\begin{align}
v_{trolley} =& N_T / 60 \\
v_{jib} =& N_R \frac{2\pi r}{60} \\
\omega =& v \cdot l \\
h_{\text{max}} =& \frac{mv^2}{2mg} \\
\theta_{\text{max}} =& \cos{^-1}\left ( \frac{l-h_{\text{max}}}{l} \right )
\end{align}

With $v$ being the translational speed of the hook, $N_T$ the trolley speed in m/min, $N_R$ the jib's rotational speed in rpm, $r$ the reach of the jib, $\omega=\dot\theta$ the angular velocity of the pendulum i.e. base rate of the hook, $l$ the length of the pendulum, $h$ the elevation of the hook relative to its lowest position and $\theta$ the angle of the pendulum.

![Base rates and maximum excitation of the selected example cranes L1-24, 71 EC-B, 380 EC-B, 1000 EC-B from the above derivations.](./figures/crane-base-rates.png){ #fig:crane-base-rates short-caption="Base rates and max. excitation of sample cranes"}

Note that all of the above assume a regular pendulum.
As will be seen in the following section, it can be necessary to model the crane as a double pendulum.
In such models, the hook and payload would be considered as separate masses.
Note that some hooks are purposely heavy to overcome the rope-drag of the crane pulley when no load is attached.

The estimations derived here provide a worst case oscillation which is most likely in excess of physical oscillations in practice.
The maximum values obtained above stem from a case where the crane is lifting the maximum load possible at the tip of the jib with the load at ground level.
With such a load, the cranes rotates at maximum velocity and then stops completely.

## Modeling the Crane

Whilst a CMG model will always have to be three-dimensional due to the rotation of the vectors involved, when it comes to cranes a 2D model will be presented before moving on to 3D models.
A 2D model is not only easier to develop, but more importantly also easier to visualize, plot and understand.
While simpler, it still helps to illustrate critical parts of the crane’s behavior and to develop control approaches.
Often the insights from a lower dimensional model can help in the design of the higher dimensional ones.

For this case a 3D SPCMG model can be attached to a 2D crane, as the SPCMG produces its torque around a fixed axis.
This illustrates the basic principles of the CMGs as they interact with the crane, while keeping the model relatively simple.
It is also possible to study the effect of process torques and forces by constraining them to the 2D case.

This simplification was carried over to the hardware prototype.
By building the crane as a swing that hangs from two diagonally spanned ropes, the motion can be mostly constrained to a single plane (see @Fig:prototype-sketch).

![Sketch of the hardware prototype. The way it is suspended should ensure as close to 2D a motion as possible without having to resort to rigid links and large bearings.](./figures/prototype-sketch.svg){ #fig:prototype-sketch short-caption="Sketch of the hardware prototype"}

The essence of a crane, a hook/load hanging from a rope, is a pendulum.
However, in contrast to the basic point mass pendulum, a crane has several important differences.
Most importantly the suspension point of the rope exhibits its own dynamics, causing excitation of the pendulum.
These can stem from controlled movement of the trolley, jib or gantry but beyond this the entire crane structure often exhibits significant flex.
Then the rope itself might actually be a set of ropes, is not rigid and also stretches under load.
The load hanging from the hook of a crane is also often so large that it possesses significant inertia, leading to its own set of dynamic behavior that interacts with the crane.
And finally, of course, there are external forces such as wind as well as drag and other dampening behavior.

This work makes several choices regarding what to include in the model.
As the CMG acts on the crane by exerting torque on its payload, it is necessary to model the payload/CMGs as an additional distributed mass hanging from the crane.
One of the applications is the dampening of pendulum motion of the crane.
While this is most often induced by crane motions, nevertheless the pendulum’s suspension point will not be modeled as movable.
Instead the assessment of the dampening capabilities will induce a pendulum motion through the initial conditions.
The dynamics of the crane structure itself as well as the flexibility of the crane’s rope will also be ignored at this stage.

### Review of Available Crane Models

A review of the existing crane models (see [@Abdel-RahmanDynamicsControlCranes2003] for a review until 2003) supplies a large variety of models that focus on different aspects or crane types.
It should be possible to copy, mix and adapt these to create a model suited for the current purpose.
It also means that this CMG-focused model could be extended relatively easily.
The following sections will develop this model from a two-dimensional double pendulum to a three-dimensional double pendulum and subsequently go from two point masses to a point mass and a distributed mass.

The @Fig:crane-model-overview illustrates how the various parts of the crane, CMG, robot and load correspond to the parts of the model.
The model ignores motion of the crane's gantry/jib, and therefore the pendulum is suspended from a fixed point.
The upper mass is a point mass that includes the mass of the hook and crane rope.
The lower mass is a distributed mass that includes the CMGs, their platform and everything attached to it e.g. robot, load and other kinematics.

![Correspondence of crane/CMG/load components to the model.](./figures/crane-model-overview.png){ #fig:crane-model-overview short-caption="Correspondance of crane/CMG/load to model"}

The generation of equations of motion and subsequent numerical integration are achieved using Python.
The code builds on the educational example of Christian Hill [@HillLearningScientificProgramming2016] [^hillwebsite], the three-dimensional model extends the work of O'Connor and Habibi [@OConnorGantryCraneControl2013].

[^hillwebsite]: Also available at his [website](https://scipython.com/).

This work envisions that the developed model can be extended by others, not necessarily coming from engineering backgrounds.
As such the following sections and appendix offer an extended discussion and the full source code.

### 2D Double Pendulum { #sec:2dpendulum }

This section uses the most basic double pendulum (massless rods with point masses, @Fig:pm-double-pendulum) as a starting point.
For this the equations of motion are commonly known, see e.g. [@HillLearningScientificProgramming2016]:

![2D double pendulum as point masses on rigid, massless rods.](./figures/2d-pendulum.png){ #fig:pm-double-pendulum short-caption="2D double pendulum with rigid, massless links"}

The Langrangian ($\mathcal{L} = KE - PE$) is the balance of potential energy (PE) and kinetic energy (KE) that describes our system:

\begin{align}
\mathcal{L} = & \tfrac{1}{2}(m_1+m_2)l_1^2\dot{\theta}_1^2 + \tfrac{1}{2}m_2l_2^2\dot{\theta}_2^2 + m_1l_1l_2\dot{\theta}_1\dot{\theta}_2\cos(\theta_1 - \theta_2) \\
& + (m_1+m_2)l_1g\cos\theta_1 + m_2gl_2\cos\theta_2
\end{align}

From the Lagrangian the following equations of motion can be obtained using the Euler-Lagrange Equations [^lagrangian].
This step can be performed using computer algebra systems (see code in  @Sec:2d-pointmass-eom).

[^lagrangian]: See the [Wikipedia entry](https://en.wikipedia.org/wiki/Euler%E2%80%93Lagrange_equation) and [lectures](https://www.youtube.com/watch?v=4uJaKJASKnY&list=PLX2gX-ftPVXWK0GOFDi7FcmIMMhY_7fU9) by Michel van Biezen for a deeper introduction.

\begin{align}
0 = & \frac{\mathrm{d}}{\mathrm{d}t}\left(\frac{\partial\mathcal{L}}{\partial \dot{q}_i}\right) - \frac{\partial \mathcal{L}}{\partial q_i} \\
\ddot{\theta}_1 = & \frac{{m_2g\sin\theta_2\cos(\theta_1-\theta_2) - m_2\sin(\theta_1 - \theta_2)(l_1\dot{\theta}_1^2\cos(\theta_1 - \theta_2) + l_2\dot{\theta}_2^2)}{ - (m_1+m_2)g\sin\theta_1}}
    {l_1(m_1 + m_2\sin^2(\theta_1-\theta_2))}  \\
\ddot{\theta}_2 = & \frac{{(m_1+m_2)(l_1\dot{\theta}_1^2\sin(\theta_1-\theta_2) - g\sin\theta_2}{ + g\sin\theta_1\cos(\theta_1-\theta_2))+m_2l_2\dot{\theta}_2^2\sin(\theta_1-\theta_2)\cos(\theta_1-\theta_2)}}{l_2(m_1 + m_2\sin^2(\theta_1-\theta_2))}
\end{align}

When these are solved through numerical integration (see code in @Sec:2d-pointmass-eom) the familiar chaotic motion is obtained, see @Fig:chaotic-dp.

![Chaotic motion of a double pendulum.](./figures/double_pendulum.gif){ #fig:chaotic-dp short-caption="Chaotic motion of a double pendulum"}

In the crane-CMG scenario, angles and velocities sufficient to create such motion outside of catastrophic failure events should not be encountered.
Nevertheless the double-pendulum makes sense as a basis for the models for several reasons:

- large payloads and their motions
- CMGs control motion by exerting torque

The first point is obvious, but requires the extension of the model from a point mass to a distributed mass model (at least for the second mass i.e. the payload/CMG platform/robot).
This will be covered in a later section since the stabilization and controlled movement of payloads is one of the goals of this work.

The second point can be illustrated by the point mass model.
In @Fig:dp-oscillations-animation and @Fig:dp-oscillations it can be seen how for small angles and velocities the double pendulum’s position is close to that of a regular pendulum.
However, the interaction between the two parts of the pendulum can be seen by looking at the velocity and especially the accelerations.
The impact of the lower pendulum can be expected to increase as the move is made to a distributed mass.
As the CMGs exert torque on their platform, this impact of the lower link on the upper link will have an even greater effect.

![Oscillations of a double pendulum at small angles and velocities.](./figures/dp-oscillations-animation.gif){ #fig:dp-oscillations-animation short-caption="Oscillations of double pendulum at small angles"}

![Oscillations of a double pendulum at small angles and velocities showing a) how the position for such parameters comes close to a simple pendulum and b) how the two parts of the pendulum interact.](./figures/dp-oscillations.svg){ #fig:dp-oscillations short-caption="Oscillations of double pendulam at small angles (plot)"}

Until now the model has been using a point mass for both links.
When the lower mass is replaced with a distributed mass, it is necessary to add a term to the kinetic energy to capture the rotational energy of the moving mass:

\begin{equation}
KW_{\omega} = \tfrac{1}{2} I \omega^2
\end{equation}

Since the point of rotation does not lie in the center of mass of our distributed mass (picture the platform hanging below the hook), the rotational inertia is not simply that of the mass.
Instead the parallel axis theorem also known as Huygens-Steiner theorem must be applied:

\begin{equation}
I = I_{CoM} + mr^2
\end{equation}

With $I_{CoM}$ being the inertia of the mass around its center of mass, $r$ the distance from this center of mass to the axis of rotation and $m$ the mass of our object.
These extensions are implemented in @Sec:2d-distmass-eom.

### The 3D Model { #sec:3d-pendulum }

![Model of a point mass double pendulum in three dimensions with a fixed point of suspension.](./figures/crane-spherical.png){ #fig:crane-spherical short-caption="Point mass double pendulum in three dimensions"}

If the point mass model is extended to three dimensions, two angles are required to describe the location of each point.
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

With this conversion the Langrangian can once again be formulated from the kinetic and potential energies:

\begin{align}
PE = & m_1 \cdot g \cdot z_1 + m_2 \cdot g \cdot z_2 \\
KE = & ^1/_2 \cdot m_1 \cdot \dot{x}_1^2 + \dot{y}_1^2 + \dot{z}_1^2 \\
     & + ^1/_2 \cdot m_2 \cdot \dot{x}_2^2 + \dot{y}_2^2 + \dot{z}_2^2  \\
\mathcal{L} = & KE - PE
\end{align}

From this the Euler-Lagrange equations for $\theta_{ij}$ can be obtained and subsequently solved for $\dot{\theta}_{ij}$.
Given their complexity, this is done using a computer algebra system.
See appendix @Sec:3D-pointmass-eom for the resulting equations and SymPy code used to obtain them.

The use of spherical coordinates to describe the kinematic constraints of the system leads to numerical issues during simulation.
The issues arise due to the fact that the same coordinates can be arrived at by rotating the azimuthal angle by 180° while also flipping the sign of the polar angle (@Fig:3d-model-angle-issues).
While such jumps do not cause issues regarding the position of the pendulum, the spikes in angular velocity represent the kinetic energy in the system incorrectly.
The effect of this can vary depending on the excitation/initial conditions of the simulation (see @Fig:2D-3D-comparison-large-excitation-spherical and @Fig:2D-3D-comparison-small-excitation in the appendix).

![3D double pendulum using spherical coordinates under small 2D excitation illustrating the issues of the use of spherical coordinates. Note how $\theta_{i2}$ jumps in steps of 180° causing $\theta_{i1}$ to remain negative. It also causes the spikes in angular velocity. These cause an erroneous dampening of the pendulum.](./figures/3d-model-angle-issues.svg){ #fig:3d-model-angle-issues short-caption="Issues with spherical coordinates in double pendulum model"}

To alleviate this, the description of the kinematic constraints can be changed to use projected angles instead of spherical coordinates.
This approach follows that of [@OConnorGantryCraneControl2013], where the authors derive the equations of motion for a double pendulum with an attached distributed mass that has two degrees of rotational freedom.
The following extends this to a full three degrees of freedom (see @Fig:crane-projected-angles), not only to model realistic crane load motion more closely but also to accommodate the load rotation use-case.

![Model of a double pendulum in three dimensions with a fixed point of suspension and using projected angles instead of spherical coordinates. Note that the lower mass is now a distributed mass with three degrees of rotational freedom, while the upper mass is still a point mass with only two rotational degrees of freedom.](./figures/crane-projected.png){ #fig:crane-projected-angles short-caption="Double pendulum in three dimensions using projected angles"}

With the use of projected angles the cartesian expressions become:

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

Assuming a point mass pendulum, the Langrangian would be the same as before:

\begin{align}
PE = & m_1 \cdot g \cdot z_1 + m_2 \cdot g \cdot z_2 \\
KE = & ^1/_2 \cdot m_1 \cdot \dot{x}_1^2 + \dot{y}_1^2 + \dot{z}_1^2 + \\
     & ^1/_2 \cdot m_2 \cdot \dot{x}_2^2 + \dot{y}_2^2 + \dot{z}_2^2  \\
\mathcal{L} = & KE - PE
\end{align}

Since the intention is to model the lower mass (the platform and load) as a distributed mass, the kinetic energy of the rotating mass has to be added to the Langrangian.
For this it is necessary to express the rotational velocities and inertia of the mass in a common reference frame.
This is defined as the center of gravity, hanging a distance $l_2$ from our point mass $m_1$.
Should the center of gravity change due to e.g. robot motion, this difference will be modeled as an external torque acting upon the platform.
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

The rotations required to transform the reference frame $X_2Y_2Z_2$ that is aligned with the world axes to the reference frame $X_3Y_3Z_3$ also enable the rotational velocities $\omega_{X_3Y_3Z_3}$ to be obtained from the projected angle velocities $\dot{\theta}_{2j}$.

![Sequence of rotations to transform the world aligned reference frame to the reference frame of the distributed mass.](./figures/cog-rotations.png){ #fig:cog-rotations short-caption="Sequence of rotations for distributed mass reference frame"}

The rotations illustrated in @Fig:cog-rotations can be expressed as:

\begin{align}
R_{2 \rightarrow 3} = & R_Y(\theta_{21})R_X(\theta_{22})R_Z(\theta_{23}) \\
= &
\left[\begin{matrix}\cos{\left (\theta_{21} \right )} & 0 & - \sin{\left (\theta_{21} \right )}\\0 & 1 & 0\\\sin{\left (\theta_{21} \right )} & 0 & \cos{\left (\theta_{21} \right )}\end{matrix}\right]
\left[\begin{matrix}1 & 0 & 0\\0 & \cos{\left (\theta_{22} \right )} & - \sin{\left (\theta_{22} \right )}\\0 & \sin{\left (\theta_{22} \right )} & \cos{\left (\theta_{22} \right )}\end{matrix}\right]
\left[\begin{matrix}\cos{\left (\theta_{23} \right )} & - \sin{\left (\theta_{23} \right )} & 0\\\sin{\left (\theta_{23} \right )} & \cos{\left (\theta_{23} \right )} & 0\\0 & 0 & 1\end{matrix}\right]
\end{align}

Thus the required rotational velocities can be expressed as follows.
Note that  -$\theta_{21}$ is used, as its rotation direction runs counter to the right-hand rule.

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

The equations of motion can then once again be obtained using a computer algebra system.
Since the 3D plotting of Matplotlib is slightly limited, the following animation is made using Rhino/Grasshopper (@Fig:sim-gh).
For this the state-vectors of the simulation are transformed to cartesian points for the masses as well as an X and Y vector for the reference frame of our mass.
See the appendix (@Sec:distributed-mass-eom) for equations of motion and code.

![Visualization of simulated 3D double pendulum with the lower mass as a distributed mass. The lower mass begins with a small angular velocity around the link axis. Visualized using Rhino/Grasshopper.](./figures/gh-screenrecording.gif){ #fig:sim-gh short-caption="Animation of distributed mass, 3D double pendulum"}

This process can be continued to add further aspects such as wind or a movable point of suspension.
The following section covers how such aspects can be added relatively easily by modifying the state of the system.
Other aspects such as a movable point of suspension would require a new Langrangian, as they introduce new terms to the kinetic or potential energy.

An alternative would be to use multi-body simulation tools as are available in Modelica or Simulink.
Here, individual blocks that contain e.g. a distributed mass or a rotary joint can be connected with each other (see @Fig:modelica-example).

![Rudimentary implementation of this model in Modelica. Note that this lacks connections to input torque from the CMGs and uses a different angle description.](./figures/modelica-example.gif){ #fig:modelica-example short-caption="Rudimentary double pendulum in Modelica"}

## Adding External Torques

The torques and forces acting upon the system cannot be included in the above Langrangian as energies, instead they must be added as source terms to the resulting equations of motion.

The torque generated by the CMGs ($\tau$) changes the angular acceleration of the lower link depending on its moment of inertia.
For the two-dimensional model, the necessary modifications to the equations of motion are straightforward:

\begin{align}
\ddot{{\theta}'}_1 = & \ddot{\theta}_1 \\
\ddot{{\theta}'}_2 = & \ddot{\theta}_2 + \frac{\tau}{m_2 l_2^2}
\end{align}

The three-dimensional model is slightly more complex due to the choice of angles.
The torque produced by the CMGs is expressed in the reference frame of the distributed mass.
The torque $\tau_{Z}$ is aligned with the link and therefore with the axis of rotation for $\theta_{23}$, ergo having no impact on $\ddot{\theta}_{2[12]}$.
To obtain $\ddot{\theta}_{2[12]}$ first $\tau_{[XY]}$ is transformed into the reference frame $XYZ_2$ using the inverse of the rotation used above.
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

The application of the CMG torques can then be added to the model as follows.

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

This encompasses _all_ torques produced by the CMG, thereby cleanly separating the crane and CMG models and simplifying their respective development.

## Adding External Forces { #sec:external-forces }

Following the above description of the torques, the forces will now be described.
These comprise the forces from the robot's motion, process forces or disturbances such as wind.
Given the way the equations of motion are constructed around the angular motion of the links, the external forces need to be translated into torques.
Subsequently they can be added to the other external torques.

A force acting on a pendulum will cause both a translational acceleration of its center of mass as well as a rotational acceleration around it.
The magnitude of the translational acceleration depends on the force and mass of the pendulum.
The rotational acceleration also depends on where the force is acting in relation to the center of mass.
This leads to the interesting phenomenon of the center of percussion.
This being the point on a pendulum where a perpendicular force leads to zero reaction force at its pivot point, due to the angular and translational acceleration cancelling each other out (see @Fig:center-of-percussion) [^center-of-percussion].

[^center-of-percussion]: For further reading the [wikipedia article](https://en.wikipedia.org/wiki/Center_of_percussion) offers an excellent explanation of this phenomenon.

![Illustration of the center of percussion and how it relates to the reaction of a pendulum given the location of a force acting upon it. CC-BY-SA 4.0, Wikipedia user Qwerty123uiop](./figures/center-of-percussion.png){ #fig:center-of-percussion short-caption="Illustration of the Center of Percussion"}

In this case, where a double pendulum is being used, this means that there is an additional torque acting upon the lower link that depends on the force and its distance to the center of mass of the lower link.
The force acts on the pivot point of the lower link and thereby on the upper link.
Here it once again results both in an angular as well as translational acceleration.
As the pivot of the upper link is assumed to be fixed and is connected by a rope, the translational acceleration has no impact.
So for the 2D model the equations of motion can be extended as follows:

\begin{align}
\ddot{{\theta}'}_1 = & \ddot{\theta}_1 + \frac{F_{1x} l_1}{m_1 l_1^2}\\
\ddot{{\theta}'}_2 = & \ddot{\theta}_2 + \frac{\tau + F_{2x} b}{I_2}
\end{align}

$b$ being the distance between the force $F_{2x}$ and the center of mass of the lower link.
The moment of inertia for the upper link is written explicitly, as it is always modeled as a point mass.
The moment of inertia for the lower link depends on whether it is being modeled as a point or distributed mass.

Defining the external force as acting in the reference frame of the lower link, the forces $F_{1x}$ and $F_{2x}$ are the components of the external force that act perpendicular to the respective links.
The force acting upon the upper link is then dependent upon $\theta_1$ and $\theta_2$ (@Fig:external-forces):

\begin{equation}
F_{1x} = F_{2x} \cos(\theta_1 + \theta_2) + F_{2y} \sin(\theta_1 + \theta_2)
\end{equation}

It is important to note that the forces acting upon the system due to gravity are already taken into account by the equations of motion derived from the Langrangian.

![Illustration of the external force acting upon the 2D model](./figures/external-forces.png){ #fig:external-forces short-caption="External forces acting upon 2D model"}

## Payload Inertia

The payload inertia is of relevance to all three applications previously outlined.
For the models a set of example inertia derived from the parameter space set forth by the selected example cranes will therefore be created (see @Sec:crane-params).

For each crane a slab of concrete will be modeled, the weight of which matches the maximum load of the crane.
The proportions of the slabs will be constant at 5, 0.1, 2 in X, Y, Z respectively.
The density of concrete is assumed to be 2,400 kg/m$^3$.
Since the center of gravity of the payload will not lie in the point of rotation (the hook), the following assumes an offset equal to the size in Z.
Using the parallel axis theorem, this results in the inertia listed in @Fig:inertia-data.

![Example payload inertia assuming constant density (2,400 kg/m$^3$), proportions (5, 0.1, 2) and a weight stemming from the max load of the associated crane. It is also assumed that the CoG is to be offset by the Z-size from the point of rotation.](./figures/inertia-data.png){ #fig:inertia-data short-caption="Example payload inertias"}

## Process Torques and Forces

Given the initial motivation of this work to stabilize an industrial robot hanging from a crane, a six-axis serial link robot is used as the model for a process generating torques and forces to be compensated by the CMGs.
Since a robot is a generic motion provider that can provide a wide set of movements, several paths were created in an attempt to provide a representative set.
These paths are:

- random motion in a plane below the robot
- vertical rectangle next to the robot
- points next to the robot incl. approach and retraction

See @Fig:robot-toolpaths for animations of the toolpaths.
These should roughly correspond to positioning/compensation, a continuous task (e.g. spray-painting) and a joining task (e.g. nail gun) respectively.
The tasks were programmed using the Rhino/Grasshopper plugin KUKA|prc for a small KUKA KR3 R540 industrial robot (see @Fig:robot-path-planning).
Since the programs are parametric they can easily be scaled to larger robots.

The KUKA|prc plug-in can output the required axis values for a programmed path.
This inverse kinematic simulation is useful for solving singularity issues in the paths but does not limit the axis accelerations.
This is obvious when looking at the axis values produced by KUKA|prc in @Fig:robot-axis-values, which have very sharp corners where the robot changes direction.

While more realistic robot simulation packages exist, for this project real axis values can be used to simplify matters.
These can be obtained using the mxAutomation option of the plugin-in, mxAutomation being a protocol intended for interfacing programmable logic controllers (PLC) with KUKA controllers.
The KUKA|prc software uses this protocol via UDP over a conventional Ethernet connection with the controller.
Using mxAutomation, the robot path can be streamed to the controller and actual axis values are sent back.
Time-stamped recordings of these can be used as input for a multi-body simulation.

The multi-body simulation is set up using the Simmechanics package in Simulink.
The CAD files from the robot manufacturer are imported into SolidWorks and rotational joints added to the assembly.
From this a Simmechanics file can be exported using the export plug-in provided by Mathworks and subsequently adapted to receive the recorded axis values and output the torques and forces experienced at the robot base (see @Fig:kr3-simmechanics).
The inertia of the robot's axes are estimated by distributing the robot’s mass according the volume of each link, which assumes a homogeneous density of the robot.

![Three robot paths used in these experiments.](./figures/robot-toolpaths.gif){#fig:robot-toolpaths short-caption="Example robot paths for experiments"}

![Parametric robot path programmed using the KUKA|prc plugin for Rhino/Grasshopper.](./figures/robot-path-planning.jpg){#fig:robot-path-planning short-caption="Parametric robot path programming in KUKA|prc"}

![Axis values simulated by KUKA|prc. Note the sharp corners resulting from unlimited acceleration/jerk values making these values ill-suited to simulate the forces and torques at the robot base.](./figures/kuka-prc-axis-values.jpg){#fig:robot-axis-values short-caption="Axis values simulated by KUKA|prc"}

![Body simulation of the KR3. The masses of the axes have been estimated from the total mass of the robot and the volume of the respective axes.](./figures/kr3-simmechanics-vis.png){ #fig:kr3-simmechanics short-caption="Body simulation of robot in SimMechanics"}
