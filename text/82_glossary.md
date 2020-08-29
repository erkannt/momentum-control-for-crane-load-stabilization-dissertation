
# Glossary {#sec:glossary}

CMG
:  Control Moment Gyroscope. A momentum control device consisting of a gyroscope mounted on a single gimbal (SGCMG) or dual nested gimbals (DGCMG). The distinguishing differences from the other common momentum control device, the reaction wheel, is that they utilize the effect of gyroscopic reaction torque for produce their output torque instead of relying on the gyroscopes motor. See @Sec:reaction-torque more information.

SPCMG
:  Scissored Pair Control Moment Gyroscope. A specific arrangement of two CMGs that results in their combined output torque being aligned along a constant axis. This simplifies their steering laws when compared to other array types. Their downside is that it requires three SPCMGs and hence six CMGs to create torque around all three spatial axes. See  @Sec:spcmg-steering for more.

Singularity
:  In the context of mechanisms a singularity is a certain configuration or state of the moving parts where the control or modelling of the system breaks down to a certain degree.
This can mean that the behavior after reaching the singularity is no longer predictable or that certain values become infinite or nondeterministic. 
An example of this for in an industrial robot can be seen in @Fig:singularity.

![Illustration of a singularity in a six-axis industrial robot. Once the two axis are in line they can in theory rotate an infinite amount with producing a lateral movement. The speed at which they have to rotate to maintain a constant lateral motion therefore also goes to infinity. Animation by Mecademic @WhatAreSingularities](./figures/mecademic.gif){#fig:singularity short-caption="Example of a robots's singularity"}

Null Space Motion
:  The term stems from the concept of state space describing all possible states of a system.
Null space is then the subspace in which changes of the state don't affect the output of the system. 
In robotics this means the end-effector remains motionless even though the robot axes are moving.
In CMG arrays this means the output torque isn't affected by the motions of the CMGs.
Another way of describing it, is that given a desired target e.g. torque, position, path there exist multiple solutions.
This redundancy can be used to optimize motions of the system while still producing exactly the desired output.

Error Torque
:  In the context of momentum control devices any deviation of the output torque from the target i.e. desired torque.

Jacobian
:  In the context of engineering the Jacobian matrix is the matrix of partial differential equations that describes the relationship between changes in a systems state and the systems output i.e. with $\boldsymbol{J}$ as the Jacobian, $\boldsymbol{x}$ as the output vector and $\boldsymbol{q}$ as the state vector:

$$ d\boldsymbol{x} = \boldsymbol{J} \cdot d\boldsymbol{q} $$

Pseudo-Inverse
:  A generalization of the inverse of a matrix that accommodates non-invertable matrices.
TODO: read Leve at al on their use of pseudo inverses

Center of Percussion
: The point on a pendulum where a perpendicular force leads to zero reaction force at its pivot point, due to the angular and translational acceleration cancelling each other out.

![Illustration of the center of percussion and how it relates to the reaction of a pendulum given the location of a force acting upon it. CC-BY-SA 4.0, Wikipedia user Qwerty123uiop](./figures/center-of-percussion.png){ #fig:center-of-percussion short-caption="Illustration of the Center of Percussion"}
