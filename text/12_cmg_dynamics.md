
# Theory of CMGs {#sec:cmg-theory}

This chapter covers various theoretical aspects of CMGs, starting with their dynamics.
Subsequently a brief introduction is given regarding their steering, workspaces and sizing.
The content of this chapter covers existing models and approaches, laying the groundwork for the following chapters that develop these aspects for the CMG-crane system.

## Dynamics of CMGs {#sec:cmg-dynamics}

With the number of spinning parts involved in a CMG, the dynamics exhibit a certain complexity.
To be able to size and control the CMGs for our application we need to understand and model these dynamics.
This section will therefore introduce and discuss the model derived in great detail by Leve et al. [@LeveSpacecraftMomentumControl2015, ch. 4.5].
The resulting expression is the derivative (with respect to time) of the angular momentum of a CMG spacecraft with variable speed gyro-rotors [@LeveSpacecraftMomentumControl2015, eq. 4.81]:

\begin{eqnarray}
\frac{^N\text{d}\mathbf{H}}{\text{d}t} &=&
\mathbf{J} \cdot
\frac{^B\text{d}\mathbf{\omega}^{B/N}}{\text{d}t} \\
&+&
\left(
\sum^{n}_{i=1} J_{g,i} \ddot{\delta}_i \mathbf{\hat{g}}_i +
J_{r,i}
 \left(
  \dot{\Omega}_{r,i}
  \mathbf{\hat{s}}_i +
  \dot\delta_i \Omega_{r,i} \mathbf{\hat{o}}_i
 \right)
\right) \\
&+&
\mathbf{\omega}^{B/N} \times
\left(
\mathbf{J} \cdot
\mathbf{\omega}^{B/N} +
 \left(
 \sum^n_{i=1} J_{g,i} \dot{\delta}_i \mathbf{\hat{g}}_i +
 J_{r,i} \Omega_{r,i} \mathbf{\hat{{s}}}_i
 \right)
\right)
\end{eqnarray}

Leve et al. use vector-dyadic notation [@LeveSpacecraftMomentumControl2015, sec. 4.1] for the above equations.
For a basic understanding it is best to disregard the dyadic notation, summations etc. and focus on the following symbols:

- $\mathbf{H}$: angular momentum of the spacecraft
- $\mathbf{\omega}$: angular velocity of the spacecraft
- $\mathbf{J}, J_r, J_g$: inertia of spacecraft, gyroscope rotor and inner gimbal assembly
- $\mathbf{\hat{s}, \hat{g}, \hat{o}}$: axis of the rotor, gimbal and output torque[^outputtorque]
- $\dot{\delta}, \ddot{\delta}$: angular velocity and acceleration of the gimbal
- $\Omega$: angular velocity of the gyroscopes rotor

[^outputtorque]: $\mathbf{\hat{o}} = \mathbf{\hat{g}} \times \mathbf{\hat{s}}$

Using this simplified notation let us look at the various parts contributing to the changes in angular momentum (for an exact discussion please refer to [@LeveSpacecraftMomentumControl2015, sec. 4.5]):

1. __Rigid-Body Motion:__ all terms involving $\mathbf{J}$
2. __Gyroscopic Reaction Torques:__   
   Caused by either the motion of the spacecraft or gimbal rotating an angular momentum vector.
   a. $J_r \Omega \dot{\delta} \mathbf{\hat{o}} \quad$: Gimbal and spinning rotor
   b. $\mathbf{\omega} \times \left(J_r \Omega \mathbf{\hat{s}} \right) \quad$: Spacecraft and spinning rotor
   c. $\mathbf{\omega} \times \left(J_g \dot{\delta} \mathbf{\hat{g}} \right) \quad$: Spacecraft and rotation of gimbal assembly
3. __Motor Torques:__
   a. Gimbal Motor
   b. Gyroscope Motor

Depending on the required fidelity of the simulation and whether the model is used for sizing or control certain simplifications can be made:

- For simplistic models one can separate 2a from the rest, as it represents the major output torque of single gimbal CMGs.
- The torque exuded on the spacecraft by the gyroscope motor (3b) can be removed if the gyroscope’s velocity is constant during operation.
- The gyroscopic reaction torque 2c will be much smaller than the other components and can therefore be disregarded for initial sizing etc.

Aside from providing the means to simulate the behavior of our CMGs, the parts 2b and 3a provide the requirements for gimbal motor sizing.
Part 2a is the torque required to sustain the reaction torque stemming from the rotation of the spacecraft and part 3a is the torque required to provide the desired torque dynamics.

## Steering of CMGs

The main challenge of steering CMGs lies in avoiding the complex singularities of a given array.
Staying some distance away from them also reduces the accelerations required in the gimbals.
Furthermore steering laws might also respect the gimbal limits regarding jerk, torque and speed.
Alternatively they can leave this to the inner control loops of the gimbal.

Most arrays consist of at least four CMGs, permitting null space motion, that is gimbal motions that produce a net output torque of zero(see @Sec:glossary for explanation).
Such motions can be used by the steering law to avoid singularities without introducing an error torque(see @Sec:glossary for explanation).
Other steering laws actually enable passing through singularities and are categorized as singularity escaping.
These methods introduce torque inaccuracies.

The fundamental principle of CMG steering laws lies in creating an inverse to the actuator Jacobian (see @Sec:glossary for explanation).
That is, given the Jacobian i.e. the matrix describing the impact of the various gimbals’ rates on the output torque, its inverse provides us with a set of target gimbal rates needed to obtain the desired torque.
Depending on the nature of the singularities, different approaches exist for the creation of a pseudo-inverse.
Some solutions avoid singularities by simply forbidding the production of certain torques, reducing the workspace of the array to guarantee singularity-free operation.

