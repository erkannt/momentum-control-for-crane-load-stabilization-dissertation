```python
""" EoM of 3D double pendulum with the second mass distributed """
from sympy import symbols, Function, Eq, Matrix
from sympy import sin, cos
from sympy import diff, simplify, expand, solve, factor
from sympy import init_printing, pprint, latex

init_printing()

""" Define Symbols """
l1, l2, m1, m2 = symbols("l1 l2 m1 m2")
Ixx, Iyy, Izz = symbols("Ixx, Iyy, Izz")
t = symbols("t")
g = symbols("g")
L, Pot, Kin = symbols("L Pot Kin")
theta11 = Function("theta11")(t)
theta12 = Function("theta12")(t)
theta21 = Function("theta21")(t)
theta22 = Function("theta22")(t)
theta23 = Function("theta23")(t)
u11, u12, udot11, udot12 = symbols("u11 u12 udot11 udot12")
u21, u22, u23, udot21, udot22, udot23 = symbols("u21 u22 u23 udot21 udot22 udot23")
x1, y1, z1, x2, y2, z2 = symbols("x1 y1 z1 x2 y2 z1")
q = [theta11, theta12, theta21, theta22, theta23]
substitutions = [
    (theta11.diff(t).diff(t), udot11),
    (theta12.diff(t).diff(t), udot12),
    (theta21.diff(t).diff(t), udot21),
    (theta22.diff(t).diff(t), udot22),
    (theta23.diff(t).diff(t), udot23),
    (theta11.diff(t), u11),
    (theta12.diff(t), u12),
    (theta21.diff(t), u21),
    (theta22.diff(t), u22),
    (theta23.diff(t), u23),
]

""" Define Kinematic Relations """
x1 = l1 * sin(theta11)
y1 = l1 * cos(theta11) * sin(theta12)
z1 = -l1 * cos(theta11) * cos(theta12)
x2 = x1 + l2 * sin(theta21)
y2 = y1 + l2 * cos(theta21) * sin(theta22)
z2 = z1 - l2 * cos(theta21) * cos(theta22)

""" Equations for omega from cog-rotations.py """
omega_x = -theta21.diff(t) * (
    -sin(theta21) * sin(theta22) * cos(theta23) - sin(theta23) * cos(theta21)
) + theta22.diff(t) * (
    -sin(theta21) * sin(theta22) * sin(theta23) + cos(theta21) * cos(theta23)
)
omega_y = -theta21.diff(t) * cos(theta22) * cos(theta23) + theta22.diff(t) * sin(
    theta23
) * cos(theta22)
omega_z = (
    -theta21.diff(t)
    * (-sin(theta21) * sin(theta23) + sin(theta22) * cos(theta21) * cos(theta23))
    + theta22.diff(t)
    * (sin(theta21) * cos(theta23) + sin(theta22) * sin(theta23) * cos(theta21))
    + theta23.diff(t)
)

""" Langrangian """
Pot = m1 * g * z1 + m2 * g * z2
Kin = (
    1 / 2 * m1 * (x1.diff(t) ** 2 + y1.diff(t) ** 2 + z1.diff(t) ** 2)
    + 1 / 2 * m2 * (x2.diff(t) ** 2 + y2.diff(t) ** 2 + z2.diff(t) ** 2)
    + 1 / 2 * Ixx * omega_x ** 2
    + 1 / 2 * Iyy * omega_y ** 2
    + 1 / 2 * Izz * omega_z ** 2
)
L = Kin - Pot

euleq = [Eq(0, L.diff(qi.diff(t)).diff(t) - L.diff(qi)) for qi in q]
euleq = [euleqi.subs(substitutions).expand() for euleqi in euleq]

solvedeuleq = solve(
    euleq, [udot11, udot12, udot21, udot22, udot23], simplify=True, rational=False
)

for ddot, eqn in solvedeuleq.items():
    print(ddot, eqn)

```
