
# Control Moment Gyroscopes 101

![](./figures/munroe-6a.jpg)

> Randal Munroe @GrossmanQuestionsRandallMunroe

Control moment gyroscopes are an established technology in spacecraft design and have also seen some terrestrial application.
In this chapter I hope to provide a basic understanding of gyroscopic reaction torque before giving an overview of its use in momentum control devices as well as existing sizing guidelines.

The use of CMGs in spacecraft is a very mature technology and therefore we can learn a lot for our application from several decades of research, development and active deployment.
As serendipity goes the start of my research in to crane-stabilisation roughly coincided with the publication of the book _Spacecraft Momentum Control Systems_ by Leve, Hamilton and Peck @LeveSpacecraftMomentumControl2015.
They did a great job of destilling said decades of research into a very legible book and most of the sizing and dynamics in this chapter are taken from there.

Unfortunately momentum control in spacecraft differs in its restrictions and goals from our use case of stabilising cranes.
The final part of this chapter describes these differences and motivates the subsequent research.

## Gyroscopic Reaction Torque

Dealing with gyroscopes can make your head spin.
Their behavior often runs counter to our intuitions due the relationship between torque, angular velocity and momentum involving the cross product of their vector, leading to everything constantly being rotated 90°.


Fundamental to understanding gyroscopes is that angular momentum ($\bm{h}$) is a conserved quantity i.e. it remains constant unless a torque ($\bm{\tau}$) is applied to the system.
Furthermore it helps to remember that therfore a change in angular momentum is a torque ($\bm{\tau} = \frac{d\bm{h}}{dt}$).

When the applied torque is aligned with the angular momentum the momentum simply increases.
This happens when a motor spins a wheel or we snap our fingers to spin a top and is quite intuitive.

When the torque lies orthogonal to the angular momentum we encounter the unintuitive side of gyroscopes.
Since no component of the torque is in line with the angular momentum its size and hence the speed of the spin remain constant.
Therefore the change in angular momentum takes the form of a change in the orientation of the angular momentum.
This is illustrated in @Fig:gyroscopic_torque.

