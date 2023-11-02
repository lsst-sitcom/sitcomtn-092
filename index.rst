################################################
.. _LVV-T2854: https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T2854
.. _LVV-T2811: 
.. _MTMount.azimuth: https://ts-xml.lsst.io/sal_interfaces/MTMount.html#azimuth
.. _MTMount.elevation: https://ts-xml.lsst.io/sal_interfaces/MTMount.html#elevation
.. _MTM1M3.appliedAccelerationForces: https://ts-xml.lsst.io/sal_interfaces/MTM1M3.html#appliedAccelerationForces
.. _MTM1M3.appliedVelocityForces: https://ts-xml.lsst.io/sal_interfaces/MTM1M3.html#appliedVelocityForces
.. _MTM1M3.hardpointActuatorData: https://ts-xml.lsst.io/sal_interfaces/MTM1M3.html#hardpointactuatordata
.. _sitcomtn-088: https://sitcomtn-088.lsst.io

:tocdepth: 1

.. abstract::

   The M1M3 Force Balance System was engineered to mitigate the influence of gravity/elevation forces, thermal fluctuations, and inertia impacts. This technical note presents an initial analysis of the Force Balance System's performance when implementing corrections to account for inertia effects.



.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

.. note::

  **This technote is a work-in-progress.**

  Access https://sitcomtn-088.lsst.io/ for other technotes associated with M1M3 tests and analysis.

Abstract
========

The M1M3 Force Balance System (FBS) was engineered to mitigate the influence of gravity/elevation forces, thermal fluctuations, and inertia forces.
This technical note presents an initial performance analysis of what we call **Inertia Compensation System** (ICS).
This ICS is componsed by the Force Balance System and a set sensors that measure the telescope acceleration when slewing.
The analysis is based on the telemetry collected during the integration of the M1M3 Force Balance System with the telescope main assembly (TMA).

Introduction
============

..
   - Who, what, when, where?
   - Definitions
   - Purpose/use of the document - Why?
   - Background - Why?
   - Scope - Why?
   - Methodology - How?
   - Results - What?

This document presents the analysis and characterization of the M1M3's Inertia Compensation System (ICS).
The ICS comes into play when the telescope moves in azimuth, elevation or both.
Its major role consists into offloading the inertia forces to the 156 Force Actuators (FA).
If it works correctly, the forces measured by six hardpoints (HPs) are almost zero.

We tested the ICS performance by moving the telescope in elevation and azimuth with limited performance.
We started at 1% of the maximum velocity, acceleration and jerk values and increased them up to 50%.
We could not go beyond 50% because the ICS could not offload the inertia forces properly using the current setup.
In tests executed before the beginnig of October 2023 ICS uses telemetry from the mount to estimate the inertia forces.

Requirements
============

.. note:
  @hdrass and @pzorzi - Please, add any relevant requirements here.


Data Collection
===============

Integration with M1M3 started mid May, 2023.
After quasi-static tests, we started to move the telescope with higher velocities, accelerations and jerks.
For sake of compactness, we call these thee parameters as **performance settings**.
The values of the performance setings are in the table below.

+------+---------+---------+---------+---------+---------+---------+
+      + Az Vel  + Az Acc  + Az Jerk  + El Vel +  El Acc + El Jerk +
+      + (deg/s) +(deg/s^2)+(deg/s^3)+ (deg/s) +(deg/s^2)+(deg/s^3)+
+------+---------+---------+---------+---------+---------+---------+
+ 100% + 10.5    + 10.5    + 42      + 5.25    + 5.25    + 21      +
+ 90%  + 9.45    + 9.45    + 37.8    + 4.725   + 4.725   + 18.9    +
+ 80%  + 8.4     + 8.4     + 33.6    + 4.2     + 4.2     + 16.8    +
+ 70%  + 7.35    + 7.35    + 29.4    + 3.675   + 3.675   + 14.7    +
+ 60%  + 6.3     + 6.3     + 25.2    + 3.15    + 3.15    + 12.6    +
+ 50%  + 5.25    + 5.25    + 21      + 2.625   + 2.625   + 10.5    +
+ 40%  + 4.2     + 4.2     + 16.8    + 2.1     + 2.1     + 8.4     +
+ 35%  + 3.675   + 3.675   + 14.7    + 1.8375  + 1.8375  + 7.35    +
+ 30%  + 3.15    + 3.15    + 12.6    + 1.575   + 1.575   + 6.3     +
+ 25%  + 2.625   + 2.625   + 10.5    + 1.3125  + 1.3125  + 5.25    +
+ 20%  + 2.1     + 2.1     + 8.4     + 1.05    + 1.05    + 4.2     +
+ 10%  + 1.05    + 1.05    + 4.2     + 0.525   + 0.525   + 2.1     +
+ 5%   + 0.525   + 0.525   + 2.1     + 0.2625  + 0.2625  + 1.05    +
+ 1%   + 0.105   + 0.105   + 0.42    + 0.0525  + 0.0525  + 0.21    +
+------+---------+---------+---------+---------+---------+---------+

For each performance settings we have test a Gateway Test and a Dynamic Test.
These tests are described in the JIRA Zephyr Scale Test Cases below:

1. LVV-T2854_ - Gateway Test for the M1M3 Dynamic Test, low speed, low acceleration - Data Collection
2. LVV-T2811_ - M1M3 Dynamic Test, low speed, low acceleration - Data Collection

These two test cases are then translated to the following BLOCKs:



Telemetry
---------

The force balance system is responsible to support the mirror and keep its shape.
Both are affected by external factors like gravity, thermal variations, and inertia during slews and track.
For this technote, we are interested in characterizing only the applied forces associated with telescope motion.
The relevant telemetry are:

  - `MTM1M3.appliedAccelerationForces`_
  - `MTM1M3.appliedVelocityForces`_

The Force Balance system should offload the forces applied to the six hardpoints.
Because of that, we want to include the following telemetry to our analysis:

  - `MTM1M3.hardpointActuatorData`_

Which contains a topic with the measured forces applied to the HPs.
Finally, we want to use the telescope mount telemetry (mtmount) to gather the information about the telescope motion.

  - `MTMount.azimuth`_
  - `MTMount.elevation`_

Single Slew Analysis
====================

- Explain test setup
- Explain data mining
- Explain analysis

Day Analysis
============

- Explain test setup
- Explain data mining
- Explain analysis

Conclusion
==========

- Summarize the results

References
==========

- sitcomtn-088_

.. Make in-text citations with: :cite:`bibkey`.
.. Uncomment to use citations
.. .. rubric:: References
..
.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :style: lsst_aa