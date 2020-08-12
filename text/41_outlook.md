
# Outlook and Conclusion

Prior to summing up this work, I would like to discuss the assumptions and associated limits of the models currently in use.
Given these limits and some of the insights gained through the experiments, I will then make recommendations regarding the most urgent developments needed to further the goals of this work.
I will also cover further questions and areas of research that need to be addressed to make CMGs a useful tool for cranes in general and the construction site in particular.

## Assumptions of Current Models

The most significant simplifications in the models are, (not in order of importance) :

- use of stiff links capable of transmitting torque  
  (possible for lower link, unrealistic for upper link)
- no drag or friction
- no process forces or torque in robot simulations
- no sensor noise or control loop delay

The sizing calculations also do not include any considerations concerning the specific shape of the momentum envelope, its singularities and changing dynamics as one moves through it.
Most of these assumptions do not limit the conclusion made from the simulations, but they do limit further understanding of the system and in particular the development of controllers.

## Next Steps for Development

With the goal of moving towards a 3 DoF CMG system suited for real world crane stabilization experiments, several parts of this work need to be transferred to 3D cases.
Nevertheless the 2D models and prototype should be of continued use.
Both controller and hardware design as well as validation can more easily be understood and performed on the 2D case.

A priority for the development of the 3D controller should be the inclusion of the reaction torque limiting strategy discussed at the end of the previous chapter on sizing (@sec:sizing_for_cranes).
Limiting the reaction torque experienced by the CMGs through alignment of momentum and rotation axis is the critical component required to make CMGs useful for crane-based applications beyond load rotation.
The development described in this section therefore mostly outlines the critical path to a state where the efficacy of such a strategy can be validated through simulations.

It is to be hoped that the existing explicit equations of motion together with the SymPy code used for their derivation will prove useful in the design and stability proofs of the required controllers.
To be able to develop and also validate the steering and control of the four-CMG roof array (required for the move to 3DoF hardware prototype), either a new modular model or the existing 3D equations of motion could be used.
The existing model will already allow developments regarding the dampening and rotation applications.
One thing currently not included in the 3D equations is the translation of external forces into additional torques on the upper and lower link.
This has so far only been implemented for the 2D model.

To move the controllers (and subsequently the hardware) to 3D, one will have to translate the error about three axes into a 3D target torque.
This in turn necessitates the extension of the SPCMG model to a four-CMG roof array with the implementation of a suitable steering law.
Once these components are in place, it will become possible to analyze the controller's performance under the limitations resulting from the agility and singularities of the 3D CMG array in combination with the chosen steering law.

The biggest challenge in limiting the reaction torque through control of the gimbal angles will be that it will probably require a novel steering law for the CMG array.
While many steering laws and steering law design strategies exist, (see [@LeveSpacecraftMomentumControl2015, ch. 7]), none deal with this very crane-specific constraint.

Apart from the reduction of reaction torques, the other major question is how well a CMG array is able to provide a stable platform for robotic and other processes.
While torques acting upon the platform itself can be compensated by the CMGs, forces acting on it end up acting on its pivot point and therefore on the link from which the platform is hanging.
This can only be compensated by the CMGs indirectly i.e. by tilting the platform.
This is not taken into account in the controller currently implemented.
A controller that reduces the error produced by the force acting on the upper link by introducing an error to the lower link might improve platform stability.

Furthermore the forces and torques applied to the pendulum during the simulated compensation assumed a fixed robot.
The motion of the robot’s base due to oscillations of the platform are therefore not taken into account in the forces and torques.
To address this issue, the robot multibody simulation needs to be integrated into the pendulum model.
Through the addition of either more realistic inverse kinematics that take axis accelerations into account, or a hardware-in-the-loop setup that uses the actual robot controller, robot-based compensation strategies could be developed, enabling these strategies to be validated as they work in coordination with the dampening controller.

Given that it will also be desirable at a later date to extend the model to include the remainder of the crane, my recommendation would be to implement a modular multibody simulation into which the model of the CMG dynamics can be integrated.
This should be possible in Modelica, Simulink Simmechanics or other toolkits.
While the CMG array could also be modeled using this approach, I would recommend the use of the explicit model used in this work, as it makes it possible to distinguish the various torque components.
This proved to be of great value in understanding the gyroscopic system.

