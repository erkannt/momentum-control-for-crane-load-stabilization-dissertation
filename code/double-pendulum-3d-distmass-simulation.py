"""Simulate 3D Distributed Mass Double-Pendulum

Uses better ode solver than the original 2d code its based off.
Dumps results as .npz for visualization in Grasshopper.
"""
import sys
import numpy as np
from math import isclose, sin, cos
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D

# Pendulum rod lengths (m), bob masses (kg).
l1, l2 = 1, 1
m1, m2 = 1, 1
Ixx, Iyy, Izz = 1, 1, 1
# The gravitational acceleration (m.s-2).
g = 9.81
# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax + dt, dt)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0_small = np.array(
    [
        np.pi / 8,  #  theta11
        0,  # dtheta11
        0,  #  theta12
        0,  # dtheta12
        np.pi / 8,  #  theta21
        0,  # dtheta21
        0,  #  theta22
        0,  # dtheta22
        np.pi / 4,  #  theta23
        1,  # dtheta23
    ]
)

# Plot settings
r = 0.05  # bob circle radius
fps = 25
di = int(1 / fps / dt)


def deriv(t, y, l1, l2, m1, m2):
    """Return the first derivatives of y = theta_ij, dtheta_ij"""
    theta11, u11, theta12, u12, theta21, u21, theta22, u22, theta23, u23 = y

    dtheta11 = u11
    dtheta12 = u12
    dtheta21 = u21
    dtheta22 = u22
    dtheta23 = u23
    du11 = 2 * Izz  # see above for full eom
    du12 = 2 * Izz  # see above for full eom
    du21 = -2 * Izz  # see above for full eom
    du22 = -2 * Izz  # see above for full eom
    du23 = 2 * Izz  # see above for full eom

    return [
        dtheta11,
        du11,
        dtheta12,
        du12,
        dtheta21,
        du21,
        dtheta22,
        du22,
        dtheta23,
        du23,
    ]


