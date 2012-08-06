==============
 Measurements
==============

Measurements of color between calibrations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a significant difference between measurements sets of color, with different calibrations. The difference is minimal at low color/luminance values, but grows to be very significant at high values. This difference can also not be described by a change in only one fitting parameter to the gamma function, and so, as of yet, it is not possible to determine the "true" gray value from the luminance measurement and so not possible to compare measurements at high luminance/color values between different calibrations.

Difference between calibrations at high colour/luminance values:
----------------------------------------------------------------
.. image:: highend.png

Below are plots of the variatons between measurements and the variation between calibrations for different colour values:

Bean plot of calibration differences for color 800:
---------------------------------------------------
.. image:: beanplotmean_800_color.png


Bean plot of calibration differences for color 600:
---------------------------------------------------
.. image:: beanplotmean_600_color.png


Bean plot of calibration differences for color 400:
---------------------------------------------------
.. image:: beanplotmean_400_color.png


Bean plot of calibration differences for color 200:
---------------------------------------------------
.. image:: beanplotmean_200_color.png



Lines
~~~~~

For these measurements, the Lines class was used to produce two images, one with horizontal lines and one with vertical lines, of varying pixel widths. At low pixel widths (i.e. 1) there is a significant difference in luminance between horizontally and vertically oriented lines, the horizontally oriented lines are brighter.

1 pixel wide lines, measured at the monitor:
--------------------------------------------
.. image:: 1linesclose.png

1 pixel wide lines, measured at distance through box:
-----------------------------------------------------
.. image:: line1dist.png

8 pixel wide lines, measured at distance through box:
-----------------------------------------------------
.. image:: line8dist.png

32 pixel wide lines, measured at distance through box:
------------------------------------------------------
.. image:: line32dist.png

It is not yet known why there is a difference between the two orientations.

Hysteresis Loop
~~~~~~~~~~~~~~~

Measurements were taken of the luminosity of the colours first increasing from low to high, and then decreasing from high to low.
No significant difference was observed over that of the random differences between measurements.

Plot of luminance against colour value, with colour value increasing and decreasing:
------------------------------------------------------------------------------------

.. image:: hgraph3.png



Tube measurements
~~~~~~~~~~~~~~~~~

The possible difference between measurements of the luminance of the tubes from increasing voltage, and from decreasing voltage was measured. Strangely a difference is measured, though it is not clear if this is much greater than error due to recalibration, etc.

In the following graphs, the black points are the measurements decreasing from high voltage, and the coloured points are the measurements increasing from low voltage.

Hysteresis measurements for the red tube:
-----------------------------------------

.. image:: redhysteresis.png

Hysteresis measurements for the green tube:
-------------------------------------------

.. image:: greenhysteresis.png

Hysteresis measurements for the blue tube:
------------------------------------------

.. image:: bluehysteresis.png

Hysteresis measurements for all of the tubes:
---------------------------------------------

.. image:: allhysteresis.png
   