## Future Work Required

Beyond the critical next steps outlined above, there is a plethora of research and engineering challenges.

Once the pendulum, CMG and robot multibody models as well as the inverse kinematics have become more tightly integrated, optimization strategies to increase process accuracy through changes to robot paths and execution speeds/accelerations could then be studied.
Similarly, by extending the models to include motion of the suspension point i.e. gantry motion or trolley and gib motion, control systems become possible that utilize information and actors of both the crane and CMG array.
This should open up novel control techniques for the controlled movement of cranes as well as better input to the reaction torque reduction and ways to desaturate the CMGs.
Desaturation goals could also be met by adjusting control during the dampening of large oscillations.
Furthermore the use of an adjustable weight as a source of low agility torque would require further extensions to the CMG steering laws.

Such adjustable weights would be added to the list of engineering challenges involved in bringing CMGs to the construction site and other cranes.
Prior to achieving on-site suitability, there is also some work to be done in extending the lab prototype from one to three degrees of freedom.
The gyroscopes should be improved with regard to their rotational accuracy and mounting so as to reduce wear, spin up times, noise and vibrations.
The issues with the maximum gyroscope speed and accuracy also need to be investigated.
To ease and accelerate the controller design process, the realtime capabilities need to be increased to allow for signal analysis during experiments and rapid modification of parameters without recompiling.
By moving the control loops to an embedded target, the round trip times from controller to motors and back should also become shorter and, most importantly, more reliable.
Given the risk of high reaction torques, stronger gimbal motors and couplings or dedicated points of failure should be investigated.

The current sole IMU should also be extended to allow for measurement of the upper link.
It might also be useful to add external optical tracking to allow for validation of the onboard sensors.
It is to be expected that the implementation of the inertia estimation should be straightforward, but it is also a required development.

Looking towards more realistic implementations of the CMG array, the power use needs to be taken into account.
While it is possible to provide power at the crane hook, given the advances in battery technology, models and experiments regarding the power consumption of the array during operation will be of interest.
As previously noted, gyroscopes in CMGs have been used as additional energy storage to handle load spikes in marine applications.
The use of such storage in spacecraft was abandoned due to batteries having a similar energy density while posing less engineering challenges.

Continuing and ever more extensive validation will also be required.
The collection of real crane motion data would be highly valuable for the validation of the crane parameter estimations and dampening requirements.
As the simulation tools are improved, more realistic and diverse processes will emerge that utilize the crane-CMG system and provide valuable input regarding the compensation and rotation requirements.

## Conclusion

This work was motivated by the desire to bring more robotic capabilities to the construction site.
Given the limited reach of conventional robot arms, the idea was to combine them with the reach of construction cranes to be able to service the large workspace of construction sites.
To ensure a stable work platform for the robot arm, the strategy was to begin with a parallel tendon kinematic, iteratively remove tendons and add other form of compensation mechanisms to maintain stability for the robot.
My initial research into potential compensation mechanisms led to spacecraft momentum control devices and the large torque capacities of control moment gyroscopes.
The focus of this work therefore became to ascertain the potential of CMG stabilization of crane hooks.

The review of the general principles of CMGs, their use in spacecraft, ships and other applications including cranes shows the knowledge gap that this work hopes to begin to fill.
There is a large amount of literature regarding the design and control of CMGs for spacecraft attitude control.
The same is true of crane dynamics and control theory.
Up to now there have only been a handful of research efforts regarding the use of CMGs in cranes, none of which provide models of crane-CMG dynamics or guidelines for the sizing and design of such systems.

This work therefore provides suitable models of the crane and platform/load as a double pendulum with a distributed mass hanging from a point mass that in turn is hanging from a fixed pivot.
Given the relevance of the base rate on the sizing of CMGs, the work also includes an estimation of the base rate for cranes that uses parameters from crane data sheets.
This in particular will require validation, as the base rates will change depending on the control of the crane and excitation sources present during operation.

