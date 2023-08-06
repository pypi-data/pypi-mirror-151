# UltraStar Stream Optimizer (usoptimize)

A Python CLI UltraStar Song Converter to optimize song files for the web.
It converts video files to an optimized and web playable format and converts txts to UTF-8.

## Installation

You can install the UltraStar Stream Optimizer from [PyPI](https://pypi.org/project/usoptimize/):

    python -m pip install usoptimize

The reader is supported on Python 3.0 and above.

## How to use

Before using the UltraStar Stream Optimizer, you need to install the FFmpeg.  
For windows you can use:  
https://github.com/icedterminal/ffmpeg-installer/releases

UltraStar Stream Optimizer is a command line application, named `usoptimize`. To see a help page run `usoptimize --help`.

    $ usoptimize --help
    usage: usoptimize [-h] -i <path of songs> -o <output path> [-r]

    A Python CLI UltraStar Song Converter to optimize song files for the web.

    optional arguments:
      -h, --help            show this help message and exit
      -i <path of songs>, --input <path of songs>
                            Filepath of songs that should be converted
      -o <output path>, --output <output path>
                            Destination directory of converted songs
      -r, --replace         Whether or not to replace old existing files in output
                            dir
