
# Introduction {#sec:background}

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

First examples of these new on-site, commercially available robots are SAM100 the brick-laying robot [@SAM100ConstructionRobotics] and Tybot the rebar-tying robot for bridge decks [@RebarTyingRobotPittsburgh].
Robots have also entered the preproduction of buildings and we are slowly seeing more direct links between digital planning and individualized robotic execution.
As industrial robots enter the construction industry, the existing construction machinery is also becoming more sophisticated.
Dump trucks are already driving autonomously in open pit mines and excavators and other machines are being fitted with sensors and digital controls.

The availability of digitally-controllable machinery has always been key to increasing automation and individualization.
Such machines are the bridge from digital planning to execution in the real world.
As such it is wonderful to see the emergence of programmable machines suited for the construction site.
Yet one aspect of the construction site is not addressed by the existing range of adapted industrial robots and upgraded construction machinery: the sheer size of construction sites.
Therefore this work investigates the idea of hanging robots from cranes to increase their work envelope to that of the construction site.

## Cranes as a Base for Robot Operations

The ability of cranes to provide logistics over large spans and at great heights has transformed construction since antiquity.
They are the kinematic systems of choice for the large scale of construction sites, naval operations and large scale assembly tasks.
However, the key to their success is also limits their ability as a provider of automated motion.
Using a rope as the last link of their kinematic chain, cranes are able to cover height with a minimum of material.
The flexibility of the rope also means that it requires extremely little space when retracted, as it can be coiled and wound around winches.
Yet this flexibility also means that the rope cannot be used to push, only to pull.
With the actors (the motors) of the crane connected to the end effector (the hook) via a flexible connection, it is difficult to produce controlled motion in the event of disturbances.

