
# Introduction

The following is a documentation of efforts to understand whether it would be possible to operate a robot hanging from a crane.
Given the desire of increasing automation in the construction industry the ability to extend the working area of conventional industrial robots by hanging them from cranes could be of great use and impact.

This introduction begins with a summary of why construction robots are of interest, their current availability and abilities.
The second section elaborates why hanging robots from cranes is of interest.
It briefly introduces the focus of this work on momentum control devices and this compares to other approaches that use parallel tendon kinematics or flying drones.
The potential abilities and applications of the approach taken in this work are also outlined.

Finally the structure and content of this work is introduced.

## The Need for Construction Robots

Construction is and will continue to face significant challenges:
Our urban population is rising [@PopulationDivision-UnitedNationsWorldUrbanizationProspects], necessitating not only the creation of significant amounts of new building stock, but also the densification and upgrading of existing stock.
Furthermore we must reduce the impact on the environment of our buildings and their use.
At the same time climate change has already resulted in increasingly extreme weather conditions and changes to the climate conditions that our buildings have to withstand.
Many so called developed nations are also facing shortages in skilled construction workers [@MorrisonConstructionLaborShortage], not only due to the aging population and unattractive working conditions, but also due to reliance on cheap foreign labour.
The latter has caused many sectors in construction to stagnate technologically as innovation was more costly than masses of cheap labour [@ArntzDigitalisierungUndZukunft].

Fortunately, technological advances have led other industries to develop means for greater individualization and increased flexibility in their production.
Looking at earlier attempts at automating construction (particularly in Japan and Korea during the 80s), one can see how the technology of the day was unable to provide said individualization and flexibility required in construction [@BockConstructionRobotsElementary2016; @BockRoboticIndustrializationAutomation2015; @BockSiteAutomationAutomated2016].
With robots, sensors and fast computing becoming more ubiquitous, we are finally seeing the emergence of construction robotics.

First examples of these new on-site, commercially available robots are [SAM100](https://www.construction-robotics.com/) the brick-laying robot and [Tybot](https://www.tybotllc.com/) the rebar-tying robot for bridge decks.
Robots have also entered the preproduction of buildings and we are slowly seeing more direct links between digital planning and individualized robotic execution.
As industrial robots enter the construction industry, the existing construction machinery is also becoming more sophisticated.
Dump trucks are already driving autonomously in open pit mines and excavators and other machines are being fitted with sensors and digital controls.

The availability of digitally-controllable machinery has always been key to increasing automation and individualization.
Such machines are the bridge from digital planning to execution in the real world.
As such it is wonderful to see the emergence of programmable machines suited for the construction site.
Yet one aspect of the construction site is not addressed by the existing range of adapted industrial robots and upgraded construction machinery: the sheer size of construction sites.

## Turning Cranes into Robots

The ability of cranes to provide logistics over large spans and at great heights has transformed construction since antiquity.
They are the kinematic systems of choice for the large scale of construction sites, naval operations and large scale assembly tasks.
However, the key to their success is also the reason for the limitation of their automation.
Using a rope as the last link of their kinematic chain, cranes are able to cover height with a minimum of material.
The flexibility of the rope also means that it requires extremely little space when retracted, as it can be coiled and wound around winches.
Yet this flexibility also means that the rope cannot be used to push, only to pull.
With the actors (the motors) of the crane connected to the end effector (the hook) via a flexible connection, it is difficult to produce controlled motion in the event of disturbances.
If robots are to be used over the large work area of the construction site effectively, they must be provided with a stable work platform.

TODO: elaborate on instability and how a robot introduces disturbance

![Overview of forces preventing stable operation of e.g. a robot suspended from a crane: a) center of gravity (CoG) of the hook/platform moves out of equilibrium, b) robot CoG gets moved out of equilibrium, c) forces and torques acting at robot base due to motion of robot, d) forces and torques stemming from interaction with external objects, e) external forces e.g. wind. Note that these all interact.](./figures/crane-robot-forces.svg){short-caption="Forces acting on a robot hanging from a crane"}

### Momentum Control Devices

Such a platform must be capable of compensating the torques and forces acting on the base of the robot as it performs its task.
If we wish to use the proven technology of construction cranes, we need to find a way of creating counteracting forces and torques in the middle of space.
Fortunately, spacecraft face a similar issues, having to maneuver without having land or air to push off from.
Whilst spacecraft are usually known for their use of rocket and other propulsive devices, they also usually have means of producing torque without expending fuel.
This feat is achieved through momentum control devices and this work will discuss the feasibility of using a specific type of these, called control moment gyroscopes (CMG), to enable construction robots for large work envelopes.

### Alternative Approaches

