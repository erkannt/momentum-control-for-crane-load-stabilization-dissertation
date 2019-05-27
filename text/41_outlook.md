
# Outlook and Conclusion

> "Once the conditions for helicopters are in place, it’s helicopter time, and so you get helicopters, everywhere, all at once." -- Cory Doctorow @locusmagCoryDoctorowTerra2019

Prior to summing up this work I would like to discuss the assumptions and associated limits of the currently used models.
Given these limits and some of the insights gained through our experiments I will then make recommendations regarding the acute developments needed to progress this work but also some ideas regarding questions and areas that need to be covered to make CMGs a useful tool for cranes in general and the construction site in particular.

## Assumptions of Current Models

Cows aren't spheres, but sometimes it is sufficient to model them as such to gain valuable insights.
Likewise the models in this work make some stark simplifications regarding the crane-cmg-process system.

In no particular order the most significant of these are:

- model uses stiff links capable of transmitting torque  
  (possible for lower link, unrealistic for upper link)
- no drag or friction
- no process forces or torque in robot simulations
- no sensor noise or control loop delay

In the sizing calculations we are also not including any considerations for the specific shape of the momentum envelope, its singularities and changing dynamics as one moves through it.
Most of these assumptions do not limit the conclusion made from the simulations, but they do limit further understanding of the system and in particular the development of controllers.

## Next Steps for Development

\todo{controller to balance torque comp of lower link and upper link due to external forces}
\todo{usefulness of explicit 2d models for controller design and proofs}

Given that one will later on wish to also extend the model to include the remainder of the crane, my recommendation would be to move to a modular multibody simulation into which one integrates the model of the CMG dynamics.
This should be possible in both Modelica or Simulink Simmechanics.
While the CMG array could also me modeled using this approach I would recommend the use of the explicit model also used in this work, as it makes it possible to distinguish the various torque components, which helps in understanding the complex nature of the gyroscopic system.

To be able to develop and validate steering and control of the desired four CMG roof array required for the move to 3d, either a new model of the crane as just described or the existing 3d equations of motion could be used.
The existing model will already allow developments regarding the dampening and rotation applications.

To move the controller to 3d, one will have to translate the error about three axis into a 3d target torque.
This of course in turn necessitates the extension of the SPCMG model to a four CMG roof array with an implementation of a suitable steering law.
Once these components are in place it becomes possible to analyze the controllers performance under the limitations resulting from the agility and singularities of the CMG array and the chosen steering law.

A priority for the development of the 3d controller should be the inclusion of the reaction torque limiting strategy discussed at the end of the previous chapter on sizing.
Limiting the reaction torque experienced by the CMGs through alignment of momentum and rotation axis is the critical component required to make CMGs useful for crane based applications.
The development described in this section therefore mostly outline the critical path to a state where the efficacy of such a strategy can be validated through simulations.

Apart from the the reduction of reaction torques the other major question is how well a CMG array is able to provide a stable platform for robotic or other processes.
The forces and torques applied to the pendulum by the robot used results from a simulation of fixed robot.
The motion of the robots base, due to oscillations of the platform are therefore not taken into account in the forces and torques.
To fix this, one needs to integrate the robot multibody simulation into the pendulum model.
Through the addition of either more realistic inverse kinematics, that take axis accelerations into account, or a HIL setup that uses the actual robot controller, one could then begin development of robot based compensation strategies and validation of said strategies as they work together with the dampening controller.

## Other Work Required

Beyond these critical next steps resides a plethora of interesting research and engineering challenges.

Once the pendulum, CMG and robot multibody models as well as inverse kinematics have become more tightly integrated, one could begin studying optimization strategies that increase the process accuracy through changes to robot paths and execution speeds/accelerations.
In a similar vein, by extending the models to include motion of the suspension point i.e. gantry motion or trolley and gib motion, it becomes possible create control systems that utilize information and actors of both the crane and CMG array.
This should open up novel control opportunities for dampening and controlled movement as well as better input to the reaction torque reduction and ways to desaturate the CMGs.
Desaturation goals could also be met by adjusting the control during dampening of large oscillations.
Furthermore the use of an adjustable weight as a source of low agility would require extensions to the CMG steering laws, which should provide fascinating research questions to people minded to such things.

Such adjustable weights would be added to the long list of engineering challenges involved in bringing CMGs to the construction site and other cranes.
Prior to on-site suitability there is also some work to be done in bringing the lab prototype to 3d dimensional application.
The gyroscopes will should be improved with regard to their rotational accuracy and mounting to reduce wear, spin up times, noise and vibrations.
To ease and accelerate the controller design process the realtime capabilities need to be increased to allow for signal analysis during experiments and rapid modification of parameters without recompiling.
By moving the control loops to an embedded target the round trip times from controller to motors and back should also become shorter and most importantly more reliable.
Given the risk of high reaction torques one should look into stronger gimbal motors and couplings or dedicated points of failure.

The current sole sensor should be extended, to also allow measurement of the upper link.
It might also be useful to add external optical tracking to allow for validation of the onboard sensors.
The implementation of the inertia estimation should hopefully be straightforward, but is also a required development.

