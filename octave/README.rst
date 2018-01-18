 
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

2) You need to install the following `Octave packages`_ : Image_, Control_ and Signal_

.. _Octave packages: https://octave.sourceforge.io/packages.php
.. _Image: https://octave.sourceforge.io/image/index.html
.. _Control: https://octave.sourceforge.io/control/index.html
.. _Signal: https://octave.sourceforge.io/signal/index.html

To install the packages, type in Octave:

>>> octave:> pkg install -forge control
>>> octave:> pkg install -forge signal
>>> octave:> pkg install -forge image

::
  octave:> pkg install -forge image
  octave:> pkg install -forge image
  octave:> pkg install -forge image