![Overview of forces preventing stable operation of e.g. a robot suspended from a crane: a) center of gravity (CoG) of the hook/platform moves out of equilibrium, b) robot CoG gets moved out of equilibrium, c) forces and torques acting at robot base due to motion of robot, d) forces and torques stemming from interaction with external objects, e) external forces e.g. wind. Note that these all interact.](./figures/crane-robot-forces.svg){#fig:crane-robot-forces short-caption="Forces acting on a robot hanging from a crane"}

The ability of robots and other digitally controlled automation technology to perform accurate and repeatable movements is key to their usefulness.
Hanging a robot from a crane to increase its work envelope needs to maintain this ability.
The hypothetical assembly in @Fig:crane-robot-forces illustrates the various forces at play that could create disturbances, moving the crane's hook, attached platform and hence the robot, leading to deviations in its intended movement.

To break down the various forces it helps to imagine conditions under which the platform would be stable and level in space.
In a static case and without external forces these conditions would exist when the centers of gravity (CoG) of the platform and the robot below it are in line with the point of suspension for the rope i.e. the gantry.
Any movement of the gantry would break this condition and lead to motion of the platform (a).
Similarly, motion of the robot or attaching loads to it would change its CoG (b), once again leading to motion of the platform.
Even if the CoG is maintained in an equilibrium position, motion of the robot results in forces and torques acting at the base of the robot (c), once again causing motion of the platform.
Further disturbance of the platform equilibrium can be caused by the robot interacting with its environment (d) and the environment e.g. wind acting on the whole assembly (e).

With the platform being able to pivot and rotate freely around the hook and the hook itself being fairly free to move laterally the robot has a very unstable base of operations.
It is obvious that by controlling the motion of the crane and robot it should be possible to reduce motion experienced by the platform.
The control that can be exerted in this fashion is quite limited and poses a challenging control problem due to an underactuation with regard to the systems degrees of freedom (see @Sec:controller-review).
Such a control approach would also limit the ways in which the crane and robot could be used.

As such it would be advantageous to add additional means with which to control the platform, thereby giving the robot a more stable base of operations.
The disturbances illustrated in @Fig:crane-robot-forces involve both forces and torques.
This work focuses on adding controllable torque to a hypothetical platform without relying on physical constraints e.g. additional ropes or propulsion e.g. propellors.
This means generating said torques in the middle of space.

Fortunately, spacecraft face a similar issues, having to maneuver without having land or air to push off from.
Whilst spacecraft are usually known for their use of rocket and other propulsive devices, they also usually have means of producing torque without expending fuel.
This feat is achieved through momentum control devices and this work will discuss the feasibility of using a specific type of these, called control moment gyroscopes (CMG), to enable construction robots for large work envelopes.
Prior to introducing these devices and their existing uses ([chapter @Sec:cmg-sota]) the following sections discuss alternative approaches to robotics for large workspaces and the potential applications for this work.

## Alternative Approaches for Large Workspaces

A well studied approach for large workspaces are parallel tendon kinematics.
Here, instead of a single rope positioning the end effector, multiple ropes/tendons are used.
By spanning these tendons from different directions, it becomes possible to create stable positions and motions over large spaces.
Such systems are commercially available for cameras in sports stadiums and researchers have proposed their use for a variety of other tasks.

The RoboCrane was originally a DARPA project at NIST that was proposed for several applications [@james1993nist] including construction [@LytleIntelligentJobSite2003; @GoodwinRoboCraneConstructionBridges1997].
Other systems such as the Fraunhofer Institute???s IPAnema have been aimed at logistics [@PottIPAnemaFamilyCableDriven2013].
More recently there have also been further conceptual proposals for the use of parallel tendon robots on construction sites [@SousaSPIDERobotCableRobotSystem2016] as well as large scale 3D-printing efforts that utilize parallel tendon research prototypes [@IzardLargescale3DPrinting2017] (see @Fig:parallel-tendon-print).

![Rendering of a 3D-printing concept for construction sites [@IzardLargescale3DPrinting2017]](./figures/parallel-tendon-printing-izard.png){ #fig:parallel-tendon-print short-caption="Rendering of a 3D-printing construction site concept"}

Parallel tendon kinematics come with some challenges and disadvantages.
Dealing with tendon elasticity is particularly relevant to vibrations in the system.
Depending on the size of the end effector platform, the systems will also struggle to produce high torques, as these depend on the amount of leverage that the tendons have on the platform.
Some researchers have therefore added momentum control devices to compensate torques in parallel tendon kinematics [@WeberActiveVibrationCanceling2014] (see @Fig:reaction-wheel-tendon), which point to interesting hybrid approaches utilizing parallel tendon systems in combination with CMGs.
The bigger issue for construction sites will most likely be the need for the tendon's winches to be placed around the workspace of the system.
This means that tendons would be required to cross large areas of the construction site, which poses significant challenges with regard to collisions, setup costs as well as worker safety.

![Experiments with dampening a parallel tendon platform using reaction wheels [@WeberActiveVibrationCanceling2014]. The left example is not using the reaction wheels. On the right, one can see them being used and rotating at the top of the platform.](./figures/reaction-wheel-tendon-gangloff.gif){ #fig:reaction-wheel-tendon short-caption="Parallel tendon platform dampened with reaction wheels"}

Drones are the only system on a construction site with a workspace larger than cranes.
They are therefore seeing use as an inspection, surveying and monitoring tool.
They have also been proposed as a logistics and robotics platform for infrastructure (see [@HOMEARCASProject] and @Fig:flying-robot).
Given the weight of construction materials, drones??? small payload capabilities in comparison to cranes severely limits this approach.
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

## Potential Applications

In comparison to the alternatives covered above, @Fig:baugrok-applications illustrates the potential abilities of the proposed system of stabilizing a crane hook with momentum control devices.
Generally speaking, it would add the ability to produce controlled torques at the hook of a crane without requiring any additional ropes or other kinematics.
The control moment gyroscopes would allow for the compensation of the torques produced by a robot's motion or other processes suspended from the hook.
They would also provide control over the rotation of parts during transport and assembly operations.
Furthermore they could assist in dampening crane oscillations.

These abilities could result in novel applications of cranes, not only on construction sites.
Components could be moved with greater control for logistics and assembly operations.
By increasing the control of the motion, safe automation of such tasks becomes possible.
The ability to compensate process torques also makes it possible to use additional kinematic systems, be they specialized or general purpose (e.g. industrial robots).
Examples of these applications are illustrated in @Fig:indoor-and-outdoor.

![Abilities of a CMG-stabilized crane. From left to right: process compensation, part rotation and dampening of pendulum oscillations.](./figures/baugrok-applications.gif){ #fig:baugrok-applications short-caption="Abilities of a CMG-stabilized crane"}

![Potential applications of a CMG-stabilized crane. From left to right: part transport with gantry cranes, transport and assembly of components on a construction site, mobile industrial robots.](./figures/indoor-and-outdoor-applications.png){ #fig:indoor-and-outdoor short-caption="Potential applications of a CMG-stabilized crane"}
