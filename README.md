# mot-from-csv
Create a OpenSim compatible .mot files from .csv files

Make OpenSim compatible .mot from a .csv file.
In this code the csv files are exported from c3d files using Mokka software.

## Usage:
    motFromCsv.py -csv_file <source_file> -amputation <amp_leg>
    motFromCsv.py (h | --help)
    motFromCsv.py --version
## Options:
    -h --help
    --version
    -csv_file       Input file that contains joint coordinates.
    -amputation     Amputated leg (left|right|none)
