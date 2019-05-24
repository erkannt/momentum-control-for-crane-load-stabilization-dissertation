"""Simulate Double-Pendulum Motion

Original code by Christian Hill, taken from his website scipython.com.
"""
import sys
import numpy as np
from math import sin, cos
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Pendulum rod lengths (m), bob masses (kg).
l1, l2 = 1, 1
m1, m2 = 1, 1
# The gravitational acceleration (m.s-2).
g = 9.81
# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax + dt, dt)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0 = np.array([3 * np.pi / 7, 0, 3 * np.pi / 4, 0])
y0_small = np.array([np.pi / 8, 0, np.pi / 8, 0])

# Plot settings
r = 0.05  # bob circle radius
fps = 25
di = int(1 / fps / dt)


def deriv(y, t, l1, l2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y

    c, s = cos(theta1 - theta2), sin(theta1 - theta2)

    theta1dot = z1
    z1dot = (
        (
            m2 * g * sin(theta2) * c
            - m2 * s * (l1 * z1 ** 2 * c + l2 * z2 ** 2)
            - (m1 + m2) * g * sin(theta1)
        )
        / l1
        / (m1 + m2 * s ** 2)
    )
    theta2dot = z2
    z2dot = (
        (
            (m1 + m2) * (l1 * z1 ** 2 * s - g * sin(theta2) + g * sin(theta1) * c)
            + m2 * l2 * z2 ** 2 * s * c
        )
        / l2
        / (m1 + m2 * s ** 2)
    )
    return theta1dot, z1dot, theta2dot, z2dot


def deriv_cas(y, t, l1, l2, m1, m2):
    """Return first deriv. using equations of motion calculated using CAS """
    theta1, z1, theta2, z2 = y

    c, s = cos(theta1 - theta2), sin(theta1 - theta2)

    theta1dot = z1
    theta2dot = z2
    z1dot = -(
        g * m1 * sin(theta1)
        + g * m2 * sin(theta1 - 2 * theta2) / 2
        + g * m2 * sin(theta1) / 2
        + l1 * m2 * z1 ** 2 * sin(2 * theta1 - 2 * theta2) / 2
        + l2 * m2 * z2 ** 2 * sin(theta1 - theta2)
    ) / (l1 * (m1 - m2 * cos(theta1 - theta2) ** 2 + m2))
    z2dot = (
        g * m1 * sin(2 * theta1 - theta2) / 2
        - g * m1 * sin(theta2) / 2
        + g * m2 * sin(2 * theta1 - theta2) / 2
        - g * m2 * sin(theta2) / 2
        + l1 * m1 * z1 ** 2 * sin(theta1 - theta2)
        + l1 * m2 * z1 ** 2 * sin(theta1 - theta2)
        + l2 * m2 * z2 ** 2 * sin(2 * theta1 - 2 * theta2) / 2
    ) / (l2 * (m1 - m2 * cos(theta1 - theta2) ** 2 + m2))
    return theta1dot, z1dot, theta2dot, z2dot


def calc_E(y):
    """Return the total energy of the system."""

    th1, th1d, th2, th2d = y.T
    V = -(m1 + m2) * l1 * g * np.cos(th1) - m2 * l2 * g * np.cos(th2)
    T = 0.5 * m1 * (l1 * th1d) ** 2 + 0.5 * m2 * (
        (l1 * th1d) ** 2
        + (l2 * th2d) ** 2
        + 2 * l1 * l2 * th1d * th2d * np.cos(th1 - th2)
    )
    return T + V


def plot_motion(t, y, title="", save=False):
    # Unpack z and theta as a function of time
    theta1, theta2 = y[:, 0], y[:, 2]

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
        111, autoscale_on=False, xlim=(-pltsize, pltsize), ylim=(-pltsize, pltsize)
    )
    plt.axis("off")

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

    # Later ffmpeg crop=1246:646:352:560 to limit to actual motion
    if save:
        ani.save(
            "../output/double_pendulum_2d_%s.mp4" % title,
            animation.writers["ffmpeg"](fps=fps),
            dpi=300,
        )

    plt.show()


def plot_comparison(t, y, y_cas):
    plt.figure()
    plt.subplot(321)
    plt.plot(t, y[:, 0])
    plt.title("theta1 lit")
    plt.subplot(322)
    plt.plot(t, y[:, 2])
    plt.title("theta2 lit")
    plt.subplot(323)
    plt.plot(t, y_cas[:, 0])
    plt.title("theta1 cas")
    plt.subplot(324)
    plt.plot(t, y_cas[:, 2])
    plt.title("theta2 cas")
    plt.subplot(325)
    plt.plot(t, y_cas[:, 0] - y[:, 0])
    plt.title("theta1 diff")
    plt.subplot(326)
    plt.plot(t, y_cas[:, 2] - y[:, 2])
    plt.title("theta2 diff")
    plt.tight_layout()
    plt.show()


def check_energy_conservation(y, y0):
    # Check that the calculation conserves total energy to within some tolerance.
    EDRIFT = 0.05
    # Total energy from the initial conditions
    E = calc_E(y0)
    if np.max(np.sum(np.abs(calc_E(y) - E))) > EDRIFT:
        sys.exit("Maximum energy drift of {} exceeded.".format(EDRIFT))


# Do the numerical integration of the equations of motion
y = odeint(deriv, y0, t, args=(l1, l2, m1, m2))
y_cas = odeint(deriv_cas, y0, t, args=(l1, l2, m1, m2))
y_cas_small = odeint(deriv_cas, y0_small, t, args=(l1, l2, m1, m2))

check_energy_conservation(y, y0)
check_energy_conservation(y_cas, y0)

plot_motion(t, y_cas, title="Large Exitation", save=True)
plot_motion(t, y_cas_small, title="Small Exitation", save=True)
plot_comparison(t, y, y_cas)

np.savez(
    "../output/pointmass-double-pendulum-large_exitation-2d-literature_eom",
    t=t,
    y0=y0,
    y=y,
)
np.savez("../output/pointmass-double-pendulum-large_exitation-2d", t=t, y0=y0, y=y_cas)
np.savez(
    "../output/pointmass-double-pendulum-small_exitation-2d",
    t=t,
    y0=y0_small,
    y=y_cas_small,
)

