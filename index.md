# M1M3 Force Balance System - Inertia Compensation

```{eval-rst}
.. abstract::

   The M1M3 Force Balance System was engineered to mitigate the influence of gravity/elevation forces, thermal fluctuations, inertial forces.

   This technical note presents an initial analysis of the Force Balance System's performance when implementing corrections to account for inertial effects.

```

% Metadata such as the title, authors, and description are set in metadata.yaml

% TODO: Delete the note below before merging new content to the main branch.

:::{note}
**This technote is a work-in-progress.**
:::

## Introduction

- What is the Inertia Compensation System?
  - Balance Forces
  - Acceleration Forces
  - Velocity Forces
  - Booster Valves
  - What are the RRGG codes we see around? Why are they important?

- [TMA Motion Settings](https://rubinobs.atlassian.net/wiki/spaces/LSSTCOM/pages/53741249/TMA+Motion+Settings)
  - Why do we have different motion settings?


## Single Slew Analysis

During the full-speed sky mapping mission, the telescope will move very quickly, generating significant inertial forces. 
To counteract these forces, the **Inertial Compensation System (ICS)** is employed. 
The ICS consists of accelerometers and gyroscopic sensors that measure the telescope's motion and activate during slews in elevation, azimuth, or both axes. 
This system is critical for minimizing the physical effects of inertial forces on the telescope's structure.
The test involves short slews of 3.5 degrees (long slews defined as > 3.5 degrees and short slews as ≤ 3.5 degrees). 
The objective is to measure forces in the six **Hardpoints (HPs)**, ensuring they remain below the breakaway limits.
The nominal breakaway limit, previously measured is **3000 N**, defines the maximum force a hardpoint can withstand before disengaging to protect the mirror. 
Breakawy testing involved applying compression and tension forces to each hardpoint until breakaway occurred, confirming that the limits were within the expected range.

### Dynamic Test and Hardpoint Forces
The dynamic test measures the force on the six Hardpoints where nominal force measurements should ideally remain at zero during slews.
The limits of Hardpoints do not bear excessive loads, forces ideally not crossing the 15% of breakway limits (450 N), forces exceeding this threshold risk long-term mirror damage.

#### Test Configurations
The tests were conducted on two observation days: **2024-01-03 and 2024-01-05**.

   1.	**100% Velocity, Acceleration, and Jerk (2024-01-03)**:
   - Forces on the Hardpoints stay within the nominal breakaway limit (3000 N)  but exceed the 30% fatigue limit (900 N).
   - This configuration poses a risk of mirror damage due to stress and fatigue.

<img width="554" alt="hp100%velo" src="https://github.com/user-attachments/assets/79fc7f7f-2327-4988-9000-49580eee0916" />
     	
   3.	**40% Velocity, Acceleration, and Jerk (2024-01-05)**:
   - Forces on the Hardpoints remained within the 15% operational limit (450 N).
   - This configuration is safe for long-term operation, minimizing stress on the mirror.

<img width="550" alt="hp40%velo" src="https://github.com/user-attachments/assets/65247b16-91f5-4673-bf55-e2c35981c7ac" />

     	
The ICS effectively compensated for inertial forces at moderate speeds (40% velocity, acceleration, and jerk). 
However, at TMA maximum motion settings (100%), the measured forces exceeded the fatigue limits, raising concerns about long-term mirror safety. 
To ensure the telescope's safety and longevity, slews should be configured to maintain Hardpoint forces within the **15% operational limit (450 N)**.

### Histogram Analysis
The same data collected on the observation days, **2024-01-03 and 2024-01-05**, is displayed as a histogram to organize the data into groups for these specific observation days. 
The histogram illustrates the slews performed at 100% and 40% velocity, along with the corresponding acceleration and jerk, which reached certain minimum and maximum values during the slewing process.

#### Test Configurations
   1. **100% Velocity, Acceleration, and Jerk (2024-01-03)**:
   - It is observed that almost every slew performed in this 100% configuration exceeds the negative and positive fatigue limits of 900 N, which poses a significant danger to the mirror in the long term due to stress and fatigue.
     
<img width="833" alt="histogram100%VEL" src="https://github.com/user-attachments/assets/7b438e0f-dfd0-425b-9117-9c60fc5d669b" />
        
   3. **40% Velocity, Acceleration, and Jerk (2024-01-05)**:
   - It is observed that almost every slew obtained during soak tests remains within the fatigue limits of 900 N, with the majority close to or within the operational limits of 450 N.

<img width="839" alt="histogram40%VELO" src="https://github.com/user-attachments/assets/57ba286f-fddb-4dcd-99ab-56bcb3fcf183" />


**Key Limits:**
   - **Nominal Breakaway Limit**: 3000 N (absolute maximum force hardpoints can handle).
   - **Fatigue Limit**: 30% of 3000 N (900 N); forces above this risk long-term mirror damage.
   - **Operational Limit**: 15% of 3000 N (450 N); target for safe, long-term operation.


## M1M3 and M2 Surrogates Test Campaigns

- When did they happen? Dates.
- What tests did we execute? Those were BLOCK tickets, instead of test cases. List them.
- Final results - add a link to SPIE Paper. There is no need to repeat information.


## ComCam on Sky Campaign

- What were the settings used?
- What are the results?
- Add links to the existing notebooks, plots, etc.
- Add interpretation to these results.


%% TODO - @pvenegas - Delete everything below this line
## M1M3 actuator movies

Craig Lage - 20-Apr-23 The 17 tons of mirror are supported by 156 pneumatic actuators where 44 are single-axis and provide support only on the axial direction, 100 are dual-axis providing support in the axial and lateral direction, and 12 are dual-axis providing support in the axial and cross lateral directions. Positioning is provided by 6 hard points in a hexapod configuration which moves the mirror to a fixed operational position that shall be maintained during telescope operations. The remaining optical elements will be moved relative to this position in order to align the telescope optics. Support and optical figure correction is provided by 112 dual axis and 44 single axis pneumatic actuators.

### Ticket SITCOM-763

M1M3 should be raised for this test. (Check this tbc)

We tested the M1M3 force balance system by applying external force over the surrogate. The force was applied by stepping on random position on the surrogate surface.

Date: 18.04.23 15.30 - 15.40h CLT.

We looked at the M1M3 EUI at the measured forces at the Actuator 2D map.

The expected result was that we see smooth gradients depending on where people were stepping.

We see the movement in the applied actuator forces. See attached video.

For detailed offline analysis: Create an animation of the 2D map for this period with a fixed color scale. Use the nominal position as a reference position.

### Prepare the notebook

```
python # Directory to store the data

```

```python
% dir_name = "/home/c/cslage/u/MTM1M3/movies/"
%
% # Times to make the plot
% start = "2023-04-18 16:10:00Z"
% end = "2023-04-18 16:15:00Z"
%
% autoScale = True
% # The following are only used if autoScale = False
% zmin = 0.0 # In nt
% zmax = 2000.0 # In nt
% lateral_max = 1500.0 # In nt
%
% # The following average the first 100 data points
% # and subtract these from the measurements
% # If subtractBasline = False, the unmodified values will be plotted
% subtract_baseline = True
% baseline_t0 = 0.0
% baseline_t1 = 100.0
%
% # The following allows you to plot only every nth data point
% # If this value is 1, a frame will be made for every data point
% # Of course, this takes longer
% # If this value is 50, it will make a frame every second
% frame_n = 50
```

```python
python import asyncio import glob import os import shlex import subprocess import sys from pathlib import Path from datetime import datetime import matplotlib.pyplot as plt
import numpy as np

from astropy.time import Time, TimeDelta

from matplotlib.colors import LightSource

from lsst.ts.xml.tables.m1m3 import FAOrientation, FATable, FAType

from lsst_efd_client import EfdClient
```

### Set up the necessary subroutines

```python
def actuator_layout(ax):
    """ Plot a visualization of the actuator locations and types       Parameters      ----------       ax : a matplotlib.axes object
      Returns
     -------
      No return, only the ax object which was input
   """
   ax.set_xlabel("X position (m)")
   ax.set_ylabel("Y position (m)")
   ax.set_title("M1M3 Actuator positions and type\nHardpoints are approximate", fontsize=18)
   types = [
             [FAType.SAA, FAOrientation.NA, 'o', 'Z', 'b'],
             [FAType.DAA, FAOrientation.Y_PLUS, '^', '+Y','g'],
             [FAType.DAA, FAOrientation.Y_MINUS, 'v', '-Y', 'cyan'],
             [FAType.DAA, FAOrientation.X_PLUS, '>', '+X', 'r'],
             [FAType.DAA, FAOrientation.X_MINUS, '<', '-X', 'r'],
         ]
   for [type, orient, marker, label, color] in types:
      xs = []
      ys = []
      for fa in FATable:
            x = fa.x_position
            y = fa.y_position
            if fa.actuator_type == type and \
               fa.orientation == orient:
               xs.append(x)
               ys.append(y)
            else:
               continue
      ax.scatter(xs, ys, marker=marker, color=color, s=200, label=label)

 # Now plot approximate hardpoint location
 Rhp = 3.1 # Radius in meters
 for i in range(6):
     theta = 2.0 * np.pi / 6.0 * float(i)
     if i == 0:
         ax.scatter(Rhp * np.cos(theta), Rhp * np.sin(theta), marker='o', color='magenta', \
                    s=200, label='HP')
     else:
         ax.scatter(Rhp * np.cos(theta), Rhp * np.sin(theta), marker='o', color='magenta', \
                    s=200, label='_nolegend_')
 ax.legend(loc='lower left', fontsize=9)
 return


def bar_chart_z(df, df_zero, ax, index, zmin, zmax):
 """ Plot a 3D bar chart of the actuator Z forces
     Parameters
     ----------
     df: pandas dataframe
         The pandas dataframe object with the force actuator data

     df_zero: pandas dataframe
         The pandas dataframe object of the quiescent force data
         which will be subtracted off from the force actuator data

     ax : a matplotlib.axes object

     index: 'int'
         The index of the movie frame

     zmin: 'float'
         The minimum force value for the plot

     zmax: 'float'
         The maximum force value for the plot

     Returns
     -------
     No return, only the ax object which was input
 """

 ax.set_xlabel("X position (m)")
 ax.set_ylabel("Y position (m)")
 ax.set_zlabel("Force (nt)")
 ax.set_title("M1M3 Actuator Z forces", fontsize=18)

 light_source = LightSource(azdeg=180, altdeg=78)
 grey_color = '0.9'
 colors = []
 xs = []
 ys = []
 for fa in FATable:
     x = fa.x_position
     y = fa.y_position
     xs.append(x)
     ys.append(y)
     if fa.actuator_type == FAType.SAA:
         colors.append('blue'); colors.append('blue')
         colors.append(grey_color); colors.append(grey_color)
         colors.append(grey_color); colors.append(grey_color)
     else:
         if fa.orientation in [FAOrientation.Y_PLUS, FAOrientation.Y_MINUS]:
             colors.append('green'); colors.append('green')
             colors.append(grey_color); colors.append(grey_color)
             colors.append(grey_color); colors.append(grey_color)
         else:
             colors.append('red'); colors.append('red')
             colors.append(grey_color); colors.append(grey_color)
             colors.append(grey_color); colors.append(grey_color)

 zs = np.zeros([len(FATable)])
 for fa in FATable:
     name=f"zForce{fa.index}"
     zs[fa.index] = df.iloc[index][name] - df_zero.iloc[0][name]

 dxs = 0.2 * np.ones([len(FATable)])
 dys = 0.2 * np.ones([len(FATable)])
 bottom = np.zeros([len(FATable)])
 ax.bar3d(xs, ys, bottom, dxs, dys, zs, shade=True, alpha=0.5, \
          lightsource=light_source, color=colors)
 ax.set_zlim(zmin, zmax)
 ax.view_init(elev=30., azim=225)
 return


def heat_map_z(df, df_zero, ax, index, zmin, zmax):
 """ Plot a "heat map" of the actuator Z forces
     Parameters
     ----------
     df: pandas dataframe
         The pandas dataframe object with the force actuator data

     df_zero: pandas dataframe
         The pandas dataframe object of the quiescent force data
         which will be subtracted off from the force actuator data

     ax : a matplotlib.axes object

     index: 'int'
         The index of the movie frame

     zmin: 'float'
         The minimum force value for the plot

     zmax: 'float'
         The maximum force value for the plot

     Returns
     -------
     No return, only the ax object which was input
 """

 ax.set_xlabel("X position (m)")
 ax.set_ylabel("Y position (m)")
 ax.set_title("M1M3 Actuator Z forces (nt)", fontsize=18)

 types = [
             [FAType.SAA, FAOrientation.NA, 'o', 'Z'],
             [FAType.DAA, FAOrientation.Y_PLUS, '^', '+Y'],
             [FAType.DAA, FAOrientation.Y_MINUS, 'v', '-Y'],
             [FAType.DAA, FAOrientation.X_PLUS, '>', '+X'],
             [FAType.DAA, FAOrientation.X_MINUS, '<', '-X'],
         ]

 for [type, orient, marker, label] in types:
     xs = []
     ys = []
     zs = []
     for fa in FATable:
         x = fa.x_position
         y = fa.y_position
         if fa.actuator_type == type and \
             fa.orientation == orient:
             xs.append(x)
             ys.append(y)
             name=f"zForce{fa.index}"
             zs.append(df.iloc[index][name] - df_zero.iloc[0][name])
     im = ax.scatter(xs, ys, marker=marker, c=zs, cmap='RdBu_r', \
                         vmin=zmin, vmax=zmax, s=50, label=label)
 plt.colorbar(im, ax=ax,fraction=0.055, pad=0.02, cmap='RdBu_r')
 return



def lateral_forces(df, df_zero, ax, index, force_max):
 """ Plot a 2D whisker plot of the actuator X and Y forces
     Parameters
     ----------
     df: pandas dataframe
         The pandas dataframe object with the force actuator data

     df_zero: pandas dataframe
         The pandas dataframe object of the quiescent force data
         which will be subtracted off from the force actuator data

     ax : a matplotlib.axes object

     index: 'int'
         The index of the movie frame

     force_max: 'float'
         maximum force values for scaling the whisker arrows

     Returns
     -------
     No return, only the ax object which was input
 """

 ax.set_xlabel("X position (m)")
 ax.set_ylabel("Y position (m)")
 ax.set_title("M1M3 lateral forces (nt)", fontsize=18)
 ax.set_xlim(-4.5,4.5)
 ax.set_ylim(-4.5,4.5)
 types = [
             [FAType.DAA, FAOrientation.Y_PLUS, '^', '+Y','g'],
             [FAType.DAA, FAOrientation.Y_MINUS, 'v', '-Y', 'cyan'],
             [FAType.DAA, FAOrientation.X_PLUS, '>', '+X', 'r'],
             [FAType.DAA, FAOrientation.X_MINUS, '<', '-X', 'r'],
         ]
 for [type, orient, marker, label, color] in types:
     xs = []
     ys = []
     arrow_xs = []
     arrow_ys = []
     for fa in FATable:
         x = fa.x_position
         y = fa.y_position
         if fa.actuator_type == type and \
             fa.orientation == orient:
             xs.append(x)
             ys.append(y)
             if orient == FAOrientation.X_PLUS:
                 name = f"xForce{fa.x_index}"
                 arrow_xs.append(df.iloc[index][name] / force_max)
                 arrow_ys.append(0.0)
             elif orient == FAOrientation.X_MINUS:
                 name = f"xForce{fa.x_index}"
                 arrow_xs.append(-df.iloc[index][name] / force_max)
                 arrow_ys.append(0.0)
             elif orient == FAOrientation.Y_PLUS:
                 name = f"yForce{fa.y_index}"
                 arrow_xs.append(0.0)
                 arrow_ys.append(df.iloc[index][name] / force_max)
             else:
                 name = f"yForce{fa.y_index}"
                 arrow_xs.append(0.0)
                 arrow_ys.append(-df.iloc[index][name] / force_max)
         else:
             continue
     ax.scatter(xs, ys, marker=marker, color=color, s=50, label=label)
     for ii in range(len(xs)):
         ax.arrow(xs[ii], ys[ii], arrow_xs[ii], arrow_ys[ii], color=color)

 ax.plot([-4.0,-3.0], [-4.0,-4.0], color='g')
 ax.text(-4.0, -4.3, f"{force_max} nt")
 return


def get_zero_values_and_limits(df, subtract_baseline, t0, t1):


 """ Plot a 2D whisker plot of the actuator X and Y forces
     Parameters
     ----------
     df: pandas dataframe
         The pandas dataframe object with the force actuator data.

     subtract_baseline : 'bool'
         Determines whether or not to subtract off a baseline value from the plots.

     t0: 'float'
         The time from the beginning of the dataframe when the baseline
         quiescent period (which will be subtracted off) begins.

     t1: 'float'
         The time from the beginning of the dataframe when the baseline
         quiescent period (which will be subtracted off) ends.

     Returns
     -------
     zmin: 'float'
         The minimum force value for the Z force plots

     zmax: 'float'
         The maximum force value for the Z force plots

     lateral_max: 'float'
         The maximum force value for the X,Y whisker plots


     df_zero: pandas dataframe
         The pandas dataframe object of the quiescent force data
         which will be subtracted off from the force actuator data

 """
 df_zero = df.head(1)
 for column_name in df_zero.columns:
     try:
         if subtract_baseline:
             df_zero.iloc[0, df_zero.columns.get_loc(column_name)] = \
                 np.median(df[column_name].values[t0:t1])
         else:
             df_zero.iloc[0, df_zero.columns.get_loc(column_name)] = 0.0
     except:
         continue
 # Now calculate the limits
 zmin = 0.0; ymin = 0.0; xmin = 0.0; zmax = 0.0; ymax = 0.0; xmax = 0.0
 for fa in FATable:
     name = f"zForce{fa.z_index}"
     zmin = min(zmin, np.min(df[name] - df_zero.iloc[0][name]))
     zmax = max(zmax, np.max(df[name] - df_zero.iloc[0][name]))
     if fa.y_index is not None:
         name = f"yForce{fa.y_index}"
         ymin = min(ymin, np.min(df[name] - df_zero.iloc[0][name]))
         ymax = max(ymax, np.max(df[name] - df_zero.iloc[0][name]))
     if fa.x_index is not None:
         name = f"xForce{fa.x_index}"
         xmin = min(xmin, np.min(df[name] - df_zero.iloc[0][name]))
         xmax = max(xmax, np.max(df[name] - df_zero.iloc[0][name]))

 lateral_max = max(xmax, ymax, -xmin, -ymin)
 return [round(zmin), round(zmax), round(lateral_max), df_zero]
```

### Now generate the frames
This will take some time

```python
  client = EfdClient('usdf_efd')

  forces = await client.select_time_series("lsst.sal.MTM1M3.forceActuatorData", "*",
                                        Time(start, scale='utc'), Time(end, scale='utc'))
  timestamp = forces.index[0].isoformat().split('.')[0].replace('-','').replace(':','')
  os.makedirs(Path(dir_name) / f"movie_{timestamp}", exist_ok=True)
  [auto_zmin, auto_zmax, auto_lateral_max, forces_zero] = \
   get_zero_values_and_limits(forces, subtract_baseline, baseline_t0, baseline_t1)

  if autoScale:
   zmin = auto_zmin
   zmax = auto_zmax
   lateral_max = auto_lateral_max


  # Build the individual frames
  fig = plt.figure(figsize=(16,16))
  for n in range(0, len(forces), frame_n):

   ax1 = fig.add_subplot(2,2,1)
   actuator_layout(ax1)
   ax2 = fig.add_subplot(2,2,2, projection='3d')
   bar_chart_z(forces, forces_zero, ax2, n, zmin, zmax)
   ax3 = fig.add_subplot(2,2,3)
   lateral_forces(forces, forces_zero, ax3, n, lateral_max)
   ax4 = fig.add_subplot(2,2,4)
   heat_map_z(forces, forces_zero, ax4, n, zmin, zmax)
   plt.savefig(f"{dir_name}/movie_{timestamp}/Frame_{n:05d}.png")
   plt.clf()

  len(forces)
```

### Now build the movie

```python
print(f"\033[1mThe movie name will be: {dir_name}movie_{timestamp}/m1m3_movie.mp4\033[0m")
```

```python
command = f"ffmpeg -pattern_type glob -i '{dir_name}movie_{timestamp}/*.png' -f mp4 -vcodec libx264 -pix_fmt yuv420p -framerate 50 -y {dir_name}movie_{timestamp}/m1m3_movie.mp4" args = shlex.split(command) build_movie = subprocess.Popen(args) build_movie.wait()

```

See the [reStructuredText Style Guide](https://developer.lsst.io/restructuredtext/style.html) to learn how to create sections, links, images, tables, equations, and more.

% Make in-text citations with: :cite:`bibkey`.

% Uncomment to use citations

% .. rubric:: References

%

% .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib

% :style: lsst_aa
