
# Outlook and Conclusion

> "Once the conditions for helicopters are in place, it’s helicopter time, and so you get helicopters, everywhere, all at once." -- Cory Doctorow @citation-needed

Prior to summing up this work I would like to discuss the assumptions and associated limits of the currently used models.
Given these limits and some of the insights gained through our experiments I will then make recommendations regarding the acute developments needed to progress this work but also some ideas regarding questions and areas that need to be covered to make CMGs a useful tool for cranes in general and the construction site in particular.

## Assumptions of Current Models

Cows aren't spheres, but sometimes it is sufficient to model them as such to gain valuable insights.
Likewise the models in this work make some stark simplifications regarding the crane-cmg-process system.

In no particular order the most significant of these are:

- ropes are modeled as stiff links capable of transmitting torque
- no drag or friction
- no external forces (including those of robot)
- no process forces or torque in robot simulations
- no sensor noise or control loop delay

In the sizing calculations we are also not including any considerations for the specific shape of the momentum envelope, its singularities and changing dynamics as one moves through it.
Most of these assumptions do not limit the conclusion made from the simulations, but they do limit further understanding of the system and in particular the development of controllers.

## Next Steps for Development

For the compensation task the most critical model issue is the lacking ability to include external forces acting upon the lower pendulum.
In a simple pendulum the forces could simply be modeled as additional torques by multiplying the force with the length of the link.
In a double pendulum though, the forces will also partially cause motion in the upper link, depending on link lengths, weights and inertias.
We sadly cannot include forces into the Langrangian directly, instead they are additional source terms that need to be added after solving the Euler-Lagrange equations.
This is what we did for the application of external torques, where we could relatively simply obtain the impact on the angular acceleration.
For forces though, this is complicated by the factors described above.

Given that one will later on wish to also extend the model to include the remainder of the crane, my recommendation would be to move to a modular multibody simulation into which one integrates the model of the CMG dynamics.
This should be possible in both Modelica or Simulink Simmechanics.
While the CMG array could also me modeled using this approach I would recommend the use of the explicit model also used in this work, as it makes it possible to distinguish the various torque components, which helps in understanding the complex nature of the gyroscopic system.

To be able to develop and validate steering and control of the desired four CMG roof array required for the move to 3d, either a new model of the crane as just described or the existing 3d equations of motion could be used.
The existing model will already allow developments regarding the dampening and rotation applications.
The new model is required to validate the compensation application in full, due to this application involving external forces in addition to torques.

To move the controller to 3d one will have to translate the error about three axis into a 3d target torque.
This of course in turn necessitates the extension of the SPCMG model to a four CMG roof array with an implementation of a suitable steering law.
Once these components are in place it becomes possible to analyze the controllers performance under the limitations resulting from the agility and singularities of the CMG array and the chosen steering law.

A priority for the development of the 3d controller should be the inclusion of the reaction torque limiting strategy discussed at the end of the previous chapter on sizing.
Limiting the reaction torque experienced by the CMGs through alignment of momentum and rotation axis is the critical component required to make CMGs useful for crane based applications.
The development described in this section therefore mostly outline the critical path to a state where the efficacy of such a strategy can be validated through simulations.

Apart from the the reduction of reaction torques the other major question is how well a CMG array is able to provide a stable platform for robotic or other processes.
This work was able to answer this regarding the compensation of torques, leaving the error produced by the forces (which can't be directly compensation through CMGs) to the dampening controller or an optimization of the robots path and controller.
The extension of the models to include external forces as would be experienced at the robot base is remaining step needed to begin development of robot path optimization as well as robot based compensation strategies and validation of said strategies as well as the efficacy of damping the remaining error.

\todo{read up on how the input to the CMG steering is shaped}

## Other Work Required

Beyond these critical next steps resides a plethora of interesting research and engineering challenges.

Once the pendulum, CMG and robot-multibody models have become more tightly integrated one could begin with the development and validation not only of control strategies that utilize the robot to compensate positional errors from pendulum oscillations.
By integrating the models into robot path planning and by using either the real robot as a hardware-in-the-loop system or a more realistic robot simulator, one could also begin finding optimization strategies that increase the process accuracy through changes to robot paths and execution speeds/accelerations.

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
Note that the gyroscopes of CMGs have been used as additional energy storage to handle short higher loads in both marine application and spacecraft experiments @citation-needed.

As with all research continuing and ever more extensive validation will be required.
The collection of real crane motion data for instance would be valuable to validate the crane parameter estimations and dampening requirements.
As the simulation tools are improved more realistic and diverse processes will emerge that utilize the crane-CMG system and provide valuable input regarding the compensation and rotation requirements.

## Conclusion

- sota regarding space and ships
- developed understanding of the problem
- basic toolset for simulation, validation and sizing