![Illustration of a torque that lies orthogonal to an angular momentum corresponds to a rotation of the angular momentums orientation instead of a change in its size.](./figures/gyroscopic_torque.png){#fig:gyroscopic_torque }

It is this change in orientation in the form of a rotation and its relation to the torque via the size of the angular momentum that lets us understand everything from simple toys (@Fig:precession) to the momentum control systems of the International Space Station (@Fig:iss).

![Precession of a gyroscope. (Public Domain, taken from Wikimedia)](./figures/Gyroscope_precession.gif){#fig:precession }

![Astronaut Dave Williams replacing a CMG on the ISS (Public Domain, NASA Photo ID: S118-E-06998)](./figures/ISS-CMG.jpg){#fig:iss }

Before proceeding I would like to emphasise several points:

- the angular momentum ($\bm{h}$) acts akin to a lever between $\bm{\omega}$ and $\bm{\tau}$
- the speed at which our gyroscope spins is not affected by torque acting orthogonal to its axis of rotation
- such a torque will instead result in a rotation orthogonal to both angular momentum and said torque

The last point is key to understanding CMGs where we do the inverse: rotate an angular momentum and thereby create a reaction torque.
This is illustrated in @Fig:CMG_principle.

![Principle of a CMG. By rotating a gyroscope orthogonally to its spin axis we create a reaction torque orthogonal to the gimbal axis and the gyroscopes spin axis.](./figures/CMG_principle.png){#fig:CMG_principle }

The torque produced by such a gimbal rotation is described by:

\begin{equation}\label{reaction_torque}
\bm{\tau} = \bm{\omega} \times \bm{h}
\end{equation}

The beauty of a CMG lies within the fact that the torque required to rotate the gimbal as to produce a given rate $\bm{\omega}$ is independant of the angular momemtum $\bm{h}$ of the gyroscope.
The gimbal motor only has to overcome the rotational inertia of the gyroscope and the surrounding gimbal bearings etc.
Yet since the torque of the CMG also depends on the angular momentum of the spinning gyroscope we can increase the output torque of the CMG simply by increasing the spin spead of the gyroscope.

This is were the lever analogy really shines:
Just like a longer leaver lets us produce a greater output force with the same input force, so can a greater angular momentum (e.g. faster spinning gyroscope) let us produce a larger output torque with the same gimbal motor.
Since the gyroscopes motor only needs to overcome the bearing friction, once it has reached the desired speed, CMGs let us produce very large torques with comparatively small motors.
Leve et al. mention terrestrial systems capable of output in excess of 100.000 Nm that require only a few kW to operate [@LeveSpacecraftMomentumControl2015, 46].
This is quite a feat when compared with e.g. a Tesla Model S motor which produces 1.250 Nm using 581 KW.

Unfortunatly there is a caveat.
If we look at @Fig:CMG_principle we see that the produced torque gets applied to the body via the bearings of the gyroscope and the those of the gimbal.
This of course means that we have to size them accordingly but the bigger issue occurs when our body containing the CMG happens to rotate around the axis of our output torque.
In such a case our wonderful angular momentum lever comes back to bite us, since it now leads to a large torque being put on our gimbal motor.
Sizing the motor to accomodate for such cases can quickly negate the advantage provided by a CMG and we will discuss this in the later sizing sections.

## Applications of CMGs

This section will cover a selection of CMG applications.
Given their at times strange properties CMGs have a very narrow field of utility.
With most of the research surrounding CMGs coming from the space exploration a brief historic romp through CMGs in space will illustrate how our understanding of the fundamental principles of CMGs has evolved.
The subsequent section covers the few terrestrial fields of application and serves to illustrate some of the challenges and limitations of CMGs.

### Development of CMG Technology and Spacecraft Application

- ability of torque without having to "push off"
- early spacecraft
  - direction of torque rotates with gimbal >> scissored pair
  - SPCMG array for first spacewalks
  - singularities: saturation and internal
  - internal singularities known from gimbal lock issues with navigational gyros
  - example: Apollo Missions
- Dual Gimbal CMGs
  - similar mechanics to nav. gyros makes them familiar to spacecraft eng.
  - simpler internal singularities >> less complex steering laws
  - extreme example ISS
  - issue: second gimbal motor must transfer torque
- Single Gimbal CMGs
  - torque only runs via bearings
  - various arrays possible leading to a variety of singularities
  - recommendation: roof array
  - refs to steering laws, null space navigation
- stabilisation of robot motion, lots of CitationNeeded
  - attractive idea, only once flown
  - very slow robot motion for various reasons
  - robot arm on ISS not integrated to ACS!
  - optimisations have been studies
    - low to zero torque maneuvers
    - how does one deal with forces???
    - idea of second robot >> mirror moves...

![Rendering of the ETS VII research satellite used to evaluate the use of robot arms to manipulate other satellits. CitationNeeded](./figures/ets-vii-space-robot.jpg){#fig:ets-vii-space-robot}

### Terrestrial Applications

- most common application: stabilisation
- historic:
  - monorail and car (never realised?) @LeveSpacecraftMomentumControl2015, CitationNeeded
    - slow motors >> heavy gyro wheels >> inefficient
    - mechanical actuation only (how did this work???)
  - ship stabilisation: @LeveSpacecraftMomentumControl2015, CitationNeeded
    - actually sailed
    - biggest CMGs ever built
    - precession vs. driven stabilisation
- current commercial applications:
  - sea keeper, gyromarine and veem for yacht stabilisation @AdamsGyroscopicRollStabilizer2005
    - approx. torque??? price???
    - patents of bearing cooling point towards engineering challenges @AdamsCoolingBearingsMotors2009
    - utilize rotor as energybuffer
  - vehicle stabilisation, see @SpryGyroscopicStabilisationUnstable2008 for review
    - authors also extend to two gyros
    - LitMotors @KimElectronicControlSystem2013
      - vaporware startup with two wheeled car
      - vibration and noise show up as issue
      - looks like passive to gyro system?
      - points towards issues regarding viability of high speed stabilisation
- research applications
  - heart stabilisation @GagneGyroLockStabilizingHeart2012, @GagneCardiacMotionCompensation2009
    - why did they use CMG???
  - human gait stabilisation @ChiuDesignWearableScissoredPair2014, @LiGyroscopicAssistanceHuman2012
    - useful sizing considerations
    - single DoF SPCMG though
  - bike stabilisation, CitationNeeded
    - feasible or only student exercise???
  - underwater robot @YimeDesignCMGUnderwater2011, @ThorntonInternalActuationUnderwater2005, @PenaAdvancesDevelopingTelemanipulators2009
    - why instead of props?
  - locomotion @RomanishinMblocksMomentumdrivenMagnetic2013, @GajamohanCubliCubeThat2012
    - actually reaction wheels but well known examples

### Crane Applications

Given that there have been significant efforts to automate construction in Japan and Korea dating back to the 1980s, it is unsurprising that one can find some research into the actuation of cranes from these countries.

- CMG vibration control of gondola @KankiDevelopmentCMGActive1994
  - passenger gondola
  - SPCMG rotated to counter the wind direction
  - validated in the field with two 30kg flywheels
- Motorized Hook patent @gimseoghoHukeuhoejeonjojeongiGaneunghanKeureinyong1997
- Field tested single CMG device @InouePracticalDevelopmentSuspender1998
  - mention of previous devices using fans
  - analysis of assembly times and reduction of dangerous work
  - discuss use of active control and passive stabilisation
- Single CMG Beam Stabilisation work by Yi et al @YiImplementationGyroActuator1999, @YiAttitudeControlStabilization2000, @SaAttitudeControlStabilization2001
  - @YiImplementationGyroActuator1999 controller design for rotating mass hanging from wire
  - @YiAttitudeControlStabilization2000 only abstract in english, addition of IMU for sensing, note that active use of gyro is needed for stabilisation of slow rotation drift since slow speeds since gear ratio of gimbal means that slow speeds can't create suitable reaction torque
  - @SaAttitudeControlStabilization2001 add clutch to be able to use reaction torque for stabilisation without overloading motor, mention inertia estimation in outlook, lengthy experiments and discussion about what essentially boils down to slew rate
- @LeeAnalysisFieldApplicability2012 test of motorized hook
  - authors also hold two patents regarding powering of rotating hooks
    - @gimseoghoHukeuhoejeonjojeongiGaneunghanKeureinyong1997 (not by authors) uses electrical motor
    - use of a clock spring
    - use of vertical hook travel to power rotation device
  - paper uses electric motor to rotate hook
  - discuss @InouePracticalDevelopmentSuspender1998 incorrectly, stating that they only used passive control
  - performed measurements of traditional method on construction site
  - rotated beams with device off site
- @KodaniTransportingRotatingControl2017 single CMG on jib crane
  - only control yaw
  - run into singularity of CMG
  - while yaw is controlled this would also occur simply due to passive stabilisation
- beam with propellors??? seen in Bock slides, haven't been able to find reference

- issue between CMGs and passive Gyros
  - motors try to block precession
  - see use of clutch in CitationNeeded
- mixture most likely possible with good gimbal controllers
- unlike roll stabilisation we have 3dof to take into account and therefore more complex singularity avoidance necessitating driven CMG


## Dynamics of CMGs {#sec:cmg-dynamics}

With the number of spinning parts involved in a CMG the dynamics exhibit a certain complexity.
To be able to size and control the CMGs for our application we need to understand and model these dynamics.


In this section we will introduce and discuss the model derived in great detail in Chapter 4.5 of @LeveSpacecraftMomentumControl2015.
The resulting expressioon is the derivative (with respect to time) of the angular momentum of a CMG spacecraft with variable speed gyro-rotors (Eq. 4.81 in @LeveSpacecraftMomentumControl2015):

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

Leve et al. use vector-dyadic notation for the above and spend a section introducing it in @LeveSpacecraftMomentumControl2015.
For a basic understanding we can ignore the dyadic notation, summations etc. and focus on the following symbols:

- $\mathbf{H}$: angular momentum of the spacecraft
- $\mathbf{\omega}$: angular velocity of the spacecraft
- $\mathbf{J}, J_r, J_g$: inertia of spacecraft, gyroscope rotor and inner gimbal assembly
- $\mathbf{\hat{s}, \hat{g}, \hat{o}}$: axis of the rotor, gimbal and output torque[^outputtorque]
- $\dot{\delta}, \ddot{\delta}$: angular velocity and acceleration of the gimbal
- $\Omega$: angular velocity of the gyroscopes rotor

[^outputtorque]: $\mathbf{\hat{o}} = \mathbf{\hat{g}} \times \mathbf{\hat{s}}$

Using this simplified notation lets us look at the various parts contributing to the changes in angular momentum (for a exact discussion please refer to @LeveSpacecraftMomentumControl2015):

1. __Rigid-Body Motion:__ These are all terms involving $\mathbf{J}$.
2. __Gyroscopic Reaction Torques:__   
   Caused by either the motion of the spacecraft or gimbal rotating an angular momentum vector.
   a. $J_r \Omega \dot{\delta} \mathbf{\hat{o}} \quad$: Gimbal and spinning rotor
   b. $\mathbf{\omega} \times \left(J_r \Omega \mathbf{\hat{s}} \right) \quad$: Spacecraft and spinning rotor
   c. $\mathbf{\omega} \times \left(J_g \dot{\delta} \mathbf{\hat{g}} \right) \quad$: Spacecraft and rotation of gimbal assembly
3. __Motor Torques:__
   a. Gimbal Motor
   b. Gyroscope Motor

Depending on the required fidelity of the simulation and whether the model is used for sizing or control we can ignore or seperate certain parts:

- For an attitude control system it make sense to seperate 2a from the rest as it represents the major output torque of single gimbal CMGs and is controllable through the CMG steering laws.
- The torque exuded on the spacecraft by the gyroscope motor (3b) can be ignored if the gyroscopes velocity is constant during operation.
- The gyroscopic reaction torque 2c will be much smaller than the others and can therefore be ignored for initial sizing etc.

Aside from providing us with the means to simulate the behaviour of our CMGs the parts 2b and 3a describe the requirements for gimbal motor sizing.
Part 2a being the torque required to sustain the reaction torque stemming from the rotation of the spacecraft and part 3a being the torque required to provide the desired torque dynamics.

## Steering of CMGs

- basic principles
- refer to @LeveSpacecraftMomentumControl2015
- see @Sec:spcmg-steering

## CMG Workspaces

- momentum envelope and momentum dynamics (Nms and Nm/s)
- outer and inner singularities
- configurations and why we choose roof config

![Various configuration options for singe gimbal CMGs. Taken from CitationNeeded.](./figures/sg-cmg-configurations.jpg){#fig:sg-cmg-configurations}

![Example of a momentum envelope. Taken from CitationNeeded.](./figures/cmg-momentum-envelope.jpg){#fig:cmg-momentum-envelope}

![Outer (green) and inner (orange) singularities for a four CMG roof array with a roof angle of 45°.](./figures/roof-array-workspace-45deg.jpg){#fig:roof-array-workspace-45deg}

![Outer (green) and inner (orange) singularities for a four CMG roof array with a roof angle of 30°.](./figures/roof-array-workspace-30deg.jpg){#fig:roof-array-workspace-30deg}

## Sizing of CMGs

- main factors in space: @LeveSpacecraftMomentumControl2015
  1. agility (slewrate)
  2. workspace (Nms)
  3. interaction with system dynamics
  4. engineering considerations (weight, power, bearings, vibrations)
- further/differing factors for stabilisation applications:
  1. produced torque (Nm)
  2. agility (Nm/s)

### Torque, Agility and Workspace

- max torque simply $\omega \cdot h$
- agility in spacecraft is slewrate i.e. how fast can I turn my satellite
  - interesting note: shift in derivative between gimbal and spacecraft
  - can be used as key factor for sizing spacecraft momentum control systems
- workspace
  - why Nms?
  - saturation: simple example SPCMG
  - saturation for arrays
  - what does a workspace shape mean?
  - example workspaces
  - shaping of roof workspaces (see appendix for code)
- agility of stabilisation systems
  - why Nm/s
  - do any of the publications go into this???

## Applicability to our Usecase

- weight, power and computational power is a limited issue
- worst case assumption regarding rotation along torque axis needs to be examined
- slewrate is next to useless in sizing
- different speeds when it comes to stabilisation of robots
- no sizing info available regarding seakeeper and lit motors
- understanding of usecase required to inform workspace and agility
- crane introduces own set of dynamics