
# Outlook and Conclusion

> "Once the conditions for helicopters are in place, it’s helicopter time, and so you get helicopters, everywhere, all at once." -- Cory Doctorow @citation-needed

## Limits of Current Models

- cow is a sphere
  - ropes are flexible
  - no drag
  - no wind
  - forces of robot not taken into account
  - no process forces or torques

## Next Steps for Development

- include external forces in equations of motion
- 3d model that includes CMG array
- translation of CMG state into 3d torque requirement
- implementation of 3d steering law (prereq for controller validation)
- controller for axis alignment in dampening
- integrated simulation loop as prereq to robot path opt

## Other Work Required

- desaturation/CoG compensation with moving weight
- 3d hardware prototype
  - improve realtime capabilities/controller validation workflow
  - improve gyro quality
  - higher torque gimbal motors to ensure sufficient headroom
- optimization of robot paths (look to space work)
- desaturation during dampening
- add crane movement
- collect real crane motion for validation
- power requirements for operation
- construction site suitable hardware design
- sensor(s) and filtering
    - implementation of the inertia estimation
    - dealing with vibrations
- validation of controller under more simulated and hw scenarios
- add controller for robot utilizing compensation

## Conclusion

- sota regarding space and ships
- developed understanding of the problem
- basic toolset for simulation, validation and sizing