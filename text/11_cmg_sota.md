
# Control Moment Gyroscope Applications

Control moment gyroscopes are an established technology in spacecraft design and have also seen some commercial terrestrial application.
This chapter starts with a brief explanation of gyroscopic reaction torque before giving an overview of historic and current applications of momentum control devices in general and CMGs in particular.
The applications have been split into three parts: spaceflight, general terrestrial and crane applications.

By investigating the various existing applications, this chapter hopes to provide a deeper understanding of the potentials and limitations of CMGs, to thereby motivate the subsequent work of this dissertation.

## Gyroscopic Reaction Torque {#sec:reaction-torque}

The behavior of gyroscopes often runs counter to intuition due the relationship between torque, angular velocity and momentum.
As it involves the cross product of their vectors, everything is constantly being rotated 90°.

Fundamental to understanding gyroscopes is that angular momentum ($\boldsymbol{h}$) is a conserved quantity i.e. it remains constant unless a torque ($\boldsymbol{\tau}$) is applied to the system.
Furthermore it helps to remember that change in angular momentum is torque ($\boldsymbol{\tau} = \frac{d\boldsymbol{h}}{dt}$).
When the applied torque is aligned with the angular momentum, the momentum simply changes in magnitude.
This happens when a motor spins a wheel or we use our fingers to spin a top.

When the torque lies orthogonal to the angular momentum, we encounter the unintuitive side of gyroscopes.
Since no component of the torque is in line with the angular momentum, its magnitude and hence the speed of the spin remain constant.
Therefore, the change in angular momentum takes the form of a change in the orientation of the angular momentum.
This is illustrated in @Fig:gyroscopic_torque.

