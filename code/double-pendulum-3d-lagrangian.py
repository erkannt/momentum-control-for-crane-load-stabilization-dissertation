```python
from sympy import symbols, Function, Eq
from sympy import sin, cos
from sympy import diff, simplify, expand, solve
from sympy import init_printing, pprint, latex
init_printing()

""" Define Symbols """
l1, l2, m1, m2 = symbols('l1 l2 m1 m2')
t = symbols('t')
g = symbols('g')
L, Pot, Kin = symbols('L Pot Kin')
theta11 = Function('theta11')(t)
theta12 = Function('theta12')(t)
theta21 = Function('theta21')(t)
theta22 = Function('theta22')(t)
u11, u12, udot11, udot12 = symbols('u11 u12 udot11 udot12')
u21, u22, udot21, udot22 = symbols('u21 u22 udot21 udot22')
x1, y1, z1, x2, y2, z2 = symbols('x1 y1 z1 x2 y2 z1')
q = [theta11, theta12, theta21, theta22]
substitutions = [(theta11.diff(t).diff(t), udot11),
                 (theta12.diff(t).diff(t), udot12),
                 (theta21.diff(t).diff(t), udot21),
                 (theta22.diff(t).diff(t), udot22),
                 (theta11.diff(t), u11),
                 (theta12.diff(t), u12),
                 (theta21.diff(t), u21),
                 (theta22.diff(t), u22),
                ]

""" Define Kinematic Relations """
x1 = l1 * sin(theta11) * cos(theta12)
y1 = l1 * sin(theta11) * sin(theta12)
z1 = -l1 * cos(theta11)
x2 = x1 + l2 * sin(theta21) * cos(theta22)
y2 = y1 + l2 * sin(theta21) * sin(theta22)
z2 = z1 - l2 * cos(theta21)

""" Langrangian """
Pot = m1 * g * z1 + m2 * g * z2
Kin = ( 1/2 * m1 * (x1.diff(t)**2 + y1.diff(t)**2 + z1.diff(t)**2)
      + 1/2 * m2 * (x2.diff(t)**2 + y2.diff(t)**2 + z2.diff(t)**2))
L = Kin - Pot

euleq = [Eq(0, L.diff(qi.diff(t)).diff(t) - L.diff(qi)).simplify() for qi in q]
euleq = [euleqi.subs(substitutions) for euleqi in euleq]

solvedeuleq = solve(euleq, [udot11, udot12, udot21, udot22], simplify=False, rational=False)

for ddot, eqn in solvedeuleq.items():
  print(ddot, eqn.simplify())
```