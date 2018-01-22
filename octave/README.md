
Test Scripts for Octave
=======================


It is a good practice to test this script in [octave] to be sure that your system
is properly configurated. You can use the Octave GUI and simply run the test script
"test_script_for_octave". Alternativally, you can use the command line by
typing "octave" and then::


```shell
octave:> run test_script_for_octave
```

When using in a fresh isntall, first you need to install the following
[Octave packages] : [Image], [Control] and [Signal]. To install the packages,
type in Octave::



```shell
octave:> pkg install -forge image
octave:> pkg install -forge image
octave:> pkg install -forge image
```


Notes
-----

Well-known problems:

1) Tested with Octave 3.8 and 4.X.

2) Octave version < 4 is only plotting when using the gnuplot backend. Include
the command ```graphics_toolkit gnuplot``` in the m-file.

3) You can run ```test_script_for_octave``` with oct2py, but without the plots.
This is done in `test_oct2py.py`. Also, in the end it generates some
error messages, but the results saved to an ascii file seems to be ok.


[octave]: https://www.gnu.org/software/octave/
[Octave packages]: https://octave.sourceforge.io/packages.php
[Image]: https://octave.sourceforge.io/image/index.html
[Control]: https://octave.sourceforge.io/control/index.html
[Signal]: https://octave.sourceforge.io/signal/index.html

