
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
\omega = \frac{h}{I}
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



## Sizing of CMGs

### Parameter Relationships

The various requirements and means for their determination are illustrated in @Fig:ref-needed.
Having determined the requirements we can move on to understanding the relationships between the various parameters of the CMG array.
These are illustrated in @fig:ref-needed.

\missingfigure{Illustration of requirement derivation of the three applications}

\missingfigure{Illustration of relationship between the various CMG array parameters.}

Beginning with the gyroscopes we have the moment of inertia of the rotor.
This can be affected by the density of the material as well as the shape and size of the rotor.
The simplest for are cylinders or for better mass utilization as close to a cylindrical shell as possible.
Another common design are spherical rotors which have a side benefit of causing less changes to the moment of inertia of the array/platform/spacecraft when rotated about their gimbal axis.
At high velocities rotors can experience significant forces, which needs to be taken into consideration when selecting the material and sizing the rotor.

The moment of inertia and rotor speed give us the momentum for each gyroscope in the array.
A naive approximation of the size of the momentum envelope can be obtained by summing the moments of all gyroscopes of the array.
The actual envelope shape depends on the the chosen array type and parameters.
As discussed in the section on CMG envelopes we create asymmetric envelopes to match asymmetric torque requirements.
An array tasked predominantly with large part rotation could be designed to have its largest extend in the Z-axis whereas an array tasked with dampening would do the inverse.

The size of the gyroscope motor is governed by the required velocity, desired spin up time and amount of friction in the system.
If one is patient with the spin up and creates a low friction system (large gyroscopes often run inside of a vacuum to reduce drag) the gyroscopes motor can be very modest.

The moment of inertia of the rotor around the gimbal axis can also be used as an approximation for the sizing of the gimbal motors.
While the gimbal motor also has to overcome the moment of inertia of the housing etc. the gyroscopes rotor will be the major contribution to the gimbals inertia.
As we saw in the simulations of the SPCMG during a dampening operation the sizing of the gimbal motors torque is dominated by two factors:

- required torque agility
- reaction torque caused by the baserate

The required torque agility $\dot\tau_{B}$ depends on the momentum of CMG array, the inertia of the gimbal assembly and the torque of the gimbal drive:

\begin{equation}
\dot\tau_B \approx h_{Array} \cdot \frac{I_{Gimbal}}{\tau_{Gimbal}}
\end{equation}

The reaction torque depends on the momentum of the gyroscope and baserate i.e. the angular velocity experienced by the platform.
Since our CMG arrays should operate in three dimension under diverse loads we must assume the worst case i.e. that the momentum vector of the gyroscope will lie orthogonal to the angular velocity.
This is particularly true for the dampening case which is most likely where the array will experience the highest angular velocities.
If the momentum vector were to lie parallel to the velocity their steering to rotate them toward an orthogonal orientation to produce the torque necessary for dampening, though it might be possible to conceive a controller that tries to avoid orthogonality during velocity peaks.

Since the torque produced by the CMG also depends on the momentum of the gyroscope and the gimbal velocity (instead of the base rate) the following relationship hold true (see @citation-needed) for full discussion): 

\begin{equation}
\frac{\omega_{gimbal}}{\omega_{system}} = \frac{\tau_{system}}{\tau_{gimbal}}
\end{equation}

In spacecraft this relationship is highly critical as the torque of a motor is strongly linked to its weight.
As a terrestrial application we have more flexibility regarding weight.
Furthermore as discussed previously unlike space applications in our case the baserate is (apart from part rotation) not what we desire to produce with the CMG.
Instead the baserate originates from the oscillatory nature of the crane as a pendulum.
Aside from limiting the baserate through limits on windspeed during operation or slower slewing speeds we might also be able to create hybrid dampening controllers where the gimbal motor doesn't try to resist the reaction torque but instead uses it to produce the desired gimbal velocities.
The impact of such a concept on the sizing of the gimbal motors most likely depends on the chosen CMG steering laws and how they desire to position the CMGs during a dampening operation.

### Feasability Analysis

The parameters, system characteristics and requirements create connected graph.
To make sizing easier we can place all equations involved in a spreadsheet (see @Fig:cmg-sizing).
This way one can quickly run through various parameters.

![Spreadsheet of the most relevant CMG parameters including the equations that link them together.](./figures/cmg-sizing.png){ #fig:cmg-sizing }

Things to note:

 - distinction between dynamics at rest and with worse case base rate
 - degrees to max speed as indicator if top speed is actually reachable
 - friction, gimbal hardware, shape of envelope not taken into account!
 - for dampening Nms more critical than Nm, but this is not taken into account in the usual sizing relationship!
 - need to ensure alignment of gimbal axis with base rate axis to avoid reaction torque
 - this is the key problem of combining dampening with compensation