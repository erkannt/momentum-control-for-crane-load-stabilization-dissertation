
# Sizing CMGs for Cranes

The models, simulations and experiments of the previous chapters provide a basis to understanding the behavior of the crane-CMG-process system.
This chapter attempts to summarize the insights gained regarding the sizing of the CMGs for such a system. 
Its first section covers sizing considerations for the three application categories set out earlier (dampening, rotation, process compensation).
The section first discusses the relationships between the requirements and system parameters before covering the sizing considerations specific to the crane-CMG system.

## Requirements

Recalling the properties of a CMG array, there are three main requirements:

- maximum torque produced (Nm)
- dynamics of the torque (Nm/s)
- torque capacity i.e. momentum envelope (Nms)

One thing to remember is that the envelope doesn't have to be symmetric and that the other properties are not homogenous within the envelope.
The steering law for the array will also change the torque availability depending on the chosen singularity avoidance techniques.

### Dampening

The performance requirements for dampening depend on the specific need for dampening.
Generally speaking though the sizing will be informed by:

- amount of excitation to dampen
- crane and load parameters
- max duration/swings until dampened

The section on modeling cranes and loads (@sec:crane-params) covers ways how one might estimate the relevant parameters, including the amount of excitation one can expect.
The chaotic interaction inherent to a double pendulum makes it difficult to create a way of determining/estimating the time it will taken a given CMG array to to dampen an excitation.
Looking at the dampening simulations of different capacity CMGs (@fig:spcmg-avoidance-animation) we can nevertheless understand the basic behavior during dampening.

The dampening controller will generate torque until the CMGs saturates i.e. its capacity (Nms) is consumed in one direction.
As the pendulum reverses direction the CMGs move out of saturation as the commanded torque also reverses direction.

Therefore I expect there to be a way to estimate the number of oscillations a CMG array requires to dampen a given pendulum.
I am guessing that the estimation will relate the momentum envelope of the array with the angular momentum of the two links.
This momentum in turn depends on the moment of inertia and maximum rotational velocity of the two links.
The developed models permit us to at least estimate the dampening performance by varying the momentum envelope and observing dampening performance (@Fig:limited-momentum-animation and @Fig:limited-momentum-plot, for code see sec:2d-dp-wcontroller-limit)
and thereby derive the necessary requirements for the subsequent sizing of the CMG array.
These simulations also provide a useful rule of thumb for the dampening performance: doubling the momentum envelope halves the number of swings it takes to dampen the crane.

