
# Control Moment Gyroscopes 101

![](./figures/munroe-6a.jpg)

> Randal Munroe [@GrossmanQuestionsRandallMunroe]

Control moment gyroscopes are an established technology in spacecraft design and have also seen some terrestrial application.
In this chapter I hope to provide a basic understanding of gyroscopic reaction torque before giving an overview of its use in momentum control devices as well as existing sizing guidelines.

The use of CMGs in spacecraft is a mature technology and therefore we can learn a lot for our application from several decades of research, development and active deployment.
As serendipity goes the start of my research in to crane-stabilization roughly coincided with the publication of the book _Spacecraft Momentum Control Systems_ by Leve, Hamilton and Peck [@LeveSpacecraftMomentumControl2015].
They did a great job of distilling said decades of research into a very legible book and most of the sizing and dynamics in this chapter are taken from there.

Terrestrial applications of CMGs are less common, with the only commercially available solutions being roll stabilizers for ships.
Other applications have been proposed in research including crane stabilization.
There have also been several failed attempts at creating gyroscopically stabilized two-wheeled vehicles.

Unfortunately our intended use of of CMGs goes beyond previous crane stabilization efforts and differs in its goals and restrictions from those in spacecraft and ships.
By delving into the various existing applications this chapter hopes to provide a deeper understanding of the potentials and limitations of CMGs and thereby motivate the subsequent work.

## Gyroscopic Reaction Torque

Dealing with gyroscopes can make your head spin.
Their behavior often runs counter to our intuitions due the relationship between torque, angular velocity and momentum involving the cross product of their vectors, leading to everything constantly being rotated 90°.

Fundamental to understanding gyroscopes is that angular momentum ($\bm{h}$) is a conserved quantity i.e. it remains constant unless a torque ($\bm{\tau}$) is applied to the system.
Furthermore it helps to remember that therefore a change in angular momentum is a torque ($\bm{\tau} = \frac{d\bm{h}}{dt}$).
When the applied torque is aligned with the angular momentum the momentum simply increases.
This happens when a motor spins a wheel or we snap our fingers to spin a top and is quite intuitive.

When the torque lies orthogonal to the angular momentum we encounter the unintuitive side of gyroscopes.
Since no component of the torque is in line with the angular momentum its size and hence the speed of the spin remain constant.
Therefore the change in angular momentum takes the form of a change in the orientation of the angular momentum.
This is illustrated in @Fig:gyroscopic_torque.

