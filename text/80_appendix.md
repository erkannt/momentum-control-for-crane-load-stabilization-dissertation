
# Appendix{.unnumbered}

## CMG Variables

The SPCMG used in this work has the following properties:

Property                       Symbol                  Size   Unit
----------------------------  --------------------- -------   -----
Density of Gyroscope Disc      $\rho_{gyro}$          7,9      $\text{g}/\text{cm}^3$
Gyroscope Speed                $\omega_{gyro}$        5000       rpm
Inner Gyro Radius              $r_1$                  4          cm
Outer Gyro Radius              $r_2$                  7          cm
Gyro Thickness                 $d$                    3          cm
Max. Gimbal Speed              $\dot{\delta}_{max}$   400         rpm
Max. Gimbal Accelleration      $\ddot{\delta}_{max}$  42494       rpm/s

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


## Other Stuff Looking for a Home

- Workspace of a Roof-Array
- spin up times
- robot tasks and their forces
- gimbal simulation model and validation
- physical demonstrator
- simulink model re: steering law
- IMU sensor
