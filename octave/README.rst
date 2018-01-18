 
=======================
Test Scripts for Octave
=======================


It is a good practice to test this script in Octave to be sure that your system is properly configurated.

You can use the Octave GUI and simply run the test script "test_script_for_octave". Alternativally, you can use the command line by typing "octave" and then

>>> octave:> run test_script_for_octave


-----
Notes
-----

Well known problems:

1) Octave version < 4 is not ploting the graphs. Use the plot flag within the script.

2) you need to install the Image, the Control and the Signal packages_ for Octave.

.. _packages: https://octave.sourceforge.io/packages.php

In Octave, type:

>>> octave:> pkg install -forge control
>>> octave:> pkg install -forge signal
>>> octave:> pkg install -forge image