To understand the interaction of the crane-CMG system, I chose to limit the crane to a 2D model but left the CMG model 3D.
This is necessary, due to the cross product involved in gyroscopic systems (@eq:reaction_torque).
By implementing the equations that describe the dynamics of a scissored pair CMG and attaching it to the obtained equations of motion for the crane/pendulum, I was able to develop an understanding of the system much more quickly than with a physical prototype.
In the physical prototype, our view into the system is limited by the sensors, noise, signal delay and of course bugs.
The simulation models also include the implementation of a steering law for the SPCMG with singularity avoidance and a model of the gimbal dynamics that limit acceleration and velocity of the gimbal.

The simulations and subsequent development of control as well as sizing approaches were systemized through the definition of three-crane-CMG applications: dampening, part rotation and process compensation.
This definition helps to distinguish the requirements and interactions of the system.
While the part rotation is akin to CMG applications in spacecraft, dampening is more related to the roll reduction systems in boats.
The addition of process compensation means that while we can borrow from certain parts of spacecraft design and particularly from the engineering of ship gyroscopes, novel control and sizing approaches are required to fully utilize the CMG's potential for cranes.
The combination of applications also sets apart this work from prior crane stabilization efforts, which only focus on stabilization and limit themselves to a single CMG.

The chapter on controller design develops an integrated control approach for the combination of the three applications.
From a review of existing crane dampening controllers, and control of underactuated systems, I chose to implement a simple PD$\alpha$ controller.
Simulations and preliminary experiments on the physical prototype show that this approach is capable of dampening the double pendulum using torque produced by the CMGs.

The process compensation utilizes the fact that the process is known in advance and controlled in a programmed manner.
By simulating the torques produced by the process in advance, it should therefore become possible to compensate these torques which would otherwise excite the pendulum.
The rotation controller arises naturally from the dampening controller, once the system is extended to three dimensions.
All of these controllers require an understanding of the moment of inertia of the platform and load.
This might be estimated using conventional techniques (e.g. a Kalman filter) that utilize the understanding of the torque being produced and the observed accelerations of the system.

The simulations created the understanding required to develop the sizing of CMGs for cranes.
The interaction of the applications' requirements and various parameters of CMGs are discussed in the chapter on sizing.
The chapter provides a workflow through the sizing parameters which was also translated into a spreadsheet that should assist in sizing CMGs for crane applications.

Together with the simulations, the sizing workflow validates the feasibility of the CMG-crane system.
More importantly, the work has also led to the identification of key challenges for the development of CMG-crane systems.

We can see that CMGs capable of producing the torque with an agility suited for process compensation and part rotation are feasible.
The issue of the gimbals having to sustain gyroscopic reaction torques caused by rotation of the system is sufficiently limited or controllable in these cases.
Processes compensation ideally results in a static platform, and ergo low base rates.
During part rotation the base rate is governed by the desired rotation speed.
During dampening, however, the base rate is governed by the crane's parameters and easily reaches velocities similar to those of our gimbals in the other applications.
Given the relationship of torques and velocities in a CMG system, this leads to high reaction torques, which in turn cause high gimbal motor torque requirements.
This is exacerbated by the fact that dampening performance is highly dependent on the size of the momentum envelope, which in turn necessitates high angular momentum in the gyroscopes which in turn increases reaction torques.

Therefore, the challenge of reducing the reaction torque during dampening is the key to the further development of this work. 
An in-depth explanation is given in the simulation chapter (@Sec:torque-issue) as well as the subsequent chapter on sizing (@Sec:sizing_for_cranes).
From the simulations it seems possible to extend the CMG control and steering laws so as to limit the reaction torques by forcing the momentum vectors into alignment with the axis of rotation during the periods of high velocities.
The previous sections on future work lay out how the existing models and hardware should be extended so as to allow the development of such CMG control.

The recent arrival of a commercial CMG based system for crane load rotation proves the potential impact of CMGs on crane operation.
The development of more advanced, crane specific CMG control for 3 DoF CMG-arrays should extend their utility beyond rotational control during critical lift operations.
Their dampening capabilities could lead to high speed, stable crane movements and also allow entirely novel crane-application by providing a stable process platform.

------------

Controlled motion is the foundation for automation.
With the addition of CMGs, cranes could become a motion provider for workspaces of unprecedented size and payload.
It is my hope that the explanations, models, code, tools and discussions of this work will prove a useful for others pursuing this potential.
