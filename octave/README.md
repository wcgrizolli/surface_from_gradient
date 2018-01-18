 
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
[pkgOctave]: [pkgImage], [pkgControl] and [pkgSignal]. To install the packages,
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

2) Octave version < 4 is not ploting the graphs. Use the plot flag in the script.
 
  

[octave]: https://www.gnu.org/software/octave/ "GNU Octave"
[pkgOctave]: https://octave.sourceforge.io/packages.php "Octave packages"
[pkgImage]: https://octave.sourceforge.io/image/index.html "Image"
[pkgControl]: https://octave.sourceforge.io/control/index.html "Control"
[pkgSignal]: https://octave.sourceforge.io/signal/index.html "Signal"

