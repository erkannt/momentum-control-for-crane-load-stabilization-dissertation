
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

- desaturation/CoG compensation with moving weight
- 3d hardware prototype
  - improve realtime capabilities/controller validation workflow
  - improve gyro quality
  - higher torque gimbal motors to ensure sufficient headroom
- optimization of robot paths (look to space work)
- desaturation during dampening
- add crane movement
- collect real crane motion for validation
- power requirements for operation
- construction site suitable hardware design
- sensor(s) and filtering
    - implementation of the inertia estimation
    - dealing with vibrations
- validation of controller under more simulated and hw scenarios
- add controller for robot utilizing compensation

## Conclusion

- sota regarding space and ships
- developed understanding of the problem
- basic toolset for simulation, validation and sizing