A well studied approach for large workspaces are parallel tendon kinematics.
Here, instead of a single rope positioning the end effector, multiple ropes/tendons are used.
By spanning these tendons from different directions, it becomes possible to create stable positions and motions over large spaces.
Such systems are commercially available for cameras in sports stadiums and researchers have proposed their use for a variety of other tasks.

The RoboCrane was originally a DARPA project at NIST that was proposed for several applications [@james1993nist] including construction [@LytleIntelligentJobSite2003; @GoodwinRoboCraneConstructionBridges1997].
Other systems such as the Fraunhofer Institute’s IPAnema have been aimed at logistics [@PottIPAnemaFamilyCableDriven2013].
More recently there have also been further conceptual proposals for the use of parallel tendon robots on construction sites [@SousaSPIDERobotCableRobotSystem2016] as well as large scale 3D-printing efforts that utilize parallel tendon research prototypes [@IzardLargescale3DPrinting2017] (see @Fig:parallel-tendon-print).

![Rendering of a 3D-printing concept for construction sites [@IzardLargescale3DPrinting2017]](./figures/parallel-tendon-printing-izard.png){ #fig:parallel-tendon-print short-caption="Rendering of a 3D-printing construction site concept"}

Parallel tendon kinematics come with some challenges and disadvantages.
Dealing with tendon elasticity is particularly relevant to vibrations in the system.
Depending on the size of the end effector platform, the systems will also struggle to produce high torques, as these depend on the amount of leverage that the tendons have on the platform.
Some researchers have therefore added momentum control devices to compensate torques in parallel tendon kinematics [@WeberActiveVibrationCanceling2014], which point to interesting hybrid approaches (see @Fig:reaction-wheel-tendon).
The bigger issue for construction sites will most likely be the need for the tendon's winches to be placed around the workspace of the system.
This means that tendons would be required to cross large areas of the construction site, which again would pose significant challenges with regard to collisions, setup costs as well as worker safety.

![Experiments with dampening a parallel tendon platform using reaction wheels [@WeberActiveVibrationCanceling2014]. The left example is not using the reaction wheels. On the right, one can see them being used and rotating at the top of the platform.](./figures/reaction-wheel-tendon-gangloff.gif){ #fig:reaction-wheel-tendon short-caption="Parallel tendon plattform damplened with reaction wheels"}

Drones are the only system on a construction site with a workspace larger than cranes.
They are therefore seeing use as an inspection, surveying and monitoring tool.
They have also been proposed as a logistics and robotics platform for infrastructure (see [ARCAS EU Research Project](http://www.arcas-project.eu) and @Fig:flying-robot).
Given the weight of construction materials, drones’ small payload capabilities in comparison to cranes severely limits this approach.
Their need to compromise flight time with battery weight is an additional constraint of drone based approaches.
It seems relevant to point out that the building materials of some widely publicized drone-based constructions are foam blocks [@GramazioKohlerFlightAssembledArchitecture2011], nylon ropes [@MirjanBuildingBridgeFlying2016; @AugugliaroBuildingTensileStructures2013] and carbon fibers [@SollyICDITKEResearch2018].
The use of propulsive systems (e.g. propellors) to rotate or stabilize crane loads has been mentioned in the literature and apparently there were experiments made in Japan or Korea [@InouePracticalDevelopmentSuspender1998], but sadly the results of these experiments are not available.

![Excerpt from the 4th year report of the ARCAS project on collaborative flying robots for maintenance and construction. The consortium also performed experiments with a kerosine-fueled drone/helicopter capable of carrying a DLR LBR robot arm.](./figures/arcas.gif){ #fig:flying-robot short-caption="EU ARCAS project on flying robots"}

While mobile platforms in robotics are starting to enter industrial use, they are not able to provide the vertical reach of cranes.
For small heights, linear axes can be added to the mobile platforms to increase the reach of their robot arms.
Some have proposed attaching industrial robot arms to other systems to enhance their reach and construction site mobility.
One example from research is the Digital Construction Platform by the MIT Media Lab [@KeatingCompoundArmApproach2014] (@Fig:dcp-media-lab).
Others have attached articulated arms to hydraulic remote controlled demolition robots for use in nuclear decommissioning [@BurrellFeedbackControlBased2016].
Apart from their vertical and horizontal reach, a further benefit of cranes can be their small footprint relative to their horizontal reach.
Mobile platforms, on the other hand, would have to be provided with access via the ground.

![The Digital Construction Platform that combines an industrial robot with a hydraulic arm to increase its reach. The red line has been drawn by the end of the hydraulic arm and the blue line by the small robot attached to it. [@KeatingCompoundArmApproach2014]](./figures/dcp-mit-media-lab.jpg){ #fig:dcp-media-lab short-caption="Digital Construction Platform by the MIT MediaLab"}

### Potential Applications

In comparison to the alternatives covered above, @Fig:baugrok-applications illustrates the potential abilities of the proposed system of stabilizing a crane hook with momentum control devices.
Generally speaking, it would add the ability to produce controlled torques at the hook of a crane without requiring any additional ropes or other kinematics.
The control moment gyroscopes would allow for the compensation of the torques produced by a robot's motion or other processes suspended from the hook.
They would also provide control over the rotation of parts during transport and assembly operations.
Furthermore they could assist in dampening crane oscillations.

These abilities could result in novel applications of cranes, not only on construction sites.
Components could be moved with greater control for logistics and assembly operations.
By increasing the control of the motion safe automation of such tasks becomes possible.
The ability to compensate provess torques also make it possible to use additional kinematic systems, be they specialized or general purpose e.g. industrial robots.
Examples of these applications are illustrated in @Fig:indoor-and-outdoor.

![Abilities of a CMG-stabilized crane. From left to right: process compensation, part rotation and dampening of pendulum oscillations.](./figures/baugrok-applications.gif){ #fig:baugrok-applications short-caption="Abilities of a CMG-stabilized crane"}

![Potential applications of a CMG-stabilized crane. From left to right: part transport with gantry cranes, transport and assembly of components on a construction site, mobile industrial robots.](./figures/indoor-and-outdoor-applications.png){ #fig:indoor-and-outdoor short-caption="Potential applicans of a CMG-stabilized crane"}

## Outline of work

The focus of this work is understanding the potential of CMG-based crane stabilization.
[Chapter @Sec:cmg-sota] therefore introduces the fundamental principle of CMGs.
It then goes on to discuss their use in spaceflight as well as terrestrial systems for maneuvering and stabilization.
The idea to utilize gyroscopes to stabilize cranes is not new and so special attention is given to previous research in this field.
This chapter thereby motivates this work by identifying areas not covered by existing research.

Following this, [chapter @Sec:cmg-theory] summarizes the existing theory on CMGs as it pertains to this work.
The majority of this chapter is spent on introducing and explaining the dynamics of CMGs before moving on to the sizing and steering of them.
The chapter thereby outlines the constraints of CMGs and limits of the existing models.

With the fundamentals of CMGs covered, [chapter @Sec:modeling-cmg-crane] develops the models required for assessing the core question of this work: how do the crane, robot and CMGs interact.
The chapter begins by identifying and approximating the parameters of a crane that affect the crane-CMG-robot interaction.
Following this a model is derived that approximates the crane and its load as a double pendulum.
The load in this case being the CMGs, any kinematic systems and or any payloads hanging from them.
To model the CMG, robot and other external forces the double pendulum model is then further extended.

[Chapter @Sec:controller-design] describes and structures the control problems of the crane-CMG system in its various applications.
After an overview regarding crane control theory a simple controller for dampening osciallations is choosen and described.

The [chapter @Sec:experiments] on experiments begins by validating the double pendulum model's behaviour through simulations before evaluating the choosen dampening controller.
The second section investigates the interaction of the dampening controller with the steering law of CMGs using a scissored pair CMG array as an example.
The previously developed model allows for an analysis of how the different torques interact, which is of great importance when it comes to sizing consideration.
The third section covers the generation of example forces and torques as generated by a robot's motion.
These forces and torques are used in the subsequent section to simulate the motion of a robot hanging from a crane and how the use of CMGs can reduce the deviation from the target path.
The chapter closes with a discussion of the hardware prototype built in parallel to this work.

Building upon the insights gained from the the modelling and experimental chapters, [chapter @Sec:sizing] develops a sizing methodology for the CMGs in a crane-CMG system.
It begins by discussing how the sizing requirements and constraints arise from the various use cases of CMGs for crane stabilization.
Subsequently the relationships between the constraints are discusses and how the sizing for crane-CMG systems differs from other CMG applications.

The insights gained during this work are summarized in [chapter @Sec:outlook] and used to derive the key challenges for further work.

Some specialized terminology is explainind in a glossary ([chapter @Sec:glossary]) and the appendix ([chapter @Sec:appendix]) includes the python implementations of the models.

--------------------

Construction robotics is a field heavily reliant on interdiscplinary collaboration.
Therefore this thesis aims not only to be of use to engineers interested in dynamic systems and their control.
Instead the intention is that, by covering certain fundamentals in greater detail, this work will be of use to architects, civil engineers and roboticists alike enabling them to understand the potentials and challenges of hanging a robot from a crane.
