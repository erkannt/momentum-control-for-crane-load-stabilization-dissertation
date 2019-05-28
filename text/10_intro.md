
# We are going to need a bigger robot

Our means to shape the world we inhabit are limited by our resources and tools.
As an engineer tools hold a special fascination for me, as they let us extend the reach of humanity.
Yet often we find that the world doesn't want our new toys.
Maybe they don't need them, or worse they are actually harmful.
I would like to make the bold statement that this is where design must come into play.
Design for me is finding and shaping a subset of the possible to fulfill the needs of humans and our surrounding ecosystem.
This definition obviously includes the trade of architects, a field where the rushing avalanche of technological innovation seems to have so far only resulted in a trickle of change.

Yet the role of design is not limited to finding the humane subset of the technologically possible.
One of its most important jobs is painting a picture of the not yet possible, so that we might understand what is still missing in our technological cornucopia.
It is one of these pictures that gave birth to this work.

![Photomontage of robots suspended from a tower crane performing facade assembly.](./figures/crane-robot-montage.jpg)

## The Need for Construction Robots

Construction is and will be facing significant challenges.
Our urban population is rising [@PopulationDivision-UnitedNationsWorldUrbanizationProspects], necessitating not only the creation of significant amounts of new building stock but also the densification and upgrading of existing stock.
Furthermore we must reduce the impact that of our buildings and their use on the environment.
At the same time our lackluster response to climate change has already resulted in increasingly extreme weather conditions and changes to the temperatures that our buildings should handle.
And ideally we need to surmount all of these challenges while creating a building stock that actually fulfills the needs specific to the locale.
Many so called developed nations are also facing shortages in skilled construction workers [@MorrisonConstructionLaborShortage], not only due to the aging population and unattractive working conditions but also due to the reliance on cheap foreign labour.
The latter has caused many sectors in construction to stagnate technologically as innovation was more costly than masses of cheap labour.

Luckily the technological advances have led other industries to look to stark individualization and increasing flexibility in their production.
Looking at earlier attempts at automating construction (particularly in Japan and Korea during the 80s) one can see how technology of the day wasn't able to provide said individualization and flexibility required in construction.
With robots, sensors and computing becoming more ubiquitous we are finally seeing the emergence of construction robotics.

