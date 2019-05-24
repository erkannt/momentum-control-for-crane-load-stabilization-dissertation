"""Distributed Mass Double-Pendulum with PDalpha Controller
"""
import os
import sys
from math import pi, sin, cos
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

""" Simulation Setup """
lab_setup = [5, 1, 1, 10, 1 / 2 * 10 * 0.4 ** 2 + 10 * 1 ** 2]  # l1, l2  # m1, m2  # I2
l1_24 = [19, 2 * 2, 50, 2500, 16484]  # l1, l2  # m1, m2  # I2
ecb380 = [83, 3.7 * 2, 300, 15660, 350877]  # l1, l2  # m1, m2  # I2
load_dims = [(0.4, 0.4), (5.1, 2.0), (9.3, 3.7)]
# PDalpha Controller Values
kp, kd, kalpha = 1.0, 4.0, 0.5
# The gravitational acceleration (m.s-2).
GRAVITY = 9.81
# Maximum time, time point spacings and the time grid (all in s).
TMAX, DT = 25, 0.01
TIMESTEPS = np.arange(0, TMAX + DT, DT)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0_small = np.array(
    [np.pi / 18, 0, np.pi / 18, 0, 0]  # theta1  # dtheta1  # theta2  # dtheta2  # tau
)

""" Use passed args as savepath, otherwise only show plots """
workdir, _ = os.path.split(os.path.abspath(__file__))
if len(sys.argv) == 1:
    output = False
else:
    output = os.path.abspath(sys.argv[1])
os.chdir(workdir)