One can also optimize solutions with a variety of methods and for a variety of goals e.g. torque accuracy, energy consumption or time required for a maneuver.
Some of these optimizations might produce only local optima or not be able to guarantee torque accuracy between points in a torque trajectory.
These optimizations are research field unto themselves.
Leve et al. provide an an overview and selection of literature regarding CMG steering laws and their optimization [@LeveSpacecraftMomentumControl2015, ch. 7].

## CMG Workspaces

One important concept with CMGs is their workspace, also referred to as the momentum envelope.
A CMG array produces torque by changing the orientation of its momentum vector.
This vector is the sum of the momentum vectors of the gyroscopes in the array.
These individual momentum vectors of the gyroscopes maintain a constant magnitude, but; depending on the orientation; they might cancel each other out.
Together they create a volume of possible momentum configurations of the array.
This can be viewed as the workspace of the array whose axes are angular momentum around the three cartesian axes.
Ergo, the dimensions of the envelope are in Nms.

The hull or envelope depends on the configuration of the array.
If one imagines each CMG as having a momentum vector that can be gimbaled 360°, the result is a circle lying on the plane orthogonal to the gimbal’s axis.
The workspace enclosed by the envelope is then the set of points defined by the sum of multiple such vectors as they are rotated.

To develop a more intuitive understanding of the momentum envelope, one can picture the gyroscopes being gimballed to move the momentum vector through the volume enclosed by the envelope.
Remembering that a change in momentum is a torque, we can picture how the velocity of the point moving through the momentum space is the output torque of the array.

Therefore, want to produce a certain torque, the point begins moving in a certain direction.
At some point the point reaches the envelope and the array simply cannot produce any more torque around that axis.
The time this takes, i.e. the duration for which a given torque can be sustained, depends on the velocity of the point i.e. the magnitude of the torque and the size of the envelope.
Therefore, if the velocity in momentum space is in Nm and the distance travelled corresponds to time, then it becomes understandable why this envelope is measured in Nms.

Note that close to singularities, the gimbals will have to move greater amounts to achieve the same travel in momentum space.
This is akin to robots’ axes having to rotate further to travel a given distance in cartesian space when they are close to singularities.
Hence, given a limited gimbal velocity and acceleration, the torque dynamics will change throughout the momentum envelope.

The envelope is not a convex hull i.e. it intersects itself and can have additional internal surfaces.
These are the internal singularities that a steering law must avoid or be able to pass through them.
See @Fig:array-envelopes for an illustration of singularities of different array types.
Leve et al. also include a more in-depth discussion of the various types of singularities and how they are taken into account by different steering laws.

![Momentum envelopes of different single gimbal CMG arrays, i.e. their inner and outer singularities. From left to right: box, roof and pyramid array [@LeveSpacecraftMomentumControl2015]](./figures/cmg-envelopes.png){ #fig:array-envelopes short-caption="Momentum envelopes of CMG arrays"}

The shape of the workspace is of relevance to this work as the requirements will not be uniform in all directions.
A pendulum will often swing around a single axis, robot tasks might be dominated by torque around certain axes and part rotations will lie around the axis of the crane's rope.
Therefore it is of note that the shape the workspace of an array can be changed by altering its parameters.
In a roof array, the critical parameter is the angle of the roof.
See @Fig:roof-array-workspace-45deg and @Fig:roof-array-workspace-30deg for a comparison of different roof angles generated with the code provided in @sec:roof-array-workspace.

![Outer (green) and inner (orange) singularities for a four-CMG roof array with a roof angle of 45°.](./figures/roof-array-workspace-45deg.jpg){#fig:roof-array-workspace-45deg short-caption="Envelope of CMG roof array at 45°"}

![Outer (green) and inner (orange) singularities for a four-CMG roof array with a roof angle of 30°.](./figures/roof-array-workspace-30deg.jpg){#fig:roof-array-workspace-30deg short-caption="Envelope of CMG roof array at 30°"}

## Sizing of CMGs

Leve et al. provide a good overview regarding the sizing of spacecraft CMG [@LeveSpacecraftMomentumControl2015].
For terrestrial systems there is little literature available, but in their paper on a wearable SPCMG Chiu et al. discuss their sizing process [@ChiuDesignWearableScissoredPair2014].
However, generally speaking, the main characteristics of a CMG array are:

- the torque it can produce (Nm)
- the agility of the torque production i.e. its acceleration (Nm/s)
- the amount of torque it can sustain i.e. its momentum envelope (Nms).

The magnitude of these requirements obviously depends on the application for which the CMGs are being sized.
This application will also pose constraints regarding torque accuracy, weight, size, vibrations and power consumption.

Looking at the sizing methods used for spacecraft, the requirements usually stem from the agility demanded of the spacecraft, also called slewrate.
Given the moment of inertia of the spacecraft, the slewrate requirement will provide a required torque and duration that must be provided.
The given slewrate also results in a base rate whose reaction torque must be handled by the gimbal motors.
From this, the sizing of the CMGs can proceed and will subsequently be governed by the harsh constraints of spaceflight hardware.

This in particular is where the CMG sizing in this work diverges from spacecraft CMG design.
Weight, size, power and computational resources are of much smaller concern when hanging the CMGs from a crane.
For instance, some crane hooks have added weights which are required to ensure that the unloaded hook can overcome the rope friction in the pulley system.
Furthermore, the slewrate or rather the rotation speed of loads is only one concern.
The compensation of the robot’s motion and oscillations of the crane must also be taken into account.
Hence, as already alluded to during the review of existing applications, an understanding of the crane-CMG-robot system is required.
This is developed in the following chapter.
