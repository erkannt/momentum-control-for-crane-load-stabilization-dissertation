import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from math import pi
import os, sys

workdir, _ = os.path.split(os.path.abspath(__file__))
output = os.path.abspath(sys.argv[1])
os.chdir(workdir)

plt.rc('text', usetex=True)
rcParams['text.latex.preamble'] = [
  r'\usepackage{tgheros}',    # helvetica font
  r'\usepackage{sansmath}',   # math-font matching  helvetica
  r'\sansmath'                # actually tell tex to use it!
  r'\usepackage{siunitx}',    # micro symbols
  r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  
rcParams['figure.figsize'] = 9,5
sns.set()
sns.set_style("ticks")
sns.set_context("paper")

colors = ['C0', 'C1', 'C2', 'C3']
linetypes = ['-', '--', '-.', ':']


datafiles = {
  '2d-large': "pointmass-double-pendulum-large_exitation-2d.npz",
  '2d-large-lit': "pointmass-double-pendulum-large_exitation-2d-literature_eom.npz",
  '2d-small': "pointmass-double-pendulum-small_exitation-2d.npz",
  '3d-large': "pointmass-double-pendulum-large_exitation-3d.npz",
  '3d-small': "pointmass-double-pendulum-small_exitation-3d.npz"}

data = {name:np.load(file) for name, file in datafiles.items()}
labels = {
  '2d': [r'$\theta_{1}$', r'$\dot{\theta}_{1}$', r'$\theta_{2}$', r'$\dot{\theta}_{2}$'],
  '3d': [r'$\theta_{11}$', r'$\theta_{12}$', r'$\theta_{21}$', r'$\theta_{22}$'],
  '3ddot': [r'$\dot{\theta}_{11}$', r'$\dot{\theta}_{12}$', r'$\dot{\theta}_{21}$', r'$\dot{\theta}_{22}$'],
  '2d3d': [r'$\theta_{1}-\theta_{11}$', r'$\theta_{2}-\theta_{21}$']}

def angle_issues():
  """ Illustrate Issue of Angle Wrap Around """
  fig, axs = plt.subplots(3, 1, sharex=True)
  fig.suptitle('Issues with Use of Spherical Coordinate Description of Rotations')
  time = data['3d-small']['t']

  axs[0].set_title("Polar Angles", loc='left')
  axs[1].set_title("Azimuthal Angles", loc='left')
  axs[2].set_title("Angular Velocities", loc='left')
  for i in range(0,8,4):
    polar = data['3d-small']['y'][i,:]
    azimuth = data['3d-small']['y'][i+2,:]
    axs[0].plot(time, polar * 180/pi,
      linetypes[i//2],
      color=colors[i//2],
      label=labels['3d'][i//2],
      linewidth='0.85')
    axs[1].plot(time, azimuth * 180/pi,
      linetypes[i//2+1],
      color=colors[i//2+1],
      label=labels['3d'][i//2+1],
      linewidth='0.85')
  for i, j in zip(range(1,8,2), range(4)):
    axs[2].semilogy(time, data['3d-small']['y'][i,:] * 180/pi,
      linetypes[j],
      color=colors[j],
      label=labels['3ddot'][j],
      linewidth='0.85')
  axs[2].set_ylim((10e-3,1000000))

  for ax in axs:
    ax.legend(loc=1, framealpha=1)
    ax.grid(axis='y')
  sns.despine(trim=True, offset=2)
  for ax in axs[0:-1]:
    ax.get_xaxis().set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.xlabel('Time [s]')
    plt.tight_layout()
  fig.subplots_adjust(hspace=0.6)
  plt.savefig(output)

angle_issues()
