
# Introduction

The following is a documentation of my efforts to understand whether one could make it possible to operate a robot hanging from a crane.
Instead of using parallel tendon kinematics, i.e. additional ropes, I choose to study how one might use control moment gyroscopes and the torque they can provide, to stabilize the hook.

This work was initiated by and took place at the relatively young chair for _Individualized Production in Architecture_.
The chair is part of the architecture faculty, but also includes researchers from computer science, mechanical as well as civil engineering and generally speaking people that whose backgrounds defy easy categorization.
We believe such interdisciplinarity to be essential to solving many of the problems our built environment faces.

Therefore this thesis aims to not only be of use to other engineers well versed in dynamic systems and their control.
Instead I hope that by covering certain fundamental is greater details, this work will be of use to architects, civil engineers and roboticists alike.
That they each may understand the potentials and challenges of hanging a robot from a crane.
With this in mind, the following work contains a basic introduction to control moment gyroscopes, models for the simulation of the crane-CMG-robot system as well tools for the sizing of CMGs for crane applications.

------------

The original idea and subsequent work captured in this thesis have been submitted as a patent application [@HaarhoffVorrichtungZurSteuerung].
Therefore many of the ideas and solutions in this thesis are part of said application, in particular the control flow and integrated approach to address multiple applications with a crane-CMG.

![Photomontage of robots suspended from a tower crane performing facade assembly. Taken and adapted from the (rejected) SEED-Fund application that initiated this work.](./figures/crane-robot-montage.jpg)

## The Need for Construction Robots

Construction is and will continue to face significant challenges:
Our urban population is rising [@PopulationDivision-UnitedNationsWorldUrbanizationProspects], necessitating not only the creation of significant amounts of new building stock, but also the densification and upgrading of existing stock.
Furthermore we must reduce the impact of our buildings and their use on the environment.
At the same time climate change has already resulted in increasingly extreme weather conditions and changes to the climes that our buildings have to handle.
Many so called developed nations are also facing shortages in skilled construction workers [@MorrisonConstructionLaborShortage], not only due to the aging population and unattractive working conditions, but also due to the reliance on cheap foreign labour.
The latter has caused many sectors in construction to stagnate technologically as innovation was more costly than masses of cheap labour [@ArntzDigitalisierungUndZukunft].

Luckily, the technological advances have led other industries to look to stark individualization and increasing flexibility in their production.
Looking at earlier attempts at automating construction (particularly in Japan and Korea during the 80s), one can see how the technology of the day wasn't able to provide said individualization and flexibility required in construction[@BockConstructionRobotsElementary2016, @BockRoboticIndustrializationAutomation2015, @BockSiteAutomationAutomated2016].
With robots, sensors and fast computing becoming more ubiquitous, we are finally seeing the emergence of construction robotics.

