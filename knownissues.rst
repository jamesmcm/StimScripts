==============
Known Issues
==============

Slow photometer measurement without threading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the moment, the measurement process in not in a separate thread from the refreshing of the display. This is a problem with, for example, the CRTTest stimulus, where taking measurements will pause the oscillations of the background luminance.

This could be fixed via threading, but the photometer measurements of these animated stimuli are not so important, so I did not consider it worth the additional complexity.