The first examples of on-site commercially available robots exist with [SAM100](https://www.construction-robotics.com/) the brick laying robot and [Tybot](https://www.tybotllc.com/) the rebar tying robot for bridge decks.
Robots have also entered preproduction of buildings and we are slowly seeing more direct links between digital planning and individualized robotic execution.
As industrial robots enter the construction industry the existing construction machinery is also becoming smarter.
Dump truck are already driving autonomously in open pit mines and excavators and other machines are being fitted with sensors and digital controls.

The availability of digitally controllable machinery has always been key to increasing automation and individualization.
Such machines are the bridge from digital planning to execution in the real world.
As such it is wonderful to see the slow emergence of programmable machines suited for the construction site.
Yet one aspect of the construction site isn't covered by the existing fare of adapted industrial robots and upgraded construction machinery: the sheer size of construction sites.

## Turning Cranes into Robots

The ability of cranes to provide logistics over large spans and in ever greater heights has transformed construction since antiquity.
They are the kinematic systems for the largest scales.
But the key to their success is also the reason holding back their automation.
Using a rope as the last link of their kinematic chain, cranes are able to cover height with a minimum of material.
This flexibility of the rope also means that it requires next to no space when retracted, as it can be coiled and wrapped.
Yet this flexibility also means that we can't use a rope to push, only to pull.
With the actors of the crane connected to the endeffector (the hook) via such a flexible connection, it isn't possible to produce controlled motion in the face of disturbances.
If we wish to effectively use robots over the large work area of the construction site we must find a way to control provide them with a stable work platform.

### Momentum Control Devices

Such a platform must be capable of compensating the torques and forces acting on the base of the robot as it performs it's task.
If we wish to use the proven technology of construction cranes we need to find a way of creating counteracting forces and torques in the middle of space.
Luckily spacecraft have a similar issue, having to maneuver themselves without having land or air to push off of.
While it would certainly be cool to attach rocket engines to a crane and robot, spacecraft also have means of producing torque without expending fuel (a valuable skill in a place where a resupply used to cost 85k $/kg).
This feat is achieved through momentum control devices and this work will discuss the feasibility of using a specific type of these called control moment gyroscopes to reach our goal of construction robots for the largest of scales.

### Alternative Approaches

But first let us look at the alternative approaches to this problem.
The first that comes to mind is parallel tendon kinematics.
Here instead of a single rope connecting us to the endeffector we have multiple.
By spanning these tendons from different directions it becomes possible to create stable positions and motions through large spaces.
Such system are used for cameras in sports stadiums and researchers have proposed their use for a variety of other tasks.
The RoboCrane was originally a DARPA project at NIST that was proposed for several applications [@james1993nist] including construction [@LytleIntelligentJobSite2003; @GoodwinRoboCraneConstructionBridges1997].
Other systems such as the Fraunhofer Institutues IPAnema have been aimed at logistics [@PottIPAnemaFamilyCableDriven2013].
More recently there have also been more conceptual proposals for the use of parallel tendon robots on construction sites [@SousaSPIDERobotCableRobotSystem2016] as well as large scale 3d-printing efforts [@IzardLargescale3DPrinting2017] (see @Fig:parallel-tendon-print).

![Rendering of a 3d-printing concept for construction sites, taken from [@IzardLargescale3DPrinting2017]](./figures/parallel-tendon-printing-izard.png){ #fig:parallel-tendon-print }

Parallel tendon kinematics come with some challenges and downsides.
Dealing with tendon elasticity is particularly relevant to vibrations in the system.
Depending on the size of the the endeffector platform the systems will struggle to produce high torques as these depend on the amount of leverage they have on the platform.
Some researches have demonstrated the use of momentum control devices to compensate torques in parallel tendon kinematics [@WeberActiveVibrationCanceling2014], which points to interesting hybrid approaches with this work (see @Fig:reaction-wheel-tendon).
The bigger issue for construction sites will most likely be the need for the tendons winches to lie around the workspace of the system.
This means that one would have tendons crossing the large areas of the construction site, which poses significant challenges with regard to collisions as well as worker safety.

![Experiments with dampening a parallel tendon platform using reaction wheels, takes from [[@WeberActiveVibrationCanceling2014]]. The left is not using the reaction wheels, in the right you can see them being used and rotating at the top of the platform.](./figures/reaction-wheel-tendon-gangloff.gif){ #fig:reaction-wheel-tendon }

Drones are the only system on a construction site with a work envelope larger than cranes.
They are therefore seeing use as an inspection, surveying and monitoring tool.
While they have also been proposed as a logistics and robotics platform for infrastructure (see [ARCAS EU Research Project](http://www.arcas-project.eu) and @Fig:flying-robot), their minuscule payload capabilities in comparison to cranes severely limits this approach given the weight of construction materials.
Note that the building materials of the widely publicized drone based constructions are foam blocks [@GramazioKohlerFlightAssembledArchitecture2011], nylon ropes [@MirjanBuildingBridgeFlying2016; @AugugliaroBuildingTensileStructures2013] and carbon fibres [@SollyICDITKEResearch2018].
The use of propulsive systems to rotate or stabilize crane loads crops up and apparently there were experiments made in Japan or Korea [@InouePracticalDevelopmentSuspender1998], but sadly we have not been able to find sources to confirm this.

![Exerpt from the 4th year report of the ARCAS project on collaborative flying robots for maintenance and construction.](./figures/arcas.gif){ #fig:flying-robot }

While mobile platforms in robotics are starting to enter industrial use they aren't able to provide the vertical reach of cranes.
For small heights linear axes can be added to the mobile platforms to increase the reach of their robot arms.
Some have proposed attaching industrial robot arms to other system to enhance their reach and construction site mobility.
One example from research is the Digital Construction Platform by the MIT Media Lab [@KeatingCompoundArmApproach2014] (@Fig:dcp-media-lab).
Others have attached articulated arms to hydraulic remote controlled demolition robots for use in nuclear decommisioning [@BurrellFeedbackControlBased2016].
Aside from their vertical and horizontal reach a further benefit of cranes can be their small footprint relative to their horizontal reach, while mobile platforms would have to be provided with access via the ground.
Given that the weight of even small mobile platforms with a payload of 15kg can encroach upon residential floor load limits, this severely reduces the feasibility of mobile platforms on construction sites.

![The Digital Construction Platform that combines an industrial robot with a hydraulic arm to increase its reach. The red line has been drawn by the end of the hydraulic arm and the blue line by the small robot attached to it. Taken from [@KeatingCompoundArmApproach2014]](./figures/dcp-mit-media-lab.jpg){ #fig:dcp-media-lab }

### Potential Applications

Having looked at alternatives to attaching space tech to cranes, lets briefly look at what we could achieve should this work out.
Generally speaking we would be adding the ability to produce controlled torques at the hook of a crane.
This would not only enable us to compensate the torques of a robot or other processes suspended from the hook.
It would also let us control the rotation of parts during transport with the crane or during assembly operations.
Furthermore it could add additional actors for the challenge of dampening crane oscillations.

![Potential applications of for a CMG-stabilized crane. From left to right: process compensation, part rotation and dampening of pendulum oscillations.](./figures/baugrok-applications.gif){ #fig:baugrok-applications }

## Goal of Work

This work was kicked off and performed at the relatively young chair for _Individualized Production in Architecture_.
The chair is part of the architecture faculty but brings together researchers from not only architecture but also computer science, mechanical as well as civil engineering and generally speaking a lot of people that defy easy categorization.
We believe such interdisciplinarity to be essential to solving many of the problems our built environment faces.
While interdisciplinary work is burdened with challenges in communication and specialization, it is critical in achieving what I described in the introduction to this work: a closer connection between design and technological developments. 

Therefore the following work aims to not only be of use to other engineers who enjoy dynamics systems and their control.
Instead I hope that this work will be of use to architects, civil engineers and roboticists alike.
That they each may understand the potentials and challenges that the idea of a robot hanging from a crane brings.

It often seems to take painfully long for a novel idea or technology to turn into widespread innovation.
Part of this is due to the fact that researchers have to actually build their own tools before they can do any research as the tools they need often don't exist.
It is once these tools mature and become available to others that things kick into a higher gear.
With this in mind the following work contains a basic introduction to control moment gyroscopes, models for the simulation of the the crane-CMG-robot system as well tools for the sizing of CMGs for crane applications.

\todo{prior work at chair and patent application}
\todo{add patent application to citations}
