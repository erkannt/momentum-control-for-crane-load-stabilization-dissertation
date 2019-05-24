""" Calculate Rotation Matrices for Dist. Mass """
from sympy import symbols, Matrix
from sympy import sin, cos
from sympy import simplify, lambdify
from sympy import init_printing, pprint, latex
from math import pi

init_printing()

""" Define Symbols """
theta21, theta22, theta23 = symbols("theta21 theta22 theta23")
dtheta21, dtheta22, dtheta23 = symbols("dtheta21 dtheta22 dtheta23")
symbolnames = {
    dtheta21: r"\dot{\theta}_{21}",
    dtheta22: r"\dot{\theta}_{22}",
    dtheta23: r"\dot{\theta}_{23}",
}
ix = Matrix([1, 0, 0])
iy = Matrix([0, 1, 0])
iz = Matrix([0, 0, 1])

""" Define Rotation Matrices for each theta, note negative theta21 """
Ry = Matrix(
    [[cos(-theta21), 0, sin(-theta21)], [0, 1, 0], [-sin(-theta21), 0, cos(-theta21)]]
)
Rx = Matrix(
    [[1, 0, 0], [0, cos(theta22), -sin(theta22)], [0, sin(theta22), cos(theta22)]]
)
Rz = Matrix(
    [[cos(theta23), -sin(theta23), 0], [sin(theta23), cos(theta23), 0], [0, 0, 1]]
)

""" Combined forward and inverse Rotation Matrices """
R = Ry * Rx * Rz
Rinv = Rz * Rx * Ry

""" dtheta's as Columnvectors, note negation of dtheta21 """
X = Matrix([dtheta22, 0, 0])
Y = Matrix([0, -dtheta21, 0])
Z = Matrix([0, 0, dtheta23])

""" Output conversion of dthetas and CoG-XY-Vectors """
for expr in [R * X + R * Y + Z, R * ix, R * iy]:
    print(latex(expr, symbol_name=symbolnames))
    print(expr)

""" Sandbox used for validating rotations """
thetas = [5, 3, 2]
negthetas = [t * -1 for t in thetas]
forw = lambdify([theta21, theta22, theta23], R)
back = lambdify([theta21, theta22, theta23], Rinv)
res = forw(*thetas) * ix
# pprint(res)
# pprint(back(*negthetas) * res)

