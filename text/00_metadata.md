---
title: Momentum Control for Crane Load Stabilization
author: Daniel A. Haarhoff
born: Dachau
subtitle: Modeling and Sizing of Control Moment Gyroscopes for Cranes
facultyblurb: Von der Fakultät für Architektur der Rheinisch-Westfälischen Technischen Hochschule Aachen zur Erlangung des akademischen Grades einer Doktorin bzw. eines Doktors der Ingenieurwissenschaften genehmigte Dissertation.
bestanden: true
examdate: 13. Juli 2021
berichter1: Univ.-Prof. Dr. techn. Sigrid Brell-Cokcan
berichter2: Univ.-Prof. Dr.-Ing. Robert Schmitt
abstract: |
  The digitalization of the construction industries planning and execution phases, coupled with advances in automation technology has led to a renaissance for construction robotics.
  Current efforts to provide robots for the execution of digital construction plans revolve around either the adaptation of industrial robots for the construction site, highly specialized custom robots or the digitalization of existing construction equipment.
  However, there is currently no robotics approach that addresses the very large work envelope that constitutes a construction site.

  This work therefore evaluates the feasibility of operating robots and other kinematic systems hanging from a regular crane.
  A crane's hook is not a stable base for a robot.
  Movements of the robot as well as external forces would lead to motions and oscillations.
  The robot would therefore not be able to execute accurate movements.

  Stabilizing a platform at the hook to create a useable base for robots requires adding further means of control to said platform.
  Three approaches are known: additional ropes, propulsive devices and momentum control devices.
  This work studies the use of a specific type of momentum control device, so called control moment gyroscopes.
  These are an established technology for the stabilization of ships and also the reorientation of spacecraft.
  By gimbaling a fast spinning rotor orthogonal to its axis of rotation, CMGs are able to generate torque through the principle of gyroscopic reaction.
  They are thereby able to generate torque in mid-air and unlike additional ropes or propulsive devices do not interfere with their environment.

  The following work develops equations of motion and a model for the crane-CMG-robot system.
  A general control strategy is laid out and a simple PD-based controller is designed.
  The model is validated through a variety of simulations and used to understand the critical interactions between the three systems.
  The ability of a CMG platform to predictively compensate the torques produced by a robot and thereby improve its path accuracy is shown through simulation.
  It is also shown how such a platform can help dampen hook and load oscillations.
  The simulations not only show the potential of the approach, but also allow the work to develop sizing guidelines and identify critical areas for future research.
  The work therefore closes by laying out the critical path to bringing this approach to the construction site.

abstractde: |
  Die Digitalisierung der Planungs- und Ausführungsphasen der Bauindustrie sowie Fortschritte in der Automatisierungstechnik haben zu einer Renaissance der Baurobotik geführt.
  Die aktuellen Bemühungen zur Bereitstellung von Robotern für die Ausführung digitaler Baupläne drehen sich entweder um die Anpassung von Industrierobotern für die Baustelle, hochspezialisierte Sonderroboter oder die Digitalisierung bestehender Baumaschinen.
  Was derzeit fehlt, ist ein Robotikansatz, der den sehr großen Arbeitsraum der Baustelle berücksichtigt.

  Der Haken eines Krans ist keine stabile Basis für einen Roboter.
  Bewegungen des Roboters sowie äußere Kräfte führen zu ungewollten Bewegungen und Oszillationen.
  Der Roboter kann daher keine genauen Bewegungen ausführen.

  Die Stabilisierung einer Plattform am Haken, um eine brauchbare Basis für Roboter zu schaffen, erfordert das Hinzufügen weiterer Kontrollmöglichkeiten zu dieser Plattform.
  Drei Ansätze sind bekannt: zusätzliche Seile, Propellervorrichtungen und Vorrichtungen zur Momentensteuerung.  In dieser Arbeit wird die Verwendung eines bestimmten Typs von Momentensteuergeräten, so genannter Kontrolmomentgyroskope, untersucht.
  Diese sind eine etablierte Technologie für die Stabilisierung von Schiffen und die Orientierung von Raumfahrzeugen.
  Durch die Verkippung eines sich schnell drehenden Rotors orthogonal zu seiner Drehachse sind CMGs in der Lage, durch das Prinzip der gyroskopischen Reaktion Drehmoment zu erzeugen.
  Dadurch können sie Drehmomente erzeugen ohne sich abstoßen zu müssen und im Gegensatz zu zusaetzlichen Seilen oder Propellern beinflussen sie nicht ihre Umgebung.

  Die folgende Arbeit entwickelt Bewegungsgleichungen und ein Modell für das Kran-CMG-Roboter-System.
  Durch eine Reihe von Simulationen wird dieses Modell validiert und verwendet, um die kritischen Wechselwirkungen zwischen den drei Systemen zu verstehen.
  Die Fähigkeit einer CMG-Plattform, die von einem Roboter erzeugten Drehmomente prädiktiv zu kompensieren und dadurch die Bahngenauigkeit zu verbessern, wird mittels einer Simulation gezeigt.
  Es wird zudem gezeigt, wie eine solche Plattform dazu beitragen kann, sowohl Haken- als auch Lastschwingungen zu dämpfen.
  Die Simulationen zeigen nicht nur das Potenzial des Ansatzes, sondern ermöglichen es auch, Dimensionierungsrichtlinien zu entwickeln und kritische Bereiche für die zukünftige Forschung zu identifizieren.
  Die Arbeit schließt daher mit der Ausarbeitung eines kritischen Pfades, um diesen Ansatz auf die Baustelle zu bringen.
bibliography: [./bibliography.yaml]
link-citations: true
linkReferences: true
documentclass: scrbook
fontsize: 11pt
papersize: a4
classoption:
- twoside
- openright
- toc=flat
---