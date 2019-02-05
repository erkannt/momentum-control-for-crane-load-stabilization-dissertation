
# Experiments

## Robot tasks

- designed paths
- results for various execution speeds
- scale results with help of comparison with KR240 and torques listed in datasheets

We can distinguish between three types of torque:

- torque from robot motion and its own inertia
- process forces transmitted from the tool to the base
- torque from imbalance

Conclusions:

- trade off between Nm/s and Nms due to time spent out of balance
- it might make sense to add sliding weight to keep COG inline with rope

## Pendulum-Motion and CMGs

### Swinging and Torque

- comparison of basic and compoun model
- various crane params
- how does swinging work?
- tests of basic control appraoch
- abstract model > compare with simulink model > validate with demonstrator

### Passive Stabilization through CMGs

- diff between modelling applied base torque and full CMG model
- impact of current orientation of CMG inertia on stabilization >>> impact on steering law
- abstract model > compare with simulink model > validate with demonstrator
- rotation from rotation of crane vs. rotation from pendulum motion

### Study of Base Rates

- base rates vs. pendulum length vs. gyro inertia
- reaction torque vs. array design vs. CMG orientation

## Gimbal dynamics

- validation of gimbal model in simulink (appendix?)
