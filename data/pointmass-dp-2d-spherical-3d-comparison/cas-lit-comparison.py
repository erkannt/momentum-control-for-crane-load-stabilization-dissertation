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


def cas_lit_comp():
  """ CAS Lit Comparison """
  fig, axs = plt.subplots(3, 1, sharex=True)
  fig.suptitle('Equations of Motion from Computer Algebra System and Literature')
  time = data['2d-large']['t']

  # CAS
  ax = axs[0]
  for i in range(4):
    ax.plot(time, data['2d-large']['y'][:,i] * 180/pi,
      linetypes[i],
      color=colors[i],
      label=labels['2d'][i],
      linewidth='0.85')
  ax.set_title("EoM from CAS", loc='left')

  # Lit
  ax = axs[1]
  for i in range(4):
    ax.plot(time, data['2d-large-lit']['y'][:,i] * 180/pi,
      linetypes[i],
      color=colors[i],
      label=labels['2d'][i],
      linewidth='0.85')
  ax.set_title("EoM from Literature", loc='left')

  # Diff
  ax = axs[2]
  for i in range(4):
    ax.plot(time, (data['2d-large-lit']['y'][:,i] - data['2d-large']['y'][:,i])* 180/pi,
      linetypes[i],
      color=colors[i],
      label=labels['2d'][i],
      linewidth='0.85')
  ax.set_title("Difference", loc='left')
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

cas_lit_comp()