The first examples of on-site, commercially available robots exist with [SAM100](https://www.construction-robotics.com/) the brick laying robot and [Tybot](https://www.tybotllc.com/) the rebar tying robot for bridge decks.
Robots have also entered preproduction of buildings and we are slowly seeing more direct links between digital planning and individualized robotic execution.
As industrial robots enter the construction industry, the existing construction machinery is also becoming smarter.
Dump trucks are already driving autonomously in open pit mines and excavators and other machines are being fitted with sensors and digital controls.

The availability of digitally controllable machinery has always been key to increasing automation and individualization.
Such machines are the bridge from digital planning to execution in the real world.
As such it is wonderful to see the emergence of programmable machines suited for the construction site.
Yet one aspect of the construction site isn't covered by the existing fare of adapted industrial robots and upgraded construction machinery: the sheer size of construction sites.

## Turning Cranes into Robots

The ability of cranes to provide logistics over large spans and in ever greater heights, has transformed construction since antiquity.
They are the kinematic systems of choice for the largest of scales.
But the key to their success is also the reason holding back their automation.
Using a rope as the last link of their kinematic chain, cranes are able to cover height with a minimum of material.
The flexibility of the rope also means that it requires next to no space when retracted, as it can be coiled and wrapped.
Yet this flexibility also means that we can't use a rope to push, only to pull.
With the actors (the motors) of the crane connected to the endeffector (the hook) via such a flexible connection, it isn't possible to produce controlled motion in the face of disturbances.
If we wish to effectively use robots over the large work area of the construction site, we must find a way to provide them with a stable work platform.

### Momentum Control Devices

Such a platform must be capable of compensating the torques and forces acting on the base of the robot as it performs its task.
If we wish to use the proven technology of construction cranes, we need to find a way of creating counteracting forces and torques in the middle of space.
Luckily spacecraft have a similar issue, having to maneuver themselves without having land or air to push off of.
While it would certainly be spectacular to attach rocket engines to a crane and robot, spacecraft also have means of producing torque without expending fuel (a valuable skill in a place where a resupply used to cost 75k $/kg [@JonesMuchLowerLaunch2017]).
This feat is achieved through momentum control devices and this work will discuss the feasibility of using a specific type of these, called control moment gyroscopes, to reach our goal of construction robots for the largest of scales.

### Alternative Approaches

Prior to looking at momentum control devices in greater detail, this section will cover some of the alternatives for large workspace kinematics.

The first systems that comes to mind are parallel tendon kinematics.
Here instead of a single rope positioning the endeffector, multiple ropes/tendons are used.
By spanning these tendons from different directions it becomes possible to create stable positions and motions over large spaces.
Such system are commercially available for cameras in sports stadiums and researchers have proposed their use for a variety of other tasks.

The RoboCrane was originally a DARPA project at NIST, that was proposed for several applications [@james1993nist] including construction [@LytleIntelligentJobSite2003; @GoodwinRoboCraneConstructionBridges1997].
Other systems such as the Fraunhofer Institutes IPAnema have been aimed at logistics [@PottIPAnemaFamilyCableDriven2013].
More recently there have also been further conceptual proposals for the use of parallel tendon robots on construction sites [@SousaSPIDERobotCableRobotSystem2016] as well as large scale 3d-printing efforts that utilize parallel tendon research prototypes [@IzardLargescale3DPrinting2017] (see @Fig:parallel-tendon-print).

![Rendering of a 3d-printing concept for construction sites, taken from [@IzardLargescale3DPrinting2017]](./figures/parallel-tendon-printing-izard.png){ #fig:parallel-tendon-print }

Parallel tendon kinematics come with some challenges and downsides.
Dealing with tendon elasticity is particularly relevant to vibrations in the system.
Depending on the size of the endeffector platform, the systems will also struggle to produce high torques, as these depend on the amount of leverage that the tendons have on the platform.
Some researches have therefore added momentum control devices to compensate torques in parallel tendon kinematics [@WeberActiveVibrationCanceling2014], which points to interesting hybrid approaches (see @Fig:reaction-wheel-tendon).
The bigger issue for construction sites will most likely be the need for the tendon's winches to lie around the workspace of the system.
This means that one would have tendons crossing large areas of the construction site, which poses significant challenges with regard to collisions, setup costs as well as worker safety.

![Experiments with dampening a parallel tendon platform using reaction wheels, taken from [[@WeberActiveVibrationCanceling2014]]. The left is not using the reaction wheels. In the right one can see them being used and rotating at the top of the platform.](./figures/reaction-wheel-tendon-gangloff.gif){ #fig:reaction-wheel-tendon }

Drones are the only system on a construction site with a work envelope larger than cranes.
They are therefore seeing use as an inspection, surveying and monitoring tool.
They have also been proposed as a logistics and robotics platform for infrastructure (see [ARCAS EU Research Project](http://www.arcas-project.eu) and @Fig:flying-robot).
Given the weight of construction materials, drones minuscule payload capabilities, in comparison to cranes, severely limits this approach.
It is relevant to point out that the building materials of some widely publicized drone based constructions are foam blocks [@GramazioKohlerFlightAssembledArchitecture2011], nylon ropes [@MirjanBuildingBridgeFlying2016; @AugugliaroBuildingTensileStructures2013] and carbon fibers [@SollyICDITKEResearch2018].
The use of propulsive systems (e.g. propellors) to rotate or stabilize crane loads crops up and apparently there were experiments made in Japan or Korea [@InouePracticalDevelopmentSuspender1998], but sadly we have not been able to find sources to confirm this.

![Exerpt from the 4th year report of the ARCAS project on collaborative flying robots for maintenance and construction. The consortium also performed experiments with a kerosine fueled drone/helicopter capable of carrying a DLR LBR robot arm.](./figures/arcas.gif){ #fig:flying-robot }

While mobile platforms in robotics are starting to enter industrial use, they aren't able to provide the vertical reach of cranes.
For small heights linear axes can be added to the mobile platforms to increase the reach of their robot arms.
Some have proposed attaching industrial robot arms to other system to enhance their reach and construction site mobility.
One example from research is the Digital Construction Platform by the MIT Media Lab [@KeatingCompoundArmApproach2014] (@Fig:dcp-media-lab).
Others have attached articulated arms to hydraulic remote controlled demolition robots, for use in nuclear decommissioning [@BurrellFeedbackControlBased2016].
Aside from their vertical and horizontal reach, a further benefit of cranes can be their small footprint relative to their horizontal reach.
Mobile platforms on the other hand, would have to be provided with access via the ground.

![The Digital Construction Platform that combines an industrial robot with a hydraulic arm to increase its reach. The red line has been drawn by the end of the hydraulic arm and the blue line by the small robot attached to it. Taken from [@KeatingCompoundArmApproach2014]](./figures/dcp-mit-media-lab.jpg){ #fig:dcp-media-lab }

### Potential Applications

Having covered alternatives to stabilizing a crane hook with momentum control devices @Fig:baugrok-applications illustrates the potential usecases for the proposed system.
Generally speaking, it would add the ability to produce controlled torques at the hook of a crane without requiring any additional ropes or other kinematics.
The control moment gyroscopes would allow for the compensation of the torques of a robot or other processes suspended from the hook.
They would also provide control over the rotation of parts during transport and assembly operations.
Furthermore they could assist in dampening crane oscillations.

![Potential applications of a CMG-stabilized crane. From left to right: process compensation, part rotation and dampening of pendulum oscillations.](./figures/baugrok-applications.gif){ #fig:baugrok-applications }
