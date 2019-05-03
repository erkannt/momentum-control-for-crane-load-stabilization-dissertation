
# Experiments

## Pendulum Simulation

### 2D Pendulum

We've already seen some of the interaction that occurs with a double pendulum in @Sec:2dpendulum, with the lower pendulum causing higher frequency oscillations to be overlaid.
Now let us look at how the parameters of the system affect its behavior.

\missingfigure{Comparison of double pendulum with different rotational inertias.}

\missingfigure{Comparison of different pendulum lengths.}

\missingfigure{Double pendulums using the selected crane parameters and those of our prototype}

### 3D Pendulum

\missingfigure{2d excitation of 3d pendulum}

\missingfigure{2d excitation with rotating mass}

- gyroscopic reaction causes rotation as we have no friction

### Dampening Controller

\missingfigure{Dampening of different inertias, PD values}

\missingfigure{Different lengths with same PD values}

### Pendulum-CMG Interaction

\missingfigure{Illustration of SPCMG limits during dampening}

\missingfigure{CMG torques at different base rates}

- base rates vs. pendulum length vs. gyro inertia
- reaction torque vs. array design vs. CMG orientation
- explain why passive stabilisation is not possible

## Robot tasks

\missingfigure{selected robot task}


![Comparison of the base torques for the same path performed and two different speeds. At low speeds the longer time spent out of balance require a larger momentum envelope while higher robot speeds require greater gimbal agility to achieve the momentum dynamics.](./figures/robot-load-speedcomparison-plot.jpg){#fig:robot-load-speedcomparison-plot}


We can distinguish between three types of torque:

- torque from robot motion and its own inertia
- process forces transmitted from the tool to the base
- torque from imbalance

Conclusions:

- trade off between Nm/s and Nms due to time spent out of balance
- it might make sense to add sliding weight to keep COG inline with rope

## Simulated Process Compensation

\missingfigure{Video of spcmg with robot underneath, with and without forces}

\missingfigure{path deviation due to forces of robot}

- simulated base forces and torques
- deviation from path

## Hardware Experiments

### Prototype Setup

![CMGs used in the hardware prototype. The Design has only two custom parts (gyro wheel, mounting flange) with the rest begin off the shelf components (incl. made to measure shafts).](./figures/CMG-sidebyside.jpg){ #fig:cmg-plans }

![Hardware SPCMG prototype with robot attached to it. Gyros are in the aluminum cases with the gyro motors mounted on their sides. The gimbal motors hang underneath the gyros. The motor controller and power supply are mounted underneath the platform. The gyro controller, IMU and communication interface for these are mounted on top. Note that the rope suspension was rotated by 90° for the picture.](./figures/KR3_seitlich.jpg){ #fig:prototype-sideview }

\missingfigure{Image of custom PCB, case and controllers}

\missingfigure{gyro motor alignment mount}

- CMG Design
- Array
- performance values
- Motor Control
- Sensors
  - filters
- Issues
- Recommendations

### Tuning Controller on Hardware

\missingfigure{video of dampening hardware prototype}

\missingfigure{plots of dampening hardware prototype}

- validation of PDalpha controller
- tuning of parameters
