```python
from sympy import symbols, Function, Eq
from sympy import sin, cos
from sympy import diff, simplify, expand, solve
from sympy import init_printing, pprint, latex

init_printing()

""" Define Symbols """
l1, l2, m1, m2, I2 = symbols("l1 l2 m1 m2 I2")
t = symbols("t")
g = symbols("g")
L, Pot, Kin = symbols("L Pot Kin")
testPot, testKin = symbols("testPot testKin")
theta1 = Function("theta1")(t)
theta2 = Function("theta2")(t)
z1, z2, zdot1, zdot2 = symbols("z1 z2 zdot1 zdot2")
x1, y1, x2, y2 = symbols("x1 y1 x2 y2")
q = [theta1, theta2]
substitutions = [
    (theta1.diff(t).diff(t), zdot1),
    (theta2.diff(t).diff(t), zdot2),
    (theta1.diff(t), z1),
    (theta2.diff(t), z2),
]

""" Define Kinematic Relations """
x1 = l1 * sin(theta1)
y1 = -l1 * cos(theta1)
x2 = l1 * sin(theta1) + l2 * sin(theta2)
y2 = -l1 * cos(theta1) - l2 * cos(theta2)

""" Langrangian """
Pot = m1 * g * y1 + m2 * g * y2
Kin = (
    1 / 2 * m1 * (x1.diff(t) ** 2 + y1.diff(t) ** 2)
    + 1 / 2 * m2 * (x2.diff(t) ** 2 + y2.diff(t) ** 2)
    + 1 / 2 * (I2) * theta2.diff(t) ** 2
)
L = Kin - Pot

euleq = [Eq(0, L.diff(qi.diff(t)).diff(t) - L.diff(qi)).simplify() for qi in q]
euleq = [euleqi.subs(substitutions) for euleqi in euleq]

solvedeuleq = solve(euleq, [zdot1, zdot2], simplify=False, rational=False)

for ddot, eqn in solvedeuleq.items():
    print(ddot, eqn.simplify())

```