![Illustration of how a torque that lies orthogonal to an angular momentum causes a rotation of the angular momentum’s orientation instead of a change in its size. Here $h$ denotes the angular momentum and $\omega$ is the rotational velocity that this vector is experiencing.](./figures/gyroscopic_torque.png){#fig:gyroscopic_torque short-caption="Principle of gyroscopic reaction torque"}

It is this change in orientation in the form of a rotation and its relation to the torque via the size of the angular momentum that lets us understand everything from simple toys (@Fig:precession) to the momentum control systems of the International Space Station (@Fig:iss).

![Precession of a gyroscope. Gravity would usually cause the object to topple over. Instead, the conservation of angular momentum leads to a precession, whose motion causes a torque that balances out the torque caused by gravity.(Lucas Vieira, Public Domain)](./figures/Gyroscope_precession.gif){#fig:precession short-caption="Gyroscopic precession"}

![Astronaut Dave Williams replacing one of the four dual gimbal CMGs on the ISS. (Public Domain, NASA Photo ID: S118-E-06998)](./figures/ISS-CMG.jpg){#fig:iss short-caption="CMG replacment spacewalk on the ISS"}

Before proceeding, I would like to emphasize three key points:

- the angular momentum ($\boldsymbol{h}$) acts akin to a lever between $\boldsymbol{\omega}$ and $\boldsymbol{\tau}$
- the speed at which our gyroscope spins is not affected by torque acting orthogonal to its axis of rotation
- such a torque will instead result in a rotation orthogonal to both angular momentum and said torque

The last point is essential to understanding CMGs where we do the inverse: rotate an angular momentum and thereby create a reaction torque.
This is illustrated in @Fig:CMG_principle.

![Principle of a CMG. A spinning mass i.e. a gyroscope ($\Omega$ denoting its angular velocity) has an angular momentum ($h$). By applying an angular velocity ($\omega$) orthogonal to the gyroscope's spin axis we create a reaction torque ($\tau$) orthogonal to both the gimbal axis and the gyroscope's spin axis.](./figures/CMG_principle.png){#fig:CMG_principle short-caption="Principle of a CMG"}

The torque produced by such a gimbal rotation is described by:

$$ \boldsymbol{\tau} = \boldsymbol{\omega} \times \boldsymbol{h} $${#eq:reaction_torque}

Within a CMG the torque required to rotate the gimbal so as to produce a given rate $\boldsymbol{\omega}$ is independent of the angular momentum $\boldsymbol{h}$ of the gyroscope.
The gimbal motor only has to overcome the rotational inertia of the gyroscope and the surrounding gimbal bearings etc.
Yet since the torque of the CMG also depends on the angular momentum of the spinning gyroscope, we can increase the output torque of the CMG simply by increasing the spin speed of the gyroscope.

This is where the lever analogy is really appropriate:
Just as a longer lever enables us to produce a greater output force with the same input force, so can a greater angular momentum (e.g. faster spinning gyroscope) enable us to produce a larger output torque with the same gimbal motor.
Since the gyroscope's motor only needs to overcome the bearing friction once it has reached the desired speed, CMGs enable us to produce very large torques with comparatively small motors.
Leve et al. mention terrestrial systems capable of output in excess of 100,000 Nm that require only a few kWs to operate [@LeveSpacecraftMomentumControl2015, p. 46].
This is quite remarkable when compared with e.g. a Tesla Model S motor which produces 1,250 Nm using 581 KW.

Unfortunately there is a caveat.
@Fig:CMG_principle shows that the produced torque is applied to the body via the bearings of the gyroscope and those of the gimbal.
This of course means that gimbals must be sized accordingly, but the greater issue occurs when the body containing the CMG happens to rotate around the axis of our output torque.
In such a case the angular momentum lever becomes a problem, as it now leads to a large torque being put on the gimbal motor.
Sizing the motor to accommodate for such cases can quickly negate the advantage provided by a CMG and this will be discussed in the later sizing sections (see @Sec:torque-issue).

## Applications of CMGs

This section will cover a selection of CMG applications.
Given their properties CMGs have a very narrow field of utility.
With most of the research surrounding CMGs coming from space exploration, a brief historic review of CMGs in space will illustrate how the understanding of the fundamental principles of CMGs has evolved.
The subsequent section covers the few terrestrial fields of application and serves to illustrate some of the challenges and limitations of CMGs.
The final section covers prior work on stabilizing cranes with gyroscopes.

### Development of CMG Technology and Spacecraft Application { #sec:space-cmg-sota }

The need to produce a torque without having something to push off from does not occur frequently.
Given sufficient speed, even a plane can push off the air surrounding it.
This explains why momentum control devices are mostly associated with space flight.
Leve, Hamilton and Peck have summarized the work in this field in their book _Spacecraft Momentum Control Systems_ [@LeveSpacecraftMomentumControl2015].

For small spacecraft, reaction wheels are common and provide a straightforward means of transferring the torque of a motor to the spacecraft.
Reaction wheels consist of a single motor attached to a disc or wheel.
It is in larger craft with higher torque demands that the lever effect of CMGs becomes essential.
The first CMGs to fly in space were three dual gimbal CMGs attached to Skylab.
Dual gimbal CMGs are less efficient than single gimbal CMGs, as the torque produced is always transferred in part through a gimbal motor, whereas in a single gimbal design it will be transferred via the bearings.
However there are several reasons why Skylab and many subsequent spacecraft including the ISS use dual gimbal CMGs.

As a gimbal rotates to produce torque with the gyroscope, so does the orientation of the output torque vector.
This gives rise to complex steering laws and issues with singularities (See @Sec:glossary for explaination of singularities).
The Apollo program did not use CMGs, but did use three gyroscopes for inertial measurement of the spacecraft’s orientation.
These gyroscopes were suspended in three nested gimbals, providing feedback regarding the spacecraft's yaw, pitch and roll.
The decision only to use three gimbals led to more frequent issues with gimbal lock (a singularity where the gimbal axis align) than was expected during multiple Apollo missions[^collinsxmas].
Given the limited computational resources and understanding of CMG steering laws at the time, it is very understandable that NASA chose to go with dual gimbal designs, which eliminate the internal singularities on the CMG array.

[^collinsxmas]: The Apollo guidance computer had to include functions to alert the astronauts to an impending gimbal lock and Mike Collins joked that all he wanted for Christmas was a fourth gimbal as he was repeatedly resetting the gimbals during Apollo 11.

The attitude control systems for the first spacewalks of the US program took a different approach.
By mechanically linking two CMGs so that they mirror each other’s motion, one can create a scissored pair CMG array.
Here the sum of the two gyroscope's momentum vectors always lies along a single axis, making for much simpler steering (see also: @Fig:spcmg-steering and @Sec:spcmg-steering).
The disadvantage is that one has to use six, instead of three CMGs to be able to produce torque around three axes (i.e. three degrees of rotational freedom).

Over the years, several ways to array single gimbal CMGs and associated steering laws with singularity avoidance have been developed.
Since redundancy is imperative in space flight, the arrays usually use four CMGs, unless other momentum control devices are also included in the spacecraft.
The three common arrays for CMGs are box, pyramid and roof (see @Fig:sg-cmg-configurations).
Leve et. al recommend roof arrays due to their simpler and easier to avoid internal singularities.

![Various configuration options for single gimbal CMGs [@KurokawaGeometricStudySingle1998]](./figures/sg-cmg-configurations.jpg){#fig:sg-cmg-configurations short-caption="Configurations for single gimabl CMGs"}

Momentum control devices such as reaction wheels, CMGs or magneto-torquers[^magnetotorquers] enable spacecraft to adjust and control their orientation without expending fuel.
This makes them invaluable, given weight and volume constraints in space flight.
However, these systems are also of value in attempts to add robot arms to spacecraft.

[^magnetotorquers]: Magneto-torquers rely on electro-magnets interacting with the earth's magnetic field.

Whilst the ISS has a remote controlled arm, the control of this arm is not coupled with the attitude control system (ACS) of the ISS.
The ACS simply continues to try and maintain the ISS in the desired orientation.
This is possible due to the very large moment of inertia that the ISS possesses.

The only other robot arm to have operated in space is that of the ETS VII research satellite (see @Fig:ets-vii-space-robot and [@OdaSummaryNASDAETSVII2000]).
The goal of this research was to study how one satellite might capture another spacecraft for repairs or even just removal of space debris.
The mission's experiments were performed using both programmed motions as well as remote control operation, both with the speed limited to 2mm/s.
Such low speeds were necessary to ensure that the ACS of the spacecraft could maintain its orientation.
Note that such speeds are orders of magnitude below those of earthbound industrial robots.

Using the ETS VII satellite, Yoshida et al. were able to show the efficacy of reactionless motion planning using so called reaction-null-space [@yoshida_zero_2001].
These are sets of movement that produce zero reaction torque at the base of the robot.
Such movements are very limited for conventional 6 DoF arms, making the approach suitable for arms with kinematic redundancy.

While the ETS VII is the only such system to fly in space, there has been a lot of research into robot arms in space (see [@ReintsemaDLRAdvancedTelerobotic2007] for a review), with the first robot arm flying as an experiment aboard the space shuttle Columbia [@HirzingerROTEXtheFirstRemotely1994].
Besides the above mentioned motion planning using reaction-null-space, other methods have been proposed to reduce the base reactions caused by the robot movement (see introduction of [@li_motion_2013] for a good summary).
These include the coordination of a second robot to compensate the torques of the first robot [@yoshida_dual_1991].
The authors show the efficacy of the approach, also with regard to energy consumption, but it must be assumed that adding a second arm just to be able to compensate the other would be less efficient than more powerful momentum control devices.
Nevertheless, this work will be valuable if more than one robot is to be attached to a crane, especially as it would also be able to assist in maintaining the center of gravity.
Other works have studied how one might coordinate the ACS and robot actuation to optimize their utilization while maintaining the satellite's attitude as well as robot path accuracy [@li_motion_2013; @JayakodyRobustAdaptiveCoordination2016; @ShiRobustAttitudeController2016; @WuRobustAntiDisturbanceCoordination2018].
Others have proposed using CMGs as the actuators of the arm to create kinematics capable of moving in space without exerting torques on their host spacecraft [@carpenter_reducing_2009].
To ensure accurate compensation and robot motion, methods for the identification of a systems inertial parameters after launch have been proposed [@XuOnorbitIdentifyingInertia2017].

![Artists rendition of the ETS VII research satellite used to evaluate the use of robot arms to manipulate other satellites (bottom right, source: JAXA [@JAXAEngineeringTest]). The satellite during ground tests (left, source: ESA Bulletin [@VisentinTestingSpaceRobotics1999]) and overview of its robot setup (top right,[@OdaSummaryNASDAETSVII2000])](./figures/ets-collage.png){#fig:ets-vii-space-robot short-caption="The ETS VII research satellite"}

### Terrestrial Applications

Looking to terrestrial applications, we mostly see CMGs being used to stabilize vehicles.
Attitude control with CMGs makes little sense on earth, as most vehicles need to rotate at velocities that are not feasible for CMG-based control, given the high reaction torques that would have to be sustained by the gimbal motors.
As we have the ground, water and air to push off from, we usually can use wheels, fins and wings instead.

Therefore CMGs find terrestrial application where such systems do not work: two-wheeled vehicles that should remain upright at slow speeds or a standstill and roll stabilization for ships at rest.
Early examples of both applications can be found.
For ground vehicles there is a gyrocar commissioned in 1912 by Pyotr Petrovich Shilovsky who also built a monorail and wrote a book on the uses of gyroscopes in 1924 [@ShilovskiiGyroscopeItsPractical1924].
Ships of the same period saw the construction of probably the largest ever CMGs (regarding size), with the first deployment to a large passenger liner, the Conte di Savoia in 1931 [@RexConteDi].
The gyroscope weighed in 175t and spun at 910 rpm (see @Fig:conte-gyro).
Given that control engineering or cybernetics had not yet been established, these systems presumably operated on a passive control principle.

![Gyro stabilizer aboard the Conte di Savoia passenger liner launched in 1934.](./figures/conte-di-savoia.jpg){ #fig:conte-gyro short-caption="Gyroscopic stabilizer for a passenger ship"}

The way that such passive stabilization with gyroscopes works is as follows:
The tipping vehicle exerts a torque orthogonal to the gyroscope’s momentum and the gimbal’s axis.
This causes the gyroscope to precess around the gimbal axis, a movement that in turn causes a reaction torque counter to the tipping motion of the vehicle.
If the gimbal resists the precession, for instance through friction, this torque also acts against the torque causing the excitation.

The low speeds of the motors available back then as well as the much simpler solution of adding further wheels or putting a foot on the ground are why gyroscopically stabilized ground vehicles did not become popular in the early 20th century.
There have, however, been subsequent attempts at producing gyro cars.

In the late sixties a team around Thomas Summers, who had worked on guidance gyroscopes in the war, and the car designer Alex Tremulis, built the Gyro-X prototype.
The goal was to increase road capacity and improve aerodynamics by slimming a car to two wheels, but the team went bankrupt before they were able to solve the engineering challenges involved in actually keeping the car stable.
A recent startup called Lit Motors also attempted to produce a similar two-wheeled car and filed multiple patents [@KimElectronicControlSystem2013] (see also @Fig:litmotors).
News surrounding the company went silent after an initial flurry of coverage around 2012 and some speculate that they were not able to reduce noise and vibrations sufficiently to create a usable consumer experience, but they have recently relaunched their [website](https://www.litmotors.com).
For a discussion as well as a derivation of equations of motion and control systems for stabilization of two-wheeled vehicles see [@SpryGyroscopicStabilisationUnstable2008].
In this paper the authors also extend the equations of motion to use two gyroscopes of opposite spin direction and show how this benefits control performance.

![Prototype of the Lit Motors C1 gyro-stabilized vehicle being driven on the webseries _Spark_ produced by Maker Studios](./figures/litmotors.gif){ #fig:litmotors short-caption="Lit Motors gyro-stabilized two-wheeler prototype"}

Even though roll stabilizing gyroscopes went out of fashion for ships as hull and fin designs improved, they have become a commercial product offered by multiple companies (see @Fig:seakeeper for an example).
Their target market are yachts as well as commercial vessels, where roll stabilization at rest or slow speeds is of greater importance.
The CMGs here are the largest CMGs commercially available today, since satellites require much lower torques.
It is therefore unsurprising that a naval CMG was used in the recent resurrection of the Gyro-X at the Lane Motor Museum.
It is also worth pointing out that some naval CMGs use the energy stored in the spinning gyroscope to provide additional electrical power during peaks in electrical load caused by the actuation.
This was also considered for spacecraft, but as spacecraft batteries have reached a similar energy density to high-speed flywheels, the added weight of the required electronics and challenges of high velocity gyroscopes in space have led to this idea being discarded.

![Marketing video for a ship-stabilizing gyroscope [@SeakeeperGyroStabilizers]. The left boat is being stabilized, the right one is not.](./figures/seakeeper.gif){ #fig:seakeeper short-caption="Current ship stabilizing gyroscopes"}

The gyroscopes used in naval CMGs are large enough to warrant a vacuum to reduce friction and are actuated using hydraulic systems.
Filed patents point towards interesting engineering challenges [@AdamsGyroscopicRollStabilizer2005], for instance regarding the cooling of the gyroscope bearings [@AdamsCoolingBearingsMotors2009].

Given the passive stabilization principle discussed earlier, one might surmise that no actuation is required.
The actuation is required to ensure that the gyroscope does not reach a singularity and also to limit the precession speed and thereby the output torque.
Given the size of the gyroscopes and bearings involved, the actuation is also required to assist the gyroscope in overcoming friction.
This is relevant during small excitations, where the friction might introduce a significant time delay in the system’s reaction.

Researchers have also proposed other applications for CMGs (see @Fig:other-terrestrial).
The most exotic is probably the use of a CMG to stabilize a beating heart during surgery [@GagneCardiacMotionCompensation2009; @GagneGyroLockStabilizingHeart2012].
Several researchers have also built CMGs into devices aimed at stabilizing human gait to e.g. assist the elderly [@ChiuDesignWearableScissoredPair2014; @LiGyroscopicAssistanceHuman2012].
Others have suggested using CMGs to orient underwater robots to allow attitude control at zero velocity and with fewer thrusters (initially proposed in 2005 [@ThorntonInternalActuationUnderwater2005], further examples:[@ThorntonZeroGClassUnderwater2007; @YimeDesignCMGUnderwater2011; @PenaAdvancesDevelopingTelemanipulators2009]).
Others have used reaction wheels instead of CMGs to create small, self-assembling robots that move by flipping themselves [@RomanishinMblocksMomentumdrivenMagnetic2013].
A quite well known example of momentum control is the Cubli, a self-balancing cube that also uses reaction wheels [@GajamohanCubliCubeThat2012].

![Other terrestrial applications proposed by researchers. From left to right: human gain stabilization [@ChiuDesignWearableScissoredPair2014], stabilizer for heart surgery [@GagneCardiacMotionCompensation2009; @GagneGyroLockStabilizingHeart2012] and underwater robot [@PenaAdvancesDevelopingTelemanipulators2009].](./figures/other-terrestrial-applications.png){ #fig:other-terrestrial short-caption="Other proposed terrestrial CMG applications"}

### Crane Applications

Given that there were significant efforts to automate construction in Japan and Korea dating back to the 1980s, it is unsurprising that research into the actuation of cranes has been done in these countries.
The earliest literature relevant to cranes is from 1994 and concerned the stabilization of a passenger gondola.
It uses a SPCMG with two 30kg flywheels to compensate wind excitation [@KankiDevelopmentCMGActive1994] (see @Fig:KankiDevelopmentCMGActive1994).
In 1997 a patent was filed on adding a motor to a crane hook to rotate the load [@gimseoghoHookBlockPossible1997].
In such a case the motor would have had to push off against the crane cable’s resistance to twisting.

A paper from 1998 describes field testing of a device using a single CMG [@InouePracticalDevelopmentSuspender1998] (see @Fig:InouePracticalDevelopmentSuspender1998).
The authors also mention previous work that utilized fans or propellors to actuate a crane's load [^langbarrier].
The authors also analyzed how the device improved assembly times and reduced dangerous work.
The greatest improvement was in tasks that involved the rotation of the load.
Here the work duration was roughly halved and nearly all work they classified as dangerous was eliminated.
Their device used the passive stabilization principle during transport and a remote controlled actuation to cause the load rotation.

[^langbarrier]: No English or German sources could be found that further detail this approach.

Yi et al. have published several works on stabilizing beams during construction work (see @Fig:SaAttitudeControlStabilization2001) and [@YiImplementationGyroActuator1999; @YiAttitudeControlStabilization2000; @SaAttitudeControlStabilization2001].
Starting with a single CMG hanging from a single rope, their subsequent publications (one having only the abstract available in English) discuss the addition of an IMU since the rotary encoder attached to the single rope was too inaccurate.
They also confront the same issue as naval CMGs, namely that slow rotations are not able to overcome the gimbal friction.
Their last paper adds a clutch to the gimbal to avoid overloading the gimbal motor during passive stabilization.
In [@LeeAnalysisFieldApplicability2012] the authors use a motorized hook to rotate beams (see @Fig:LeeAnalysisFieldApplicability2012).
The authors also filed two patents with regard to ways of powering such a hook, one proposed a clock spring with the other proposing to use the vertical hook travel to power the device.
They incorrectly discuss [@InouePracticalDevelopmentSuspender1998], stating that the authors were only using passive stabilization.
More recently researchers have once again used a single CMG to stabilize the yaw of a load attached to a model jib crane [@KodaniTransportingRotatingControl2017] (see @Fig:KodaniTransportingRotatingControl2017).
The authors run into difficulties with the singularity and changing orientation of the output torque.

![CMG pair used to stabilize a gondola against wind excitation [@KankiDevelopmentCMGActive1994].](./figures/KankiDevelopmentCMGActive1994.png){ #fig:KankiDevelopmentCMGActive1994 short-caption="CMG based gondola stabilization"}

![Single CMG device used in field tests [@InouePracticalDevelopmentSuspender1998].](./figures/InouePracticalDevelopmentSuspender1998.png){ #fig:InouePracticalDevelopmentSuspender1998 short-caption="Single CMG crane stabilization field test"}

![Illustration of beam stabilization setup from [@SaAttitudeControlStabilization2001].](./figures/SaAttitudeControlStabilization2001.png){ #fig:SaAttitudeControlStabilization2001 short-caption="Illustration of beam stabilization with CMG"}

![Motorized crane hook experiments [@LeeAnalysisFieldApplicability2012].](./figures/LeeAnalysisFieldApplicability2012.png){ #fig:LeeAnalysisFieldApplicability2012 short-caption="Motorized crane hook experiments"}

![Single CMG experiments on a model jib crane [@KodaniTransportingRotatingControl2017].](./figures/KodaniTransportingRotatingControl2017.png){ #fig:KodaniTransportingRotatingControl2017 short-caption="CMG stabilization of jib crane model"}

The concept of using CMGs to rotate a load hanging from a crane has recently been turned into a commercially available product by the Australian company Verton.
Founded in 2014 they published a patent regarding the rotational control of a crane load with gyroscopes in 2017 [@THOMSONMaterialsManagementSystems2017].
The product is called R-Series, was launched in 2019 and is currently available for 20 and 5 tonne loads.
Their marketing material focusses on the increased worker safety and reduced handling times, as also covered in prior work by [@InouePracticalDevelopmentSuspender1998].

From the patent filing and limited information available on their website it appears that they use two single gimbal CMGs with the ability to add further CMGs as modules.
The introduction of the patent discusses the issue of how reaction torque interferes with manual rotation of the load.
Given the use of two gyroscopes I would assume they are using a scissored pair array.
By rotating the two gimbals in the same direction (as opposed to mirrored) it should be possible to align the gyroscopes' axes of rotation with that of the load without exerting any torque on it, thereby placing the device in a state that does not interfere with manual rotation.

![The R-Series is a commercially available load rotation device that uses gyroscopes and was launched by the Australian company Verton in 2019. (Picture by Rod Pilbeam)](./figures/Verton_20180115_082.jpg){ #fig:verton short-caption="Commercially available load rotation device"}

## Summary

The idea of using gyroscopic effects for stabilization is an old one.
Yet following this review of existing applications, it appears that a solution for the idea of stabilizing a robot hanging from a crane cannot easily be extrapolated from the existing applications of CMGs.
Unlike a satellite or spacecraft we are predominantly interested in maintaining a given position, not in rotational agility.
The oscillations and dynamic behavior of cranes will differ from those of ships, and unlike ships we have to deal not only with roll, but also pitch and yaw.
It is this three-dimensional requirement that also sets this challenge apart from the previous work with CMGs and cranes.

The trajectory optimizations proposed for space robotics can most likely be adapted to our purpose, but cannot be applied directly due to the stark differences between spacecraft and crane dynamics.
For instance, in space the torques produced by the robot will always only rotate the spacecraft, whereas attached to a crane we will also have to deal with translations caused by robot motions and other external forces.

We will have to develop an understanding of crane-CMG dynamics to allow us find a way to consolidate the different control and sizing requirements.
On the one hand we have a system at rest being excited by e.g. a robot and on the other hand a system in an oscillatory state that needs to be dampened.
