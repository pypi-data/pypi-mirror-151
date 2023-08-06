# ZmxTools

[![Build Status](https://github.com/wemake-services/zmxtools/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/zmxtools/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/wemake-services/zmxtools/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/zmxtools)
[![Python Version](https://img.shields.io/pypi/pyversions/zmxtools.svg)](https://pypi.org/project/zmxtools/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

A toolkit to read Zemax files.

Currently this is limited to unpacking ZAR archives. To parse the files contained within the archive, e.g. ZMX or AGF 
glass files, please check out the following projects and packages:
- [Optical ToolKit](https://github.com/draustin/otk) reads Zemax .zmx files.
- [RayTracing](https://github.com/DCC-Lab/RayTracing) reads Zemax .zmx files.
- [Zemax Glass](https://github.com/nzhagen/zemaxglass) reads Zemax .agf files.
- [RayOptics](https://github.com/mjhoptics/ray-optics) reads Zemax .zmx and CODE-V .seq files.
- [RayOpt](https://github.com/quartiq/rayopt) reads Zemax .zmx as well as OSLO files.
- [OpticsPy](https://github.com/Sterncat/opticspy) does not read Zemax .zmx files but it reads CODE-V .seq files and 
glass information from data downloaded from https://www.refractiveindex.info/.

## Features
- Unpack a Zemax OpticStudio Archive ZAR file using the `unzar` command.
- Repack a ZAR file as a standard zip file using the `unzar -z` command.
- Use as a pure Python 3 library.
- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)

## Installation
### Prerequisites
- Python 3.6 (tested on Python 3.8)
- pip, the Python package manager

To install `zmxtools`, just run the following command in a command shell:
```bash
pip install zmxtools
```

## Usage
This package can be used directly from a terminal shell or from your own Python code.

### Command line shell
The command `unzar` is added to the path upon installation. It permits the extraction of the zar-file to a sub-directory
as well as its conversion to a standard zip-file. For example, extracting to the sub-directory `mylens` is done using 
```console
unzar mylens.zar
```
Repacking the same zar-archive as a standard zip-archive `mylens.zip` is done with:
```console
unzar mylens.zar -z
```
Input and output can be specified. 
```console
unzar -h
unzar -i mylens.zar -o some/where/else/
```
More information and alternative options:
```console
unzar -h
unzar -i mylens.zar -o some/where/else/
```

### As a Python library
Extraction and repacking can be done programmatically as follows:
```python
from zmxtools import zar

zar.extract('mylens.zar')
zar.repack('mylens.zar')
zar.read('mylens.zar')
```
Python `pathlib.Path` objects can be used instead of strings.

## Online
The latest version of the source code can be found on
[github: https://github.com/tttom/zmxtools](https://github.com/tttom/zmxtools)

## License
This code is distributed under the
[agpl3: GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html)

## Credits
- [Wouter Vermaelen](https://github.com/m9710797) for decoding the ZAR header and finding LZW compressed contents.
- [Bertrand Bordage](https://github.com/BertrandBordage) for sharing this [gist](https://gist.github.com/BertrandBordage/611a915e034c47aa5d38911fc0bc7df9).
- This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [cfbc9ea21c725ba5b14c33c1f52d886cfde94416](https://github.com/wemake-services/wemake-python-package/tree/cfbc9ea21c725ba5b14c33c1f52d886cfde94416). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/cfbc9ea21c725ba5b14c33c1f52d886cfde94416...master) since then.
