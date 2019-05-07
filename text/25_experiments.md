
# Experiments

## Pendulum Simulation

### 2d Model

We've already seen some of the interaction that occurs with a double pendulum in @Sec:2dpendulum, with the lower pendulum causing higher frequency oscillations to be overlaid.
In @Fig:distmass-impact-animation and @Fig:distmass-impact-plot we can see how the rotational inertia of the lower mass changes the interaction of the two part of the pendulum.

![Difference between an double pendulum with two point masses and one where the lower mass is modeled as a distributed mass.](./figures/impact-of-rotational-inertia.gif){ #fig:distmass-impact-animation }

![Angles and angular velocity comparison of point mass and distributed mass pendulum.](./figures/dp-2d-distmass-inertias.svg){ #fig:distmass-impact-plot }

### 3d Model

Now lets look at some simulations of our 3d pendulum.
Just to validate the model let us create some 2d excitations.
In @fig:3d-projected-large-exitation we see that the motion remains in the plane of excitation as we would expect.
Note that the movement is not identical to that of the 2d model, due to the fact that minuscule numerical errors lead to noticeable changes in a chaotic system such as a double pendulum (see discussion in appendix @sec:2d-pointmass-eom).
This is also most likely the reason that once we rotate the plane of excitation (@Fig:3d-projected-large-exitation-diagonal) the motion breaks out of the plane at some point.

![Large exitation of double pendulum modelled with equations of motion derived using projected angles. From left to right: front, side and top view. Note how the path begins to differ strongly when compared to the simulation using the 2D model. This is a prime example of how minor changes can cause large differences in chaotic systems like a double pendulum.](figures/double_pendulum_3d_large_exitation.gif){ #fig:3d-projected-large-exitation }

![Large out of plane exitation of double pendulum modelled with equations of motion derived using projected angles. From left to right: front, side and top view. Note how the small inaccuracies cause motion outside of the original plane of exitation. These deviations quickly become chaotic for larger exitations.](figures/double_pendulum_3d_Large_Exitation-diagonal.gif){ #fig:3d-projected-large-exitation-diagonal }

As we move to the 3d model with distributed mass another effect occurs.
In @Fig:distmass-sim-gh the pendulum was given a 2d excitation but also the mass was given an angular velocity around the axis of suspension.
The break from the 2d plane occurs immediately, which is most likely due to the impact of gyroscopic reaction due to the pendulum motion and the inertia around the axis of suspension.

![Simulation of a distributed mass hanging from a point mass. Initial excitation lies in a plane, but the mass is also given an angular velocity. Note how the pendulum breaks out the of the plane. Most likely due to gyroscopic effects.](./figures/distmass-sim-gh.gif){ #fig:distmass-sim-gh }

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