def deriv(t, y, l1, l2, m1, m2, I2, kp, kd, kalpha):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    kp *= I2
    kd *= I2
    theta1, z1, theta2, z2, tauprev = y
    error = (0 - theta2) + (0 - theta1) * kalpha
    errordot = (0 - z2) + (0 - z1) * kalpha
    tau = kp * error + kd * errordot
    taudot = (tau - tauprev) / DT

    theta1dot = z1
    theta2dot = z2
    z1dot = (
        1.0
        * (
            -l2 ** 2
            * m2 ** 2
            * (GRAVITY * sin(theta2) - l1 * z1 ** 2 * sin(theta1 - theta2))
            * cos(theta1 - theta2)
            + (I2 + l2 ** 2 * m2)
            * (
                GRAVITY * m1 * sin(theta1)
                + GRAVITY * m2 * sin(theta1)
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
            (m1 + m2) * (GRAVITY * sin(theta2) - l1 * z1 ** 2 * sin(theta1 - theta2))
            - (
                GRAVITY * m1 * sin(theta1)
                + GRAVITY * m2 * sin(theta1)
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


def animated_pendulum(data, params, dims, title="", save=False, show=True):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.patches import Circle

    # Unpack data and params
    t = data["t"]
    theta1 = data["theta1"]
    theta2 = data["theta2"]
    l1, l2 = params[0:2]
    w, h = dims

    # Plot settings
    r = 0.1 * l2  # bob circle radius
    fps = 25
    di = int(1 / fps / DT)

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

    def load_vertices(x, y, theta):
        vx0 = np.array([-w, +w, +w, -w, -w])
        vy0 = np.array([-h, -h, +h, +h, -h])
        vx = vx0 * cos(theta) - vy0 * sin(theta)
        vy = vx0 * sin(theta) + vy0 * cos(theta)
        return vx + x, vy + y

    # Trail
    trail, = ax.plot(
        [], [], c="r", solid_capstyle="butt", lw=2, alpha=0.4, linestyle=":"
    )
    # The pendulum rods.
    line, = ax.plot([], [], c="k", lw=1.5)
    # Circles representing the anchor point of rod 1, and bobs 1 and 2.
    c0 = Circle((0, 0), r / 2, fc="k", zorder=10)
    c1 = Circle((0, 0), r, fc="b", ec="b", zorder=10)
    c2 = Circle((0, 0), r, fc="r", ec="r", zorder=10)
    # Box representing the load
    load, = ax.plot([], [], c="r", lw=2)
    # Scale Bar
    ax.plot([-pltsize * 0.2, -pltsize * 0.2], [0, -5], c="gray", lw=5)
    ax.text(-pltsize * 0.2 + pltsize * 0.01, -5, "3m")
    # Time label
    time_template = "time = %.1fs"
    time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)

    def animation_init():
        line.set_data([], [])
        ax.add_patch(c0)
        ax.add_patch(c1)
        ax.add_patch(c2)
        trail.set_data([], [])
        load.set_data([], [])
        time_text.set_text("")
        return line, time_text, c0, c1, c2, load

    def animation_func(i):
        thisx = [0, x1[i], x2[i]]
        thisy = [0, y1[i], y2[i]]
        thistheta = theta2[i]
        vx, vy = load_vertices(x2[i], y2[i], thistheta)

        line.set_data(thisx, thisy)
        c1.center = (thisx[1], thisy[1])
        c2.center = (thisx[2], thisy[2])
        load.set_data(vx, vy)
        trail.set_data(x2[1:i], y2[1:i])
        time_text.set_text(time_template % (i * DT))
        return line, time_text, c1, c2, trail, load

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
    if show:
        plt.show()


def solve(init_cond, params):
    sol = solve_ivp(
        lambda t, y: deriv(t, y, *params), (0, TMAX), init_cond, t_eval=TIMESTEPS
    )
    data = {
        "t": sol.t,
        "theta1": sol.y[0, :],
        "theta2": sol.y[2, :],
        "dtheta1": sol.y[1, :],
        "dtheta2": sol.y[3, :],
        "tau": sol.y[4, :],
    }
    return data


def plot_pos_vel(data, ax, title=""):
    colors = ["C0", "C1", "C2", "C3"]
    linetypes = ["-", "--", "-.", ":"]
    labels2d = [
        r"$\theta_{1} [^\circ]$",
        r"$\dot{\theta}_{1} [\frac{rad}{s}]$",
        r"$\theta_{2} [^\circ]$",
        r"$\dot{\theta}_{2} [\frac{rad}{s}]$",
    ]
    varnames = ["theta1", "dtheta1", "theta2", "dtheta2"]
    for i, vn in enumerate(varnames):
        ax.plot(
            data["t"],
            data[vn] * 180 / pi,
            linetypes[i],
            color=colors[i],
            label=labels2d[i],
            linewidth="0.85",
        )
    if title:
        ax.set_title(title, loc="left")


def plot_torque(data, ax, title=""):
    ax.plot(data["t"], data["tau"], label=r"$\tau [Nm]$", linewidth="1.0")
    if title:
        ax.set_title(title, loc="left")


def output_figure(fig, axs, output):
    for ax in axs:
        ax.grid(axis="y")
    axs[0].legend(loc=1, framealpha=1)
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


""" Run Simulations """
saveanim = True
showanim = not saveanim
cranes = [lab_setup, l1_24, ecb380]
crane_names = [
    "Lab Setup (5m, 10kg)",
    "L1-24 (19m, 2400kg)",
    "380EC-B16 (83m, 15660kg)",
]
crane_sol = []
for c, name, dims in zip(cranes, crane_names, load_dims):
    params = (*c, kp, kd, kalpha)
    sol = solve(y0_small, params)
    crane_sol.append(sol)

    # Create animation when run without args
    # Run before switching on seaborn to avoid slow animation
    if not output:
        animated_pendulum(sol, params, dims, title=name, save=saveanim, show=showanim)

""" Set up Seaborn Plots """
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

""" Make Plots """
fig, axs = plt.subplots(3, 1, sharex=True)
fig.suptitle("Dampening of Selected Cranes")
for sol, name, ax in zip(crane_sol, crane_names, axs):
    plot_pos_vel(sol, ax, title=name)
output_figure(fig, axs, output)
