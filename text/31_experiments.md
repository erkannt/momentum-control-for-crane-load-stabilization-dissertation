
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

### 2D Pendulum

- comparison of basic and compound model
- various crane params
- tests of basic control appraoch
  - overlay frequencies in lower pendulum
- validation on demonstrator

### 3D Pendulum

- what changes???

### Pendulum CMG Interaction

- base rates vs. pendulum length vs. gyro inertia
- reaction torque vs. array design vs. CMG orientation
- explain why passive stabilisation is not possible
- explain how roof angle impacts gimbal sizing due to reaction torque
  - consequences for steering law???

## Part Rotation

- test performance of inertia estimation

## Process Compensation

- HIL setup (real robot attached to virtual model)