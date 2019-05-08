"""Distributed Mass Double-Pendulum with PDalpha Controller
"""
import numpy as np
from math import isclose, sin, cos
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.animation as animation
from matplotlib.patches import Circle
import seaborn as sns
from math import pi
import os, sys

""" Simulation Setup """
# Pendulum rod lengths (m), bob masses (kg).
l1, l2 = 5, 1
m1 = 1
m2 = 10
r2 = 0.3 * l2
# PDalpha Controller Values
kp, kd, kalpha = 1.0, 4.0, 0.5
# The gravitational acceleration (m.s-2).
g = 9.81
# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax + dt, dt)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0_small = np.array([np.pi/8,  #  theta1
                     0,        # dtheta1
                     np.pi/8,  #  theta2
                     0,        # dtheta2
                     0         #  tau
                     ])

""" Plot Stuff """
# Plot settings
r = 0.1  # bob circle radius
fps = 25
di = int(1 / fps / dt)

workdir, _ = os.path.split(os.path.abspath(__file__))
if len(sys.argv) == 1:
    output = False
else:
    output = os.path.abspath(sys.argv[1])
os.chdir(workdir)

colors = ["C0", "C1", "C2", "C3"]
linetypes = ["-", "--", "-.", ":"]

labels2d = [
    r"$\theta_{1} [^\circ]$",
    r"$\dot{\theta}_{1} [\frac{rad}{s}]$",
    r"$\theta_{2} [^\circ]$",
    r"$\dot{\theta}_{2} [\frac{rad}{s}]$",
]



def deriv(t, y, l1, l2, m1, m2, I2, kp, kd, kalpha):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2, tauprev = y
    error = (0 - theta2) + (0 - theta1) * kalpha
    errordot = (0 - z2) + (0 - z1) * kalpha
    tau = kp * error + kd * errordot
    taudot = (tau - tauprev) / dt

    theta1dot = z1
    theta2dot = z2
    z1dot = (
        1.0
        * (
            -l2 ** 2
            * m2 ** 2
            * (g * sin(theta2) - l1 * z1 ** 2 * sin(theta1 - theta2))
            * cos(theta1 - theta2)
            + (I2 + l2 ** 2 * m2)
            * (
                g * m1 * sin(theta1)
                + g * m2 * sin(theta1)
                + l2 * m2 * z2 ** 2 * sin(theta1 - theta2)
            )
        )
        / (
            l1
            * (
                l2 ** 2 * m2 ** 2 * cos(theta1 - theta2) ** 2
                - (I2 + l2 ** 2 * m2) * (m1 + m2)
            )
        )
    )
    z2dot = (
        1.0
        * l2
        * m2
        * (
            (m1 + m2) * (g * sin(theta2) - l1 * z1 ** 2 * sin(theta1 - theta2))
            - (
                g * m1 * sin(theta1)
                + g * m2 * sin(theta1)
                + l2 * m2 * z2 ** 2 * sin(theta1 - theta2)
            )
            * cos(theta1 - theta2)
        )
        / (
            l2 ** 2 * m2 ** 2 * cos(theta1 - theta2) ** 2
            - (I2 + l2 ** 2 * m2) * (m1 + m2)
        )
    )
    z2dot += tau / I2
    return theta1dot, z1dot, theta2dot, z2dot, taudot


def slugify(value):
    import re

    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value