![Simulation of dampening with differently sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-controller-limited-momentum.gif){ #fig:limited-momentum-animation}

![Lower link angle, torque used and position in momentum envelope for dampening with different sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-2d-distmass-limited-momentum.svg){ #fig:limited-momentum-plot}

Depending on the cause of excitation one might have to further increase the momentum envelope.
In the discussed dampening simulations one can see that dampening can leave the CMG array in a state away from the center of its momentum envelope.
If the processes compensations require a certain volume of momentum, one could increase the envelope to ensure sufficient volume remains after dampening.
Alternatively, as discussed in the controller design section, one could develop dampening control that extends the dampening duration but leaves the CMG array closer to the center of it momentum envelope. 

### Part Rotation

Rotating a load around the axis of the lower link is very much like trying to orient a spacecraft using momentum control devices.
The sizing is fairly straightforward and we can look to the spacecraft literature.

For satellites as well as part rotation the speed of rotation is usually not the main concern.
Instead we are interested in how long it will take to rotate to the desired position.
This of course depends on the rotation speed, but also on the maximum acceleration and jerk (derivative of acceleration).
This is particularly true for short rotations where one might not reach the maximum speed before having to begin decelleration.
See [@LeveSpacecraftMomentumControl2015, sec. 3.1] for an in depth discussion of this and how the duration of the jerk- and acceleration-limited regime can be derived from the relationship between maximum jerk, acceleration and velocity.

While the optimization of these relationships is of great relevance to spacecraft design, for the part rotation on cranes we can assume that rotation performance is mostly concerned with large rotations.
As such the sizing requirements can be simplified to:

\begin{equation}
\omega = \frac{h}{I}
\end{equation}

Where $\omega$ is the desired rotation speed of the platform/load/part, $I$ its moment of inertia about the axis in line with the lower link and $h$ the combined angular momentum of the gyroscopes in the CMG array.

### Process Compensation

Process compensation brings with it the most complex and demanding requirements.
As discussed in the simulations of the robot paths, we need to look at the peak torque, torque dynamics and total torque consumption.
By optimizing the robot paths or trading dynamics for consumption, the design of the process can significantly change the requirements.
It is therefore most likely beneficial to develop tools that provide a short feedback loop for the process designers.

This work provides an example of such a tool with the ability to evaluate the requirements of a parametric robot path made with KUKAprc.
Currently this is still a multi-step process that could certainly be more tightly integrated.
The simulation of the obtainable path accuracy through the use of process compensation currently does not take into account the ability of the robot to adapt to deviations of its base.
Nevertheless an estimation of the path accuracy without such additional compensation techniques has been shown in @Sec:robot-comp and the existing tools can already provide the fundamental requirements of Nm, Nm/s and Nms for the process compensation.
The interaction with additional robot based compensation might lead to an increase in the torque dynamics requirements, but the torque and envelope requirements should remain similar.

## Sizing of CMGs

### Parameter Relationships

The various requirements discussed above are illustrated in @Fig:cmg-reqs.
Having determined the requirements we can move on to understanding the relationships between the various parameters of the CMG array.
These are illustrated in @Fig:cmg-params.

![Illustration of the requirements stemming from the different CMG tasks.](./figures/cmg-reqs.png){ #fig:cmg-reqs }

![Illustration of the relationship between the parameters of a CMG array and crane.](./figures/cmg-param-relationships.svg){ #fig:cmg-params }

Beginning with the gyroscopes, we have the moment of inertia of the rotor.
This can be affected by the density of the material as well as the shape and size of the rotor.
The simplest form are cylinders with cylindrical shells providing better mass utilization.
Another common design are spherical rotors which have a side benefit of causing less changes to the moment of inertia in the array/platform/spacecraft when rotated about their gimbal axis.
At high velocities rotors can experience significant forces, which needs to be taken into consideration when selecting the material and sizing the rotor.

The moment of inertia and rotor speed give us the momentum for each gyroscope in the array.
A naive approximation of the size of the momentum envelope can be obtained by summing the moments of all gyroscopes of the array.
The actual envelope shape depends on the chosen array type and parameters.
As discussed in the section on CMG envelopes, one can utilize asymmetric envelopes to match asymmetric torque requirements.
An array tasked predominantly with large-part rotation could be designed to have its largest extent in the Z-axis whereas an array tasked with dampening would prioritize the other axes.

The size of the gyroscope motor is governed by the required velocity, desired spin up time and amount of friction in the system.
If one is patient with the spin up and creates a low friction system (large gyroscopes often run inside of a vacuum to reduce drag) the gyroscopes' motor can be very modest.

The moment of inertia of the rotor around the gimbal axis can also be used as an approximation for the sizing of the gimbal motors.
While the gimbal motor also has to overcome the moment of inertia of the housing etc. the gyroscopes rotor will be the major contributor to the gimbals inertia.
As we saw in the simulations of the SPCMG, during dampening the sizing of the gimbal motor's torque is dominated by two factors:

- required torque agility
- reaction torque caused by the baserate

The required torque agility $\dot\tau_{B}$ depends on the momentum of CMG array, the inertia of the gimbal assembly and the torque of the gimbal drive:

\begin{equation}
\dot\tau_B \approx h_{Array} \cdot \frac{I_{Gimbal}}{\tau_{Gimbal}}
\end{equation}

The reaction torque depends on the momentum of the gyroscope and baserate i.e. the angular velocity experienced by the platform.
Since our CMG arrays should operate in three dimensions and under diverse loads we must assume the worst case i.e. that the momentum vector of the gyroscope will lie orthogonal to the angular velocity.
Since the torque produced by the CMG also depends on the momentum of the gyroscope but on the gimbal velocity instead of the base rate, the following relationship  holds true (see section 3.2.6 of [@LeveSpacecraftMomentumControl2015]) for full discussion): 

$$ \frac{\omega_{gimbal}}{\omega_{system}} = \frac{\tau_{system}}{\tau_{gimbal}} $${#eq:torque-velocity-relation}

In spacecraft this relationship is highly critical as the torque of a motor is strongly linked to its weight.
As a terrestrial application we have more flexibility regarding weight.
Furthermore, unlike space applications in our case the baserate is (apart from part rotation) not the desired output of the CMGs.
Instead the baserate originates from the oscillatory nature of the crane as a pendulum.
The relevance of this difference will be discussed in the following section.

The parameters, system characteristics and requirements create connected graph.
To make sizing easier we can place all equations involved in a spreadsheet (see @Fig:cmg-sizing).
This way one can quickly run through various parameters.

![Spreadsheet of the most relevant CMG parameters including the equations that link them together.](./figures/cmg-sizing.png){ #fig:cmg-sizing }

The spreadsheet makes a distinction between torque dynamics at rest and those during the worst case.
In such a case the momentum of the gyroscopes would be aligned with the axis of rotation of the array/base and we would be trying to move the gimbal in the opposite direction of the precession caused by the gyroscopic reaction.
This would lead to the gimbal motor having to overcome the entire reaction torque prior to being able to produce any of the desired torque.
To illustrate this the spreadsheet subtracts the reaction torque from the maximum torque of the gimbal motor.

To provide a better intuition of the characteristics of the CMGs the spreadsheet also calculates the angle of rotation required by the gimbal motor to reach its maximum speed from a standstill.
In an SPCMG array one will run into a singularity after 90° when starting from a neutral position, therefore this value gets highlighted yellow once it goes above 90°.
In other arrays the singularities will be different, but one will most likely struggle to achieve the maximum gimbal velocity if one requires more than 90° to reach it.

The spreadsheet does not take friction or the exact shape of the momentum envelope into account.
The actual inertia of a gimbal assembly will also be higher than the inertia of just the gyroscope's rotor.
All of this can most likely be taken into account with scaling factors, once one has some prototypes to base them off.

### Sizing CMGs for Cranes { #sec:sizing_for_cranes }

The challenge of sizing CMGs for cranes is the unique combination of requirements arising from the three application cases of damping, rotation and process compensation.
While commercial applications and sizing experience exist for spacecraft control (similar to part rotation) and roll stabilization (similar to dampening) the addition of process compensation as well as the need to operate around three axis creates novel challenges.
The core challenge is the high base rate that our CMGs experience when they are attached to a swinging crane.

In a spacecraft the baserate is dictated by the agility requirements, which in turn leads to requirements regarding the output torque of the CMGs.
The relationship of torques and velocities in a CMG (see @Eq:torque-velocity-relation) lead the sizing of the gimbal and gyroscope motor.
Unlike the case of crane dampening, the reaction torque here is self inflicted.
Also, since most maneuvers will produce a net change of zero in the CMG array's momentum, the size requirements regarding the envelope are much smaller than in our cases, where we have to soak up external influences.

While the base rate in ship stabilization is more akin to our base rate, we can't imitate their solutions.
In ship stabilization the base rate i.e. the roll is actually utilized, as the precession causes exactly the gimbal movement necessary to produce torque counteracting the roll of the ship.
Gimbal actuation is only used to assist the gyroscope in overcoming friction, limit the response and avoid hitting the singularities.
In our case though, we also want to be able to use the same CMGs to provide torque compensation while at the same time dampening oscillations.

Given the requirements for dampening and process compensation previously discussed, the size of the momentum envelope is paramount to the usefulness of the CMGs for crane applications.
Obviously, the size of the envelope is governed by the momentum of the gyroscopes.
So given a certain baserate we will always have to deal with reaction torques that outweigh the gimbal torque requirements resulting from torque dynamics requirements (see discussion in @Sec:cmg-pendulum-interaction and @Sec:torque-issue).

To make CMGs feasible for an application in cranes, we must therefore find ways to alleviate the baserate or to be more precise: its impact on our gimbal motor sizing.
This is the key issue confronting us and the following solutions come to mind:

- limit CMG operations to certain wind loads and crane movement speeds
- introduce a clutch mechanism to the gimbals
- align the gyroscopes momentum with the baserate's axis

As we can see in the simulations of the SPCMG during dampening (@Fig:spcmg-avoidance-animation), the momentum vector of the gyroscopes passes through a configuration parallel to the axis of rotation of the platform as it is dampened.
It should therefore be possible to add a switching behavior or otherwise modify the controller to ensure a certain amount of alignment in relation to the current baserate and its acceleration.
The animation in @Fig:torque-issue-zero, hopefully helps illustrate the challenge.
In the current configuration the gimbal experiences zero reaction torque through the entire pendulum's swing.
But as the gimbal isn't moving, there is also no torque produced to dampen the oscillation.
Imagining that yellow denotes a reaction torque harmful to the gimbal assembly, the challenge is to rotate the gimbal past the midpoint prior to it turning yellow.

![Illustration of the potential reaction torque acting on the gimbal, depending on the current base rate and gimbal angle. Note how as the gimbal axes are held parallel to the axis of rotation no reaction torque is produced. The blue arrow is the angular momentum of the gyroscope, it therefore remains constant. The green arrow is the angular velocity that the CMG experiences due to the pendulum's oscillations, i.e. the baserate. The semicircular bar denotes in color the reaction torque that the gimbal axis would experience at the various gimbal angles.](./figures/torque_issue_zero_reaction.gif){ #fig:torque-issue-zero }

It is also important to note that the direction of reaction torque is in line with the desired rotation of the gimbal.
Under a well designed control regime the maximum allowable reaction torque might lie above the maximum torque rating of the motor and other part of the gimbal assembly.
As the motor and reaction torque are pushing in the same direction during the dampening process, the limits might actually lie in the current limits and electronics design of the controllers.

All of this could lead to a stark reduction in the impact of the reaction torque as compared to the the worst case scenario assumed in the sizing spreadsheet.
Nevertheless I would recommend adding dedicated points of failure for gimbal motor couplings and perhaps even means to mechanically arrest the gimbals' motion should a failure of the coupling occur.