![Illustration of how a torque that lies orthogonal to an angular momentum corresponds to a rotation of the angular momentums orientation instead of a change in its size.](./figures/gyroscopic_torque.png){#fig:gyroscopic_torque }

It is this change in orientation in the form of a rotation and its relation to the torque via the size of the angular momentum that lets us understand everything from simple toys (@Fig:precession) to the momentum control systems of the International Space Station (@Fig:iss).

![Precession of a gyroscope. Gravity would usually cause the object to topple over. Instead the conservation of angular momentum leads to a precession whose motion causes a torque that balances out the torque caused by gravity.(Public Domain, taken from Wikimedia)](./figures/Gyroscope_precession.gif){#fig:precession }

![Astronaut Dave Williams replacing a CMG on the ISS. (Public Domain, NASA Photo ID: S118-E-06998)](./figures/ISS-CMG.jpg){#fig:iss }

Before proceeding I would like to emphasize several points:

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

The beauty of a CMG lies within the fact that the torque required to rotate the gimbal as to produce a given rate $\bm{\omega}$ is independent of the angular momentum $\bm{h}$ of the gyroscope.
The gimbal motor only has to overcome the rotational inertia of the gyroscope and the surrounding gimbal bearings etc.
Yet since the torque of the CMG also depends on the angular momentum of the spinning gyroscope we can increase the output torque of the CMG simply by increasing the spin speed of the gyroscope.

This is were the lever analogy really shines:
Just like a longer leaver lets us produce a greater output force with the same input force, so can a greater angular momentum (e.g. faster spinning gyroscope) let us produce a larger output torque with the same gimbal motor.
Since the gyroscopes motor only needs to overcome the bearing friction once it has reached the desired speed, CMGs let us produce very large torques with comparatively small motors.
Leve et al. mention terrestrial systems capable of output in excess of 100.000 Nm that require only a few kW to operate [@LeveSpacecraftMomentumControl2015, p. 46].
This is quite a feat when compared with e.g. a Tesla Model S motor which produces 1.250 Nm using 581 KW.

Unfortunately there is a caveat.
If we look at @Fig:CMG_principle we see that the produced torque gets applied to the body via the bearings of the gyroscope and those of the gimbal.
This of course means that we have to size them accordingly but the bigger issue occurs when our body containing the CMG happens to rotate around the axis of our output torque.
In such a case our wonderful angular momentum lever comes back to bite us, since it now leads to a large torque being put on our gimbal motor.
Sizing the motor to accommodate for such cases can quickly negate the advantage provided by a CMG and we will discuss this in the later sizing sections.

## Applications of CMGs

This section will cover a selection of CMG applications.
Given their at times strange properties CMGs have a very narrow field of utility.
With most of the research surrounding CMGs coming from the space exploration a brief historic romp through CMGs in space will illustrate how our understanding of the fundamental principles of CMGs has evolved.
The subsequent section covers the few terrestrial fields of application and serves to illustrate some of the challenges and limitations of CMGs.

### Development of CMG Technology and Spacecraft Application

The need to produce a torque without having something to push off from does not occur frequently.
Even plane can push off of the air surround it, given sufficient speed.
This explains why momentum control devices are such a very spaceflight technology.

For small spacecraft reaction wheels are common and provide a straightforward means of transferring the torque of a motor to the spacecraft.
It is in larger craft, with higher torque demands that the lever effect of CMGs becomes essential.
The first CMGs to fly in space where three dual gimbal CMGs attached to Skylab.
Dual gimbal CMGs are less efficient than single gimbal CMGs, as the produced torque is always transferred in part through a gimbal motor, whereas in a single gimbal design it will be transferred via bearings.
But there are several reasons why Skylab and many subsequent spacecraft including the ISS used dual gimbal CMGs.

As a gimbal rotates to produce torque with the gyroscope, so does the orientation of the output torque vector.
This gives rise to complex steering and issues with singularities.
The Apollo program did not use CMGs but had three gyroscope for inertial measurement of the spacecrafts orientation.
These gyroscopes where suspended in three nested gimbal providing feedback regarding the spacecrafts yaw, pitch and roll.
The decision to only use three gimbals lead to more frequent issues with gimbal lock (a singularity where the gimbal axis align) than was expected, during multiple Apollo missions.
The Apollo guidance computer had to include functions to alert the astronauts of an impending gimbal lock and Mike Collins joked that all he wanted for Christmas was a fourth gimbal as he was repeatedly resetting the gimbals during Apollo 11. 

Given the limited computational resources and understanding of CMG steering at the time it therefore very understandable that NASA chose to go with dual gimbal designs, which eliminate the internal singularities on the CMG array.
The attitude control systems for the first spacewalks of the US program took a different approach.
By mechanically linking to CMGs so that they mirror each others motion, one can create a scissored pair CMG array.
Here the sum of the two gyroscope's momentum vectors always lies along a single axis, making for much simpler steering.
The downside is that one has to use six instead three CMGs to be able to produce torque around all three axis in space.

Over the years several ways to array single gimbal CMGs and associated steering laws with singularity avoidance have been developed.
Since redundancy is a must in spaceflight the arrays usually start with four CMGs unless other momentum control devices are also included in the spacecraft.
The three common arrays are box, pyramid and roof (see @fig:sg-cmg-configurations).
Leve et. al recommend roof arrays due to their simpler and easier to avoid internal singularities.

![Various configuration options for single gimbal CMGs. Taken from an extensive treatise on the geometric theory of single gimbal CMGs [@KurokawaGeometricStudySingle1998].](./figures/sg-cmg-configurations.jpg){#fig:sg-cmg-configurations}

Momentum control devices like reaction wheels, CMGs or magneto-torquers enable spacecraft to adjust and control their orientation without expending fuel.
This makes them invaluable given weight and volume constraints in spaceflight.
But such systems also come into play when one attempts to add robot arms to spacecraft.

While the ISS has a remote controlled arm, the control of this arm is not coupled with the attitude control system (ACS) of the ISS.
The ACS simply continues to try and maintain the ISS in the desired orientation.
This is most likely possible due to the very large moment of inertia that the ISS possesses.

The only other robot arm that has operated in space is that of the ETS VII research satellite (see @Fig:ets-vii-space-robot and [@OdaSummaryNASDAETSVII2000]).
The goal of the this research was to study how one satellite might capture another spacecraft for repairs or even just removal of space debris.
The missions experiments were performed using both programmed motion and remote control operation with the speed limited 2mm/s.
Such low speeds were necessary so that the ACS of the spacecraft could maintain its orientation.
Using the ETS VII satellite Yoshida et al. were able to show the efficacy of reactionless motionplanning using so called reaction-null-space [@yoshida_zero_2001].
These are sets of movement that in theory produce zero reaction torque at the base of the robot.
Note that the movements would feel ridiculous in the context of earth, as they took over 20 minutes to move less than 50cm.

While the ETS VII is the only such system to actually fly there has been a lot of research into robot arms in space (see [@ReintsemaDLRAdvancedTelerobotic2007] for a review), with the first robot arm flying as an experiment aboard the space shuttle Columbia [@HirzingerROTEXtheFirstRemotely1994].
These include the idea of adding a second robot to compensate the torques of the first robot [@yoshida_dual_1991].
This proved to be a waste of payload as one is in essence creating a low efficiency momentum control device, since the second arm cannot be used as an arm while it is compensating.
Other works have studied the use of CMG based ACS and optimization techniques to ensure that these can compensate the torques of the arm [@li_motion_2013].
Others have proposed using CMGs as the actuators of the arm to create kinematics capable of moving in space without exerting torques on their host spacecraft [@carpenter_reducing_2009].

\todo{proposals for dealing with forces produced by robots, can't we just model them as torques?}

![Artists rendition of the ETS VII research satellite used to evaluate the use of robot arms to manipulate other satellites (bottom right, taken from JAXA [@JAXAEngineeringTest]). The satellite during ground tests (left, taken from ESA Bulletin [@VisentinTestingSpaceRobotics1999]) and overview of its robot setup (top right, taken from [@OdaSummaryNASDAETSVII2000])](./figures/ets-collage.png){#fig:ets-vii-space-robot}

### Terrestrial Applications

Looking to terrestrial applications we mostly see CMGs being used to stabilize vehicles.
Attitude control with CMGs simply doesn't make sense on earth as most vehicles need to rotate at velocities that aren't feasible for CMG based control, given the high reaction torques that would have to be sustained by the gimbal motors.
As we have the ground, water and air to push off from we usually can simply use wheel, fins and wings instead.

So CMGs find terrestrial application where such systems don't work: two wheeled vehicles that should remain upright at slow speeds or a standstill and roll stabilization for ships at rest.
Looking back there are early examples of both applications.
For ground vehicles there is a gyrocar commissioned in 1912 by Pyotr Petrovich Shilovsky who also built a monorail and wrote a book on the uses of gyroscopes in 1924 [@ShilovskiiGyroscopeItsPractical1924].
Ships of the same period saw the construction of probably the largest CMGs with the first deployment to a large passenger liner, the Conte di Savoia in 1931 [@RexConteDi]
The gyroscope weighed in 175t and spun at 910 rpm (see @Fig:conte-gyro).
Given that control engineering or cybernetics hadn't come about yet it is obvious that these systems must have operated on a passive control principle.

![Gyro stabilizer aboard the Conte di Savoia passenger liner launched in 1934.](./figures/conte-di-savoia.jpg){ #fig:conte-gyro }

The way that such passive stabilization with gyroscopes works is as follows:
The tipping vehicle exerts a torque orthogonal to the gyroscopes momentum and the gimbals axis.
This causes the gyroscope to precess around the gimbal axis, a movement that in turn causes a reaction torque counter to the tipping motion of the vehicle.
If the gimbal resists the precession for instance through friction this torque also acts agains the the exciting torque.

Low speeds of motors available back then as well as the much simpler solution of adding further wheels or putting a foot on the ground are why gyroscopically stabilized ground vehicles didn't take off.
There were subsequent attempts at producing gyro cars.
In the late sixties a team around Thomas Summers who had worked on guidance gyroscopes in the war and the car designer Alex Tremulis, built the Gyro-X prototype.
The goal was to increase road capacity and improve aerodynamics by slimming a car to two wheels, but the team went bankrupt before they were able to solve the engineering challenges involved in actually keeping the car stable.
A recent startup called Lit Motors also attempted to produce a two wheeled car in a similar vein and filed multiple patents [@KimElectronicControlSystem2013] (see also @Fig:litmotors).
News surrounding the company went silent after an initially flurry of coverage around 2012 and some speculate that they weren't able to reduce noise and vibrations sufficiently to create a usable consumer experience, but they have recently relaunched their [website](https://www.litmotors.com).
For a discussion as well as a derivation of equations of motion and control system for stabilization of two wheeled vehicles see [@SpryGyroscopicStabilisationUnstable2008].
In this paper the authors also extend the equations of motion to use two gyroscopes of opposite spin direction and show how this benefits control performance.

![Prototype of the Lit Motors C1 gyro-stabilized vehicle being driven on the webseries _Spark_ produced by Maker Studios](./figures/litmotors.gif){ #fig:litmotors }

While roll stabilizing gyroscopes went out of fashion for ships as hull and fin designs improved, they have become a commercial product offered by multiple companies (see @Fig:seakeeper for an example).
Their target audience are yachts as well as commercial vessels, where roll stabilization at rest or slow speeds is of greater import.
The CMGs here are the the largest CMGs commercially available, since satellites require much lower torques.
It is therefore unsurprising that a naval CMG was used in the recent resurrection of the Gyro-X at the Lane Motor Museum.
It is also worth pointing out that some naval CMGs use the energy stored in the spinning gyroscope to provide additional electrical power during high peaks (caused by the actuation).
This was also considered for spacecraft, but as spacecraft batteries have reached a similar energy density to high speed flywheels the added weight of the required electronics and challenges of high velocity gyroscopes in space have lead to this idea being scrapped.

![Marketing video for a ship stabilizing gyroscope, taken from [@SeakeeperGyroStabilizers]. The left boat is being stabilized, the right one is not.](./figures/seakeeper.gif){ #fig:seakeeper }

The gyroscopes used in naval CMGs are large enough to warrant running in a vacuum to reduce friction and are actuated using hydraulic systems.
Filed patent point towards interesting engineering challenges [@AdamsGyroscopicRollStabilizer2005] for instance regarding the cooling of the gyroscope bearings [@AdamsCoolingBearingsMotors2009].
Given the passive stabilization principle discussed earlier, one might surmise that no actuation is required.
The actuation is required to ensure that the gyroscope doesn't reach a singularity, limit the precession speed and thereby the output torque.
Given the size of the gyroscopes and bearings involved the actuation is also required to assist the gyroscope in overcoming friction.
This is important during small excitations where the friction might introduce a significant time delay in the systems reaction.

Researchers have also proposed other applications for CMGs.
The weirdest is most likely the use of a CMG to stabilize a beating heart during surgery [@GagneCardiacMotionCompensation2009; @GagneGyroLockStabilizingHeart2012].
Several researchers have built CMGs into devices aimed at stabilizing human gait to e.g. assist the elderly [@ChiuDesignWearableScissoredPair2014; @LiGyroscopicAssistanceHuman2012].
Others have suggested using CMGs to orient underwater robots to allow for more precise movements and efficient use of thrusters [@YimeDesignCMGUnderwater2011; @ThorntonInternalActuationUnderwater2005; @PenaAdvancesDevelopingTelemanipulators2009].
Others have used reaction wheels instead of CMGs to create small, self assembling robots that move by flipping themselves [@RomanishinMblocksMomentumdrivenMagnetic2013].
A quite well known example of fun with momentum control is the Cubli, a self balancing cube that also uses reaction wheels [@GajamohanCubliCubeThat2012].

### Crane Applications

Given that there have been significant efforts to automate construction in Japan and Korea dating back to the 1980s, it is unsurprising that one can find some research into the actuation of cranes from these countries.

A work from 1994 is relevant to cranes but actually on the stabilization of a passenger gondala uses an SPCMG with two 30kg flywheels to compensate wind excitation [@KankiDevelopmentCMGActive1994].
In 1997 a patent was filed on adding a motor to a crane hook to rotate the load [@gimseoghoHukeuhoejeonjojeongiGaneunghanKeureinyong1997].
In such a case the crane cables resistance to twisting would be what the motor has to push off against.
A paper from 1998 describes field testing of a device using a single CMG [@InouePracticalDevelopmentSuspender1998].
Interestingly the authors also mention previous work that utilized fans or propellors to actuate a crane's load.
We have sadly not been able to find a source for this, the language barrier being quite an issue.
The authors also analyzed how the device improved assembly times and reduced dangerous work.
The most impressive improvement came about in tasks that involved the rotation of the load.
Here the work duration was roughly halved and nearly all work they classified as dangerous was eliminated.
Their device used the passive stabilization principle during transport and a remote controlled actuation to cause the load rotation.
Yi et al. have published several works on stabilizing beams during construction work [@YiImplementationGyroActuator1999; @YiAttitudeControlStabilization2000; @SaAttitudeControlStabilization2001].
Starting with a single CMG hanging from a wire their subsequent publications (one having only the abstract available in english) discuss the addition of an IMU as a rotary encoder attached to the wire is too inaccurate.
They also run into the same issue as naval CMGs that slow rotations aren't able to overcome the gimbal friction.
Their last paper adds a clutch to the gimbal to avoid overloading the gimbal motor during passive stabilization.
In [@LeeAnalysisFieldApplicability2012] the authors use a motorized hook to rotate beams.
The authors also filed to patents with regard to ways of powering such a hook, one proposed a clock spring with the other proposing use of the vertical hook travel to power the device.
They incorrectly discuss [@InouePracticalDevelopmentSuspender1998], stating that the author were only using passive stabilization.
More recently researchers have once again used a single CMG to stabilize the yaw of a load attached to a model of a jib crane [@KodaniTransportingRotatingControl2017].
The author run into issues with the singularity and changing orientation of the output torque.

\missingfigure{crane stabilisation papers}

### Summary

The idea of using gyroscopic effects for stabilization is an old one.
Yet having reviewed existing applications it appears that a solution for the idea of stabilizing a robot hanging from a crane can't be easily extrapolated from the existing applications of CMGs.
Unlike a satellite or spacecraft we are predominantly interested in maintaining a given position, not in a rotational agility.
The oscillations and dynamic behavior of cranes will differ from those of ships and unlike ships we have to deal not only with roll, but also pitch and yaw.
It is this three-dimensional requirement that also sets this challenge apart from the previous experiments with CMGs and cranes.

We will have to develop an understanding of crane-cmg dynamics to let us find a way to consolidate the different control and sizing requirements of on the one hand a system at rest being excited by e.g. a robot and on the other hand a system in an oscillatory state that needs to be dampened.

## Dynamics of CMGs {#sec:cmg-dynamics}

With the number of spinning parts involved in a CMG the dynamics exhibit a certain complexity.
To be able to size and control the CMGs for our application we need to understand and model these dynamics.
This section will therefore introduce and discuss the model derived in great detail in Chapter 4.5 of [@LeveSpacecraftMomentumControl2015].
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

Leve et al. use vector-dyadic notation for the above and spend a section introducing it in [@LeveSpacecraftMomentumControl2015, sec. 4.1].
For a basic understanding we can ignore the dyadic notation, summations etc. and focus on the following symbols:

- $\mathbf{H}$: angular momentum of the spacecraft
- $\mathbf{\omega}$: angular velocity of the spacecraft
- $\mathbf{J}, J_r, J_g$: inertia of spacecraft, gyroscope rotor and inner gimbal assembly
- $\mathbf{\hat{s}, \hat{g}, \hat{o}}$: axis of the rotor, gimbal and output torque[^outputtorque]
- $\dot{\delta}, \ddot{\delta}$: angular velocity and acceleration of the gimbal
- $\Omega$: angular velocity of the gyroscopes rotor

[^outputtorque]: $\mathbf{\hat{o}} = \mathbf{\hat{g}} \times \mathbf{\hat{s}}$

Using this simplified notation lets us look at the various parts contributing to the changes in angular momentum (for an exact discussion please refer to [@LeveSpacecraftMomentumControl2015, sec. 4.5]):

1. __Rigid-Body Motion:__ These are all terms involving $\mathbf{J}$.
2. __Gyroscopic Reaction Torques:__   
   Caused by either the motion of the spacecraft or gimbal rotating an angular momentum vector.
   a. $J_r \Omega \dot{\delta} \mathbf{\hat{o}} \quad$: Gimbal and spinning rotor
   b. $\mathbf{\omega} \times \left(J_r \Omega \mathbf{\hat{s}} \right) \quad$: Spacecraft and spinning rotor
   c. $\mathbf{\omega} \times \left(J_g \dot{\delta} \mathbf{\hat{g}} \right) \quad$: Spacecraft and rotation of gimbal assembly
3. __Motor Torques:__
   a. Gimbal Motor
   b. Gyroscope Motor

Depending on the required fidelity of the simulation and whether the model is used for sizing or control we can ignore or separate certain parts:

- For simplistic model one can separate 2a from the rest, as it represents the major output torque of single gimbal CMGs.
- The torque exuded on the spacecraft by the gyroscope motor (3b) can be ignored if the gyroscopes velocity is constant during operation.
- The gyroscopic reaction torque 2c will be much smaller than the others and can therefore be ignored for initial sizing etc.

Aside from providing us with the means to simulate the behavior of our CMGs the parts 2b and 3a describe the requirements for gimbal motor sizing.
Part 2a being the torque required to sustain the reaction torque stemming from the rotation of the spacecraft and part 3a being the torque required to provide the desired torque dynamics.

## Steering of CMGs

The main challenge of steering CMGs is avoiding the complex singularities of a given array.
Staying some distance away from them also reduces the required accelerations in the gimbals.
Furthermore steering laws might also respect the gimbal limits regarding jerk, torque and speed.
Alternatively they can leave this to the inner control loops of the gimbal.

Given that most arrays with have at least four CMGs, the arrays permit null space motion.
That is gimbal motions that produce a net output torque of zero.
Such motions can be used by the steering law to avoid singularities without introducing an error torque.
Other steering laws actually enable passing through singularities and are categorized and singularity escaping.
These methods to introduce torque inaccuracies to be able to do so.

The fundamental principle of CMG steering laws in creating an inverse to the actuator Jacobian.
That is given the Jacobian i.e. the matrix describing the impact of the various gimbal's rates on the output torque, its inverse provides us with a set of target gimbal rates needed to obtain the desired torque.
Depending on the nature of the singularities different approaches exist to create a psuedo-inverse.
Some solutions avoid simulations by simply forbidding the production of certain torques, reducing the workspace of the array to guarantee singularity free operation.
Furthermore, one can optimize solutions in various ways.
In spacecraft, as everywhere, different optimization goals exist e.g. torque accuracy, energy consumption or time required for a maneuver.
Some of these optimizations might produce only local optima or not be able to guarantee torque accuracy between points in a torque trajectory.
The reader is pointed toward [@LeveSpacecraftMomentumControl2015, ch. 7] for a discussion of CMG steering laws and a selection of literature from a vast field of research.

## CMG Workspaces

One important concept to understand with CMGs is their workspace also referred to as the momentum envelope.
A CMG array produces torque by changing the orientation its momentum vector.
This vector is the sum of the momentum vectors of the gyroscopes in the array.
These individual momentum vectors of the gyroscopes maintain a constant magnitude but depending on the orientation they might cancel each other out.
Therefore together they create a volume of possible momentum configurations of the array.
We can think of this of the workspace of the array whose axes are angular momentum around the three cartesian axes, meaning that the dimensions of the envelope are in Nms.

The hull or envelope of this momentum depends on the configuration of the array.
If one imagines each CMG having a momentum vector that can be gimbaled 360°, the result is a circle lying on the plane orthogonal to the gimbals axis.
The envelope then is the set of points defined by the sum multiple of such vectors through their rotation (see @Fig:cmg-momentum-envelope).

To develop a more intuitive understanding of the momentum envelope one can picture the gyroscopes being gimbaled to move the momentum vector through the volume enclosed by the envelope.
Remembering that a change in momentum is a torque we can picture how the velocity of the point moving through the momentum space is the output torque of the array.
So if we want to produce a certain torque the point begins moving in a certain direction.
At some point the point reaches the envelope and the array simply cannot produce any more torque around that axis.
The time this takes i.e. the duration which we can sustain a given torque ergo depends on the velocity of the point i.e. the magnitude of the torque.
So if our velocity in momentum space is in Nm and the distance travelled corresponds to time then it becomes understandable why our envelope is measured in Nms.

Note that close to singularities the gimbals will have to move greater amounts to achieve the same travel in momentum space just like a robots axis have to rotate further close to singularities to achieve the same travel in cartesian space.
Hence given a limited gimbal velocity and acceleration the torque dynamics will change throughout the momentum envelope.

![Example of a momentum envelope. Taken from @CitationNeeded.](./figures/cmg-momentum-envelope.jpg){#fig:cmg-momentum-envelope}

It is important to understand that the envelope is not a convex hull i.e. it intersects itself and can have additional internal surfaces.
These are the internal singularities that the steering law must avoid or be able to pass through.
See @Fig:array-envelopes for an illustration of singularities of different array types taken from [@LeveSpacecraftMomentumControl2015] where one can also find a more in depth discussion of the various types of singularities and how the different steering laws are able to take them into account.

\missingfigure{envelopes of pyramid, box and roof arrays}

The shape of workspace is some relevance to us as our requirements regarding it won't be uniform in all directions.
A pendulum will often swing around a single axis, robot tasks might be dominated by torque around certain axes and our part rotations will lie around the axis of the cranes rope.
Therefore it is of note that we can shape the workspace of an array by changing its parameters.
In the roof array this is the angle of the roof.
See @Fig:roof-array-workspace-45deg and @Fig:roof-array-workspace-30deg for a comparison of different roof angles generated with the code provided in @sec:roof-array-workspace.

![Outer (green) and inner (orange) singularities for a four CMG roof array with a roof angle of 45°.](./figures/roof-array-workspace-45deg.jpg){#fig:roof-array-workspace-45deg}

![Outer (green) and inner (orange) singularities for a four CMG roof array with a roof angle of 30°.](./figures/roof-array-workspace-30deg.jpg){#fig:roof-array-workspace-30deg}

## Sizing of CMGs

Once again Leve et al. provide a good overview regarding the sizing of spacecraft CMG [@LeveSpacecraftMomentumControl2015].
For terrestrial systems the literature is quite barren, but in their wearable SPCMG Chiu et al. do detail their sizing process [@ChiuDesignWearableScissoredPair2014].
Generally speaking though, we can note that the main characteristics of a CMG array are the torque it can produce (Nm), the agility of the torque production i.e. its acceleration (Nm/s) and then the amount of torque it can sustain i.e. its momentum envelope (Nms).
The magnitude of these requirements of course depends on the application for which the CMGs are being sized.
This application will also pose constraints for instance on torque accuracy, weight, size, vibrations and power requirements.

Looking at the sizing methods used for spacecraft, the requirements usually stem from the agility demanded of the spacecraft, also called slewrate.
Given the moment of inertia of the spacecraft, the slewrate requirement will provide a required torque and duration that it must be provided.
The given slewrate also results in a base rate whose reaction torque must be handled by the gimbal motors.
From this the sizing of the CMGs can proceed and will subsequently be controlled by the harsh constraints of of spaceflight hardware. 

This in particular is where our sizing process will diverge from spacecraft CMG design.
Weight, size power and computational resources are of much smaller concern when the goal is hanging the CMGs from a crane.
Some crane hooks have added weights which are required to ensure that the unloaded hook can overcome the rope friction in the pulley system.
Furthermore, the slewrate or in our case the rotation speed of loads is only one concern.
We must also account for the compensation of the robots motion and deal with the oscillations of the crane.
Hence, as already alluded to during the review of existing applications, we must first develop an understanding of our crane-cmg-robot system, a process discussed in the following chapter.