def plot_motion(t, y, title="", save=False):
    # Unpack z and theta as a function of time
    theta1, theta2 = y[0, :], y[2, :]

    # Convert to Cartesian coordinates of the two bob positions.
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)

    # Create animated plot
    fig = plt.figure()
    plt.title(title)
    pltsize = 1.2 * (l1 + l2)
    ax = fig.add_subplot(
        111,
        autoscale_on=False,
        ylim=(-pltsize, 0.05 * pltsize),
        xlim=(-pltsize * 0.5, pltsize * 0.5),
    )

    # Trail
    trail, = ax.plot(
        [], [], c="r", solid_capstyle="butt", lw=2, alpha=0.4, linestyle=":"
    )
    # The pendulum rods.
    line, = ax.plot([], [], c="k", lw=2)
    # Circles representing the anchor point of rod 1, and bobs 1 and 2.
    c0 = Circle((0, 0), r / 2, fc="k", zorder=10)
    c1 = Circle((0, 0), r, fc="b", ec="b", zorder=10)
    c2 = Circle((0, 0), r, fc="r", ec="r", zorder=10)
    # Time label
    time_template = "time = %.1fs"
    time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)

    def animation_init():
        line.set_data([], [])
        ax.add_patch(c0)
        ax.add_patch(c1)
        ax.add_patch(c2)
        trail.set_data([], [])
        time_text.set_text("")
        return line, time_text, c0, c1, c2

    def animation_func(i):
        thisx = [0, x1[i], x2[i]]
        thisy = [0, y1[i], y2[i]]

        line.set_data(thisx, thisy)
        c1.center = (thisx[1], thisy[1])
        c2.center = (thisx[2], thisy[2])
        trail.set_data(x2[1:i], y2[1:i])
        time_text.set_text(time_template % (i * dt))
        return line, time_text, c1, c2, trail

    ani = animation.FuncAnimation(
        fig,
        animation_func,
        range(0, t.size, di),
        interval=fps,
        blit=True,
        init_func=animation_init,
    )

    plt.axis("off")
    # Later ffmpeg crop=1246:646:352:560 to limit to actual motion
    if save:
        ani.save(
            "%s.mp4" % slugify(title), animation.writers["ffmpeg"](fps=fps), dpi=300
        )
    plt.show()


def plot_comp(data, time, suptitle):
    fig, axs = plt.subplots(2, 1, sharex=True)
    fig.suptitle(suptitle)

    ax = axs[0]
    ax.plot(
        time, data[4, :], linetypes[0], color="gray", label=r"$\tau$", linewidth="1.0"
    )
    for i in range(4):
        ax.plot(
            time,
            data[i, :] * 180 / pi,
            linetypes[i],
            color=colors[i],
            label=labels2d[i],
            linewidth="0.85",
        )

    for ax in axs:
        ax.legend(loc=1, framealpha=1)
        ax.grid(axis="y")
    sns.despine(trim=True, offset=2)
    for ax in axs[0:-1]:
        ax.get_xaxis().set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.xlabel("Time [s]")
        plt.tight_layout()
    # fig.subplots_adjust(hspace=0.6)
    plt.tight_layout()
    if output:
        plt.savefig(output)
    else:
        plt.show()


I2 = 1 / 2 * m2 * r2 ** 2 + m2 * l2 ** 2
sol = solve_ivp(
    lambda t, y: deriv(t, y, l1, l2, m1, m2, I2, kp * I2, kd * I2, kalpha),
    (0, tmax),
    y0_small,
    t_eval=t,
)

if not output:
    save_animations = False
    plot_motion(
        t, sol.y, title="Point Mass (no rotational inertia)", save=save_animations
    )
    # plot_motion(t, data[1], title="Point Mass (upper), Distributed Mass (lower)", save=save_animations)
    # plot_motion(t, data[2], title="inertia-10", save=save_animations)
    # plot_motion(t, data[3], title="inertia-100", save=save_animations)

plt.rc("text", usetex=True)
rcParams["text.latex.preamble"] = [
    r"\usepackage{tgheros}",  # helvetica font
    r"\usepackage{sansmath}",  # math-font matching  helvetica
    r"\sansmath"  # actually tell tex to use it!
    r"\usepackage{siunitx}",  # micro symbols
    r"\sisetup{detect-all}",  # force siunitx to use the fonts
]
rcParams["figure.figsize"] = 9, 4
sns.set()
sns.set_style("ticks")
sns.set_context("paper")

plot_comp(sol.y, t, "Double Pendulum with different Inertias")