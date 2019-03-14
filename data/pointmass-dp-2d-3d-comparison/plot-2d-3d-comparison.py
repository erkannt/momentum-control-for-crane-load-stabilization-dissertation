import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from math import pi
import os

workdir, _ = os.path.split(os.path.abspath(__file__))
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
outputtypes = ['pdf', 'svg', 'png']
outputfolder = "../../figures/"

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
    ax.plot(time, (data['2d-large-lit']['y'][:,i] - data['2d-large-lit']['y'][:,i])* 180/pi,
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
  for ftype in outputtypes:
    plt.savefig('%s/cas-lit-comparison.%s' % (outputfolder, ftype))

def comp_large_exitation():
  """ 2D-3D Comparison Large Exitation """
  fig, axs = plt.subplots(3, 1, sharex=True)
  fig.suptitle('Comparison of 2D- and 3D-Pendulum (Large Exitation)')
  time = data['2d-large']['t']

  # 2D
  ax = axs[0]
  for i in range(0,4,2):
    ax.plot(time, data['2d-large']['y'][:,i] * 180/pi,
      linetypes[i],
      color=colors[i],
      label=labels['2d'][i],
      linewidth='0.85')
  ax.set_title("2D Model", loc='left')

  # 3D
  ax = axs[1]
  for i in range(4):
    ax.plot(time, data['3d-large']['y'][i*2,:] * 180/pi,
      linetypes[i],
      color=colors[i],
      label=labels['3d'][i],
      linewidth='0.85')
  ax.set_title("3D Model", loc='left')

  # Diff
  ax = axs[2]
  for i in range(2):
    ax.plot(time, (data['2d-large']['y'][:,i*2] - data['3d-large']['y'][i*4,:])* 180/pi,
      linetypes[i*2],
      color=colors[i*2],
      label=labels['2d3d'][i],
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
  for ftype in outputtypes:
    plt.savefig('%s/2d-3d-comparison-large-exitation.%s' % (outputfolder, ftype))

def comp_small_exitation():
  """ 2D-3D Comparison Small Exitation """
  fig, axs = plt.subplots(3, 1, sharex=True)
  fig.suptitle('Comparison of 2D- and 3D-Pendulum (Small Exitation)')
  time = data['2d-small']['t']

  axs[0].set_title("2D Model", loc='left')
  axs[1].set_title("3D Model", loc='left')
  axs[2].set_title("Difference", loc='left')
  for i in range(0,8,4):
    angles2d = (data['2d-small']['y'][:,i//2] + pi) % (2 * pi ) - pi
    polar = (data['3d-small']['y'][i,:] + pi) % (2 * pi ) - pi
    azimuth = (data['3d-small']['y'][i+2,:] + pi) % (2 * pi ) - pi
    polar[np.abs(azimuth) > pi/10] *= -1
    axs[0].plot(time, angles2d * 180/pi,
      linetypes[i//2],
      color=colors[i//2],
      label=labels['2d'][i//2],
      linewidth='0.85')
    axs[1].plot(time, polar * 180/pi,
      linetypes[i//2],
      color=colors[i//2],
      label=labels['3d'][i//2],
      linewidth='0.85')
    axs[2].plot(time, (angles2d - polar) * 180/pi,
      linetypes[i//2],
      color=colors[i//2],
      label=labels['2d3d'][i//4],
      linewidth='0.85')

  for ax in axs:
    ax.legend(loc=1, framealpha=1)
    ax.grid(axis='y')
    ax.set_ylim((-30,30))
  sns.despine(trim=True, offset=2)
  for ax in axs[0:-1]:
    ax.get_xaxis().set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.xlabel('Time [s]')
    plt.tight_layout()
  fig.subplots_adjust(hspace=0.6)
  for ftype in outputtypes:
    plt.savefig('%s/2d-3d-comparison-small-exitation.%s' % (outputfolder, ftype))

def angle_issues():
  """ Illustrate Issue of Angle Wrap Around """
  fig, axs = plt.subplots(3, 1, sharex=True)
  fig.suptitle('Issues with Use of Conventional Description of Rotations')
  time = data['3d-small']['t']

  axs[0].set_title("Polar Angles", loc='left')
  axs[1].set_title("Azimuthal Angles", loc='left')
  axs[2].set_title("Angular Velocites", loc='left')
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
  for ftype in outputtypes:
    plt.savefig('%s/3d-model-angle-issues.%s' % (outputfolder, ftype))

cas_lit_comp()
comp_large_exitation()
comp_small_exitation()
angle_issues()