def plot_motion(t, y, title="", save=False):
    y = np.array(y).T
    theta11 = y[:, 0]
    theta12 = y[:, 2]
    theta21 = y[:, 4]
    theta22 = y[:, 6]

    # Convert to Cartesian coordinates of the two bob positions.
    x1 = l1 * np.sin(theta11)
    y1 = l1 * np.cos(theta11) * np.sin(theta12)
    z1 = -l1 * np.cos(theta11) * np.cos(theta12)
    x2 = x1 + l2 * np.sin(theta21)
    y2 = y1 + l2 * np.cos(theta21) * np.sin(theta22)
    z2 = z1 - l2 * np.cos(theta21) * np.cos(theta22)

    length1 = (isclose(np.linalg.norm([x, y, z]), l1) for x, y, z in zip(x1, y1, z1))
    length2 = (
        isclose(np.linalg.norm([x, y, z]), l2)
        for x, y, z in zip(x2 - x1, y2 - y1, z2 - z1)
    )
    if not (all(length1) and all(length2)):
        print("ERROR: Lengths of links are not maintained!")
        sys.exit()

    # Create animated plot
    fig = plt.figure(figsize=(12, 4))
    pltsize = 1.2 * (l1 + l2)
    axs, lines, trails, circles = [], [], [], []
    for i in range(3):
        ax = fig.add_subplot(
            131 + i,
            autoscale_on=False,
            xlim=(-pltsize, pltsize),
            ylim=(-pltsize, pltsize),
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
        for col, single in zip(
            [axs, lines, trails, circles], [ax, line, trail, [c0, c1, c2]]
        ):
            col.append(single)
    # Time label
    time_template = "time = %.1fs"
    time_text = axs[0].text(0.05, 0.9, "", transform=ax.transAxes)
    plt.tight_layout()

    def animation_init():
        for ax, line, trail, circs in zip(axs, lines, trails, circles):
            line.set_data([], [])
            for c in circs:
                ax.add_patch(c)
            trail.set_data([], [])
            time_text.set_text("")
        return axs + lines + trails + [c for cs in circles for c in cs] + [time_text]

    def animation_func(i):
        front = {"x1": x1, "x2": x2, "y1": z1, "y2": z2}
        right = {"x1": y1, "x2": y2, "y1": z1, "y2": z2}
        top = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
        views = [front, right, top]

        for view, ax, line, trail, circs in zip(views, axs, lines, trails, circles):
            thisx = [0, view["x1"][i], view["x2"][i]]
            thisy = [0, view["y1"][i], view["y2"][i]]
            line.set_data(thisx, thisy)
            circs[1].center = (thisx[1], thisy[1])
            circs[2].center = (thisx[2], thisy[2])
            trail.set_data(view["x2"][1:i], view["y2"][1:i])
        time_text.set_text(time_template % (i * dt))
        return axs + lines + trails + [c for cs in circles for c in cs] + [time_text]

    # blit=True sadly leads to blank animations on saving
    ani = animation.FuncAnimation(
        fig,
        animation_func,
        range(0, len(t), di),
        interval=fps,
        blit=False,
        init_func=animation_init,
    )
    if save:
        ani.save(
            "../output/double_pendulum_3d_distmass_%s.mp4"
            % title.lowercase().replace(" ", "_"),
            animation.writers["ffmpeg"](fps=fps),
            dpi=300,
        )
    plt.show()


def plot_angles(time, y, events):
    fig, axs = plt.subplots(2, 1, sharex=True)
    colors = ["C0", "C1", "C2", "C3"]
    linetypes = ["-", "--", "-.", ":"]
    labels = {
        "3d": [
            r"$\theta_{11}$",
            r"$\theta_{12}$",
            r"$\theta_{21}$",
            r"$\theta_{22}$",
            r"$\theta_{23}$",
        ],
        "3ddot": [
            r"$\dot{\theta}_{11}$",
            r"$\dot{\theta}_{12}$",
            r"$\dot{\theta}_{21}$",
            r"$\dot{\theta}_{22}$",
            r"$\dot{\theta}_{23}$",
        ],
    }

    axs[0].set_title("Upper Link", loc="left")
    axs[1].set_title("Lower Link", loc="left")
    for i, thetaid in zip([0, 1], [0, 1]):
        axs[0].plot(
            time,
            y[thetaid * 2, :] * 180 / np.pi,
            linetypes[i],
            color=colors[i],
            label=labels["3d"][thetaid],
            linewidth="0.85",
        )
    for i, thetaid in zip([0, 1, 2], [2, 3, 4]):
        axs[1].plot(
            time,
            y[thetaid * 2, :] * 180 / np.pi,
            linetypes[i],
            color=colors[i],
            label=labels["3d"][thetaid],
            linewidth="0.85",
        )
    for ax in axs:
        ax.legend(loc=1, framealpha=1)
        ax.grid(axis="y")
    plt.show()


def save2file(y, filename):
    y = np.array(y).T
    theta11 = y[:, 0]
    theta12 = y[:, 2]
    theta21 = y[:, 4]
    theta22 = y[:, 6]
    theta23 = y[:, 8]

    # Convert to Cartesian coordinates of the two bob positions.
    x1 = l1 * np.sin(theta11)
    y1 = l1 * np.cos(theta11) * np.sin(theta12)
    z1 = -l1 * np.cos(theta11) * np.cos(theta12)
    x2 = x1 + l2 * np.sin(theta21)
    y2 = y1 + l2 * np.cos(theta21) * np.sin(theta22)
    z2 = z1 - l2 * np.cos(theta21) * np.cos(theta22)
    points = np.vstack([x1, y1, z1, x2, y2, z2]).T

    # X and Y Vector of distributed mass reference frame
    # (equations generated by cog-rotations.py)
    cogxx = -np.sin(theta21) * np.sin(theta22) * np.sin(theta23) + np.cos(
        theta21
    ) * np.cos(theta23)
    cogxy = np.sin(theta23) * np.cos(theta22)
    cogxz = np.sin(theta21) * np.cos(theta23) + np.sin(theta22) * np.sin(
        theta23
    ) * np.cos(theta21)
    cogyx = -np.sin(theta21) * np.sin(theta22) * np.cos(theta23) - np.sin(
        theta23
    ) * np.cos(theta21)
    cogyy = np.cos(theta22) * np.cos(theta23)
    cogyz = -np.sin(theta21) * np.sin(theta23) + np.sin(theta22) * np.cos(
        theta21
    ) * np.cos(theta23)
    cogvecs = np.vstack([cogxx, cogxy, cogxz, cogyx, cogyy, cogyz]).T

    np.savetxt(filename, np.hstack([points, cogvecs]))


# Small Exitation
save_animations = False
sol = solve_ivp(lambda t, y: deriv(t, y, l1, l2, m1, m2), (0, tmax), y0_small, t_eval=t)
save2file(sol.y, "data4gh")
# plot_angles(t, sol.y, sol.t_events)
# plot_motion(sol.t, sol.y, title="Small Exitation", save=save_animations)
# np.savez('../output/distmass-double-pendulum-small_exitation', t=sol.t, y0=y0_small, y=sol.y)
print("done")
