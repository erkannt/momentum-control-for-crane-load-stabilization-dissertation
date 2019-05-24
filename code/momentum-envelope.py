""" Plot momentum envelope of a 4CMG roof array """

import plotly.offline as py
import plotly.graph_objs as go
from math import cos, sin, pi, sqrt
import numpy as np
import colorlover as cl
from IPython.display import HTML
py.init_notebook_mode()

def unit_sphere(theta1, theta2):
    i = np.array([1, 0, 0])
    j = np.array([0, 1, 0])
    k = np.array([0, 0, 1])
    return np.array(sin(theta2)*i
                    - sin(theta1) * cos(theta2) * j
                    + cos(theta1) * cos(theta2) * k)
#roof_angle = 0.52  #30 degrees
roof_angle = 0.78  #45 degrees

roof4_gimbal_axes = [np.array([0, -cos(roof_angle), sin(roof_angle)]),
                     np.array([0, -cos(roof_angle), sin(roof_angle)]),
                     np.array([0,  cos(roof_angle), sin(roof_angle)]),
                     np.array([0,  cos(roof_angle), sin(roof_angle)])]

epsilon_4H = [1, 1, 1, 1]
epsilon_0H = [1, 1, -1, -1]

def singular_momentum_vector(gimbal_axes, epsilon, theta1, theta2):
    H = np.zeros(3)
    u = unit_sphere(theta1, theta2)
    for i, g in enumerate(gimbal_axes):
        H_i = epsilon[i] * (u - g * np.dot(g, u))
        H_i /= np.linalg.norm(np.cross(g, u))
        H = H + H_i
    return H

res = 150
angles = np.linspace(0, 2*pi, res)

envelope = np.empty([res**2, 3])
inner = np.empty([res**2, 3])

n = 0
for i in angles:
    for j in angles:
        envelope[n] = singular_momentum_vector(roof4_gimbal_axes, epsilon_4H, i, j)
        inner[n] = singular_momentum_vector(roof4_gimbal_axes, epsilon_0H, i, j)
        n = n+1


cl1 = cl.scales['9']['seq']['Greens'][3:]
cl2 = cl.scales['9']['seq']['Oranges'][3:]

cscale1 = [ [ float(i)/float(len(cl1)-1), cl1[i] ]
                for i in range(len(cl1)) ]
cscale2 = [ [ float(i)/float(len(cl2)-1), cl2[i] ]
                for i in range(len(cl2)) ]

envelope4 = go.Scatter3d(
    name = 'Outer Singularities',
    x = envelope[:, 0],
    y = envelope[:, 1],
    z = envelope[:, 2],
    mode = 'markers',
    marker=dict(
        size=2,
        color = envelope[:, 2],
        colorscale = cscale1,
        opacity=0.6
    )
)
inner4 = go.Scatter3d(
    name = 'Inner Singularities',
    x = inner[:, 0],
    y = inner[:, 1],
    z = inner[:, 2],
    mode = 'markers',
    marker=dict(
        size=2,
        color = inner[:, 2],
        colorscale = cscale2,
        opacity=0.6
    )
)
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
data = [envelope4, inner4]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='roof4_envelope')
