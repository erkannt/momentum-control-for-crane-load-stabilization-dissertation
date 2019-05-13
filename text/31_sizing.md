
# Sizing CMGs for Cranes

The models, simulations and experiments of the previous sections provide us with a growing understanding of the behavior of the crane-cmg-process system.
In this section we try to sum up how how one might go about sizing a CMG array for a given crane or process.
First we will go through the requirements for the three application categories (dampening, rotation and process compensation) and then move on to describe how the various requirements and system properties interact.

## Requirements

Recalling the properties of a CMG array, there are three main requirements we can formulate for a CMG array:

- maximum torque produced (Nm)
- dynamics of the torque (Nm/s)
- torque capacity i.e. momentum envelope (Nms)

One thing to remember is that the envelope doesn't have to be symmetric and that the other properties also then won't be symmetric.
The steering law for the array will also change the torque availability with the chosen singularity avoidance techniques.

### Dampening

The performance requirements for dampening depend on the specific need for dampening.
Generally speaking though our sizing will be informed by:

- amount of excitation to dampen
- crane and load parameters
- max duration/swings until dampened

The section on modeling cranes and loads (@sec:crane-params) covers ways how one might estimate the parameters relevant here, including the amount on excitation we can expect, given the crane parameters.
The chaotic interaction inherent to a double pendulum make it difficult to create a way of determining/estimating the time it will taken a given CMG array to to dampen an excitation.
Looking at the dampening simulations of different capacity CMGs (@fig:spcmg-avoidance-animation) we can understand the basic behavior during dampening.
The dampening controller will generate torque until the CMGs saturates i.e. its capacity (Nms) is consumed in one direction.
As the pendulum reverses direction the CMGs move out of saturation as the commanded torque also reverses direction.

Therefore I expect there to be a way to estimate the number of oscillations a CMG array requires to dampen a given pendulum.
I am guessing that the estimation will relate the momentum envelope of the array with the angular momentum of the two links.
This momentum in turn depends on the moment of inertia and maximum rotational velocity of the two links.

The developed models at least permit us to estimate the dampening performance and vary the momentum envelope (@Fig:limited-momentum-animation and @Fig:limited-momentum-plot, for code see sec:2d-dp-wcontroller-limit) and thereby derive the necessary requirements for the subsequent sizing of the the CMG array.
These simulations also provide us with a useful intuition/rule of thumb for the dampening performance: doubling the momentum envelope halves the number of swings it takes to dampen the crane.
Given that the frequency of a pendulum is straightforward for small oscillations the number of swings immediately give us the dampening duration.

![Simulation of dampening with different sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-controller-limited-momentum.gif){ #fig:limited-momentum-animation}

![Lower link angle, torque used and position in momentum envelope for dampening with different sized momentum envelopes i.e. CMG workspace sizes.](./figures/dp-2d-distmass-limited-momentum.svg){ #fig:limited-momentum-plot}

Depending upon the cause of excitation one might have to further increase the momentum envelope.
In the discussed dampening simulations one can see that dampening can leave the CMG array in a state off center of its momentum envelope.
If the processes compensations require a certain volume of momentum, one could increase the envelope to ensure sufficient volume remains after dampening.
Alternatively, as discussed in the controller design section, one could maybe develop steering of the dampening control that extends the dampening duration but leaves the CMG array closer to the center of it momentum envelope. 

### Part Rotation

Rotating a load around the axis of the lower link is very much like trying to orient a spacecraft using momentum control devices.
The sizing is fairly straightforward and we can look the the spacecraft literature.

For satellite as with part rotation the speed of rotation is usually not the core interest, instead we are interested in how long it will take us to rotate to the desired position.
This of course also depends on the rotation speed, but also on the maximum acceleration and maximum jerk (derivative of acceleration).
This is particularly true for short rotations where one might not reach the maximum speed before having to begin breaking.
See chapter ??? of @citationneeded for a in depth discussion of this and how the duration of the jerk- and acceleration-limited regime can be derived from the relattionships between ???.

While the optimization of these relationships is over relevance to spacecraft design, for the part rotation the sizing requirements regarding part rotation can be boiled down to:

\begin{equation}
\omega = \frac{h}{I} [rad/s]
\end{equation}

Where $\omega$ is the desired rotation speed of the platform/load/part, $I$ its moment of inertia about the axis in line with the lower link and $h$ the combined angular momentum of the gyroscopes in the CMG array.
When selecting the desired rotation speed remember to take into account that small rotation angles will fall into the jerk- or acceleration regime.
Assuming a bang-bang-jerk control one can use the equation in @citationneeded mentioned above to determine these from the gimbal parameters obtained in the later sizing stages.
This and and subsequent adjustment of the CMGs sizing should only be necessary when rotation performance is central to the chosen crane-cmg application.
Given the relatively slow movement speeds of cranes with loads attached I would assume that this gives one ample time to perform rotations and that high rotation agility will be a rare requirement. 

### Process Compensation

Process compensation brings with it the most complex and demanding requirements.
As discussed in the simulations of the robot paths, we need to look at the peak torque, torque dynamics and total torque consumption.
By optimizing our robot paths or trading dynamics for consumption the design of the process can majorly change the requirements.
It is therefor most likely beneficial to develop tools that provide close feedback loops to the process designers.
This work provides an example of such a tool with the ability to evaluate the requirements of a parametric robot path made with KUKAprc.
Currently this is still a multi-step process that could certainly be more tightly integrated.
  
The simulation of the obtainable path accuracy through the use of process compensation currently does not take into account the ability of the robot to adapt to deviations of its base.
Nevertheless an estimation of the path accuracy without such additional compensation techniques has been shown in @sec:ref-needed and the existing tools let us already obtain the fundamental requirements of Nm, Nm/s and Nms for the process compensation.
The interaction with additional robot based compensation might lead to an increase in the torque dynamics requirements, but the torque and envelope requirements should remain similar.


The various requirements and means for their determination are illustrated in @Fig:ref-needed.

\missingfigure{Illustration of requirement derivation of the three applications}


## Sizing of CMGs

### Parameter Relationships

TBD?: $\frac{\omega_{gimbal}}{\omega_{system}} = \frac{\tau_{system}}{\tau_{gimbal}}$

- derive gimbal torque requirements:
  - from dynamics
  - from reaction torques
- moment of inertia of gyro/gimbal
- gyro motors
    - spinup times
    - friction, alignment

### Feasability Analysis

- gimbal torques
- gyro speeds and inertias
- size and weight of setup