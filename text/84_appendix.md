
# Appendix {#sec:appendix}

## CMG Variables

@Fig:cmg-data lists the properties of the SPCMG used in this work.

![Properties of the SPCMG with associated symbols and units.](./figures/cmg-data.png){ #fig:cmg-data }

The angular momentum of the gyroscope can be determined as follows:

\begin{align}
\text{h} &= I\omega \\
&= \frac{\pi\rho\text{d}}{2} (r_2^4 - r_1^4) * \omega
\end{align}

Some useful conversions to SI-Units:

\begin{align}
\text{rpm} \cdot \frac{\pi}{30} &= \text{rad}/s \\
\text{g}/\text{cm}^3 \cdot 1000 &= \text{kg}/\text{s}
\end{align}

## Equations of Motion and Simulation using Python

### 2D Point Mass Double Pendulum { #sec:2d-pointmass-eom}

Prior to obtaining the equations of motion for more complex cases, I obtained those of a point mass double pendulum.
The following code uses the SymPy Python library which allows us to perform symbolic calculations.
The code also validates our results against known equations of motion.

```{.python include=code/double-pendulum-2d-lagrangian.py}
```

Subsequently we can copy the resulting equations into a second program to simulate the pendulum.
Note how even though we are using symbolically identical equations, the simulation results begin to differ after a while.
This is a lovely example of numerical inaccuracy in computers and also how minimal changes in a chaotic system  like a double pendulum can cause increasingly large differences in behavior.

```{.python include=code/double-pendulum-2d-simulation.py}
```

![Validation of the equations of motion generated using the above SymPy code against those taken from [@HillLearningScientificProgramming2016]. Note how symbolically equal equations can lead to different result due to numerical inaccuracies in computers.](figures/cas-lit-comparison.svg){ #fig:cas-lit-comparison short-caption="Validation of SymPy derived equations of motion against literature"}

### 2D Point Mass and Distributed Mass { #sec:2d-distmass-eom }

The following code derives the equations of motion for a double pendulum where the second pendulum is a distributed mass.
Note that this assumes that the rotational inertia `I2` is provided relative to the axis of rotation lying in `m1`.

```{.python include=code/double-pendulum-2d-distmass-lagrangian.py}
```

```{.txt include=code/double_pendulum-2d-distmass-eom.txt}
```

### 2D Double Pendulum with Controller { #sec:2d-dp-wcontroller }

The following code extends the python simulation to include the PD$\alpha$ controller by including it in the equations of motion.
It also allows for the visualization of the load as a moving and rotating box.
The code was also cleaned up in comparison to the other simulation code.

```{.python include=code/dp-2d-distmass-controller.py}
```

### 2D Double Pendulum with Controller and Momentum Limit{ #sec:2d-dp-wcontroller-limit }

The following is a crude extension of the equations of motion to include a momentum envelope limit.
This is useful for simulating the effect of different sized CMGs on dampening.
Note that these equations do not limit the torque dynamics. 

```{.python include=code/dp-2d-distmass-limited-momentum.py}
```

## 3D Point Mass Double Pendulum { #sec:3D-pointmass-eom}

```{.python include=code/double-pendulum-3d-simulation.py}
```

### Spherical Coordinates

```{.python include=code/double-pendulum-3d-spherical-coords-lagrangian.py}
```

```{.txt include=code/double-pendulum-eom-3d-pointmass-spherical-coords.txt}
```

![Comparison of 2D and 3D double point mass pendulum given a small 2D excitation. As also discussed in @Sec:3d-pendulum the description of the kinematics using spherical coordinates leads to the model flipping between nearly identical solutions that cause major steps in the azimuthal angle. While the position of the pendulum is not visibly affected this does lead very high azimuthal angular velocities. The kinetic energy associated with these leads to the dampening of the oscillation we can observe in this plot. Note that the signs of $\theta_{1j}$ have been flipped where $|\theta_{2j}| > \frac{\pi}{10}$ to ease comparison of the two models.](figures/2d-3d-comparison-small-exitation-spherical-coords.svg){ #fig:2d-3d-comparison-small-exitation-spherical short-caption="2D and 3D pointmass double pendulums under small excitation"}

![Large excitation of double pendulum modelled with equations of motion derived using spherical coordinates. From left to right: front, side and top view. Note how the issues of spherical coordinates cause disturbances that quickly lead to chaotic out of plane motion.](figures/double_pendulum_3d_large_exitation_spherical.gif){ #fig:3d-spherical-large-exitation short-caption="Large excitation of spherical coordinate model"}

![Comparison of 2D and 3D double point mass pendulum given a large 2D exitation. Note how they are identical until for roughly the first five seconds and then begin to strongly deviate as the 3D pendulum begins to leave the plane of exitation. This is due to the issues discussed in @Sec:3d-pendulum and illustrated in @Fig:3d-model-angle-issues.](figures/2d-3d-comparison-large-exitation-spherical-coords.svg){ #fig:2D-3D-comparison-large-excitation-spherical short-caption="Comparison of spherical coordinate model with 2D model"}

### Projected Angles

```{.python include=code/double-pendulum-3d-lagrangian.py}
```

```{.txt include=code/double-pendulum-3d-pointmass.txt}
```

![3D double pendulum using projected angles under small 2D exitation. Note how we no longer have the jumps in the second angle observed in the simulations using spherical coordinates. The motion remains entirely in the XZ-plane. Note that this is no longer the case when the planar exitation lies in a plane outside of the XZ- or YZ-plane (see @Fig:3D-projected-large-exitation-diagonal).](./figures/3d-model-angle-issues-solution.svg){ #fig:3d-model-angle-issues-solution short-caption="Evaluation of projected angle model"}

![Comparison of 2D and 3D model (projected angles) of double pendulum with small planar exitation. Note the stark decrease in difference and lack of dampening when compared with the spherical coordinate model.](figures/2d-3d-comparison-small-exitation.svg){ #fig:2D-3D-comparison-small-excitation short-caption="Comparison of projected angle model with 2D model"}

## 3D Distributed Mass Pendulum{ #sec:distributed-mass-eom }

```{.python include=code/double-pendulum-3d-distmass-lagrangian.py}
```

```{.txt include=code/double-pendulum-eom-3d-distmass.txt}
```

```{.python include=code/cog-rotations.py}
```

```{.python include=code/double-pendulum-3d-distmass-simulation.py}
```

```{.python include=code/gh-data-import.py}
```

## Roof Array Workspace { #sec:roof-array-workspace}

The code below has been exported from an interactive Jupyter notebook that was used to generate the plots of the roof array momentum envelope for different roof angles.

```{.python include=code/momentum-envelope.py}
```