Looking towards more realistic implementations of the CMG array the power use needs to be taken into account.
While it is possible to provide power at the crane hook, given the advances in battery technology models and experiments regarding the power consumption of the array during operation will be interesting.
As previously noted gyroscopes of CMGs have been used as additional energy storage to handle short higher loads in marine application but abandoned in spacecraft research due to batteries having a similar energy density while posing less engineering challenges.

As with all research continuing and ever more extensive validation will be required.
The collection of real crane motion data for instance would be valuable to validate the crane parameter estimations and dampening requirements.
As the simulation tools are improved more realistic and diverse processes will emerge that utilize the crane-CMG system and provide valuable input regarding the compensation and rotation requirements.

## Conclusion

This work got started with a robot photoshopped to a crane and the idea to somehow keep it stable through some form of compensation mechanism.
The potential of momentum control systems rapidly became clear, but whether they where up to the task and how one might go about building such a system were entirely unclear.
As Leonardo da Vinci's sketches of helicopters show: simple ideas can turn out to be deviously hard to actually to implement but cause lots of interesting research along the way.

So in this work we have looked at how control moment gyroscopes work, how they have been applied to spacecraft, ships and other terrestrial applications including some cranes.
This review showed several gaps in our knowledge regarding how CMGs might interact usefully with a crane.
As someone setting out to build a CMG array aimed at stabilizing a robot hanging from a crane, I struggled to determine how to size the CMGs.
Furthermore the combined weirdness of gyroscopes and pendulums made it disconcertingly hard to grasp how the system would behave.
Therefore the first order of business had to be the development of some simplified models that would let us understand this fairly novel terrestrial application of CMG technology.

This work includes suitable models of the crane and platform/load as a double pendulum of a distributed mass hanging from a point mass.
Given the relevance of the base rate on the sizing of CMGs it also includes an estimation of the base rate for cranes, given parameters from their data sheets.
This in particular will require validation and the base rates will change depending on the control of the crane and the excitation sources present during operation.
To understand the interaction of the crane-cmg system, we chose to limit the crane to a 2d model but left the CMG model 3d.
This is necessary, due the cross product involved in gyroscopic systems.
By implementing the equations that describe the dynamics of a scissored pair CMG and attaching it to the obtained equations of motion for the pendulum, we were able to develop an understanding of the system much quicker than with a physical prototype where our view inside the system in limited by our sensors, noise, signal delay and of course bugs.
The simulation models also include a steering law for the SPCMG with singularity avoidance and a model of the gimbal dynamics that limit acceleration and velocity of the gimbal.

The simulations and subsequent development of control as well as sizing approaches were systemized through the definition of three crane-cmg applications: dampening, part rotation and process compensation.
This definition helped distinguishing the diverse requirements and interactions of the system.
While the part rotation is akin to CMG applications in spacecraft, dampening is more related to the roll reduction systems in boats.
The addition of process compensation means that while we can borrow from certain parts of spacecraft design and particularly from the engineering of ship gyroscopes, novel control and sizing approaches are required to fully utilize the CMG's potential for cranes.
This combination is also what sets apart this work from prior crane stabilization efforts, which only focus on stabilization and limit themselves to a single CMG.

In the chapter on controller design this work develops an integrated control approach for the combination of the three defined applications.
From a review of existing crane dampening controllers, and control of underactuated systems, we show that a simple PD$\alpha$ controller is capable of dampening the double pendulum using torque produced by the CMGs.
The process compensation utilizes the fact that the process is known in advance and controlled in a programmed manner.
By simulating the torques produced by the process in advance it should therefore become possible to compensate these torques that would otherwise excite the pendulum.
We use such simulations to also generate example requirements for the compensation of several paths executed with a small industrial robot.
The rotation controller arises naturally from the dampening controller, once one extends the system to three dimensions.
All controllers require an understanding of the moment of inertia of the platform and load.
This can be estimated using conventional techniques from the understanding of the torque being produced and the observed accelerations of the system.

The simulations discussed in this work show the validity of this approach and create the understanding required to develop the sizing of CMGs for cranes.
In the chapter on sizing we see how the combination of the three applications and associated controllers create a certain dilemma.
We can see that CMGs capable of producing the torque with an agility suited for process compensation and part rotation are very feasible.
The issue of gyroscopic reaction torques caused by rotation of the system having to be sustained by our gimbal motors is very limited or highly controllable in these cases.
During processes compensation we ideally should have a static platform and the base rate during part rotation is governed by our desired rotation speed.
During dampening though the base rate is governed by the crane parameters and easily reaches velocities similar to those of our gimbals in the other applications.
Given the relationship of torques and velocities in a CMG system this leads to high reaction torques giving rise to high gimbal motor torque requirements.
This is exacerbated by the fact that dampening performance is highly dependent on the size of the momentum envelope.

This dilemma is why reducing the reaction torques caused by our base rates during dampening is the critical issue in getting CMGs to be a useful addition for cranes.
From the simulations performed in this work it seems possible to extend the CMG control and steering laws so as to limit the reaction torques by forcing the momentum vectors into alignment with the axis of rotation during the periods of high velocities.

------------

Control moment gyroscopes have the potential to change the way we use cranes and with that change the way we not only build but generally how we can think about automation in large workspaces.
I hope that this work goes towards showing and understanding this potential.

Gyroscopes make my brain hurt.
I hope that the explanations, models and discussions in this work help others avoid some of the same headaches as they go about solving the many challenges ahead for the realization of the potential outlined in this work. 
