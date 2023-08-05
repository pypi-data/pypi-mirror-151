[![pypi](https://img.shields.io/pypi/v/cartolidar.svg)](https://pypi.org/project/cartolidar/)
[![Coverage Status](https://codecov.io/gh/cartolidar/cartolidar/branch/main/graph/badge.svg)](https://codecov.io/gh/cartolidar/cartolidar)
[![Join the chat at https://gitter.im/cartolidar/cartolidar](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cartolidar/cartolidar?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/cartolidar/cartolidar/main)

CartoLidar
----------

Tools for Lidar processing focused on Spanish PNOA datasets (https://pnoa.ign.es/el-proyecto-pnoa-lidar)

Herramientas python para procesado de datos Lidar del PNOA (https://pnoa.ign.es/el-proyecto-pnoa-lidar)

Introduction
------------

CartoLidar es una coleción de herramientas destinadas a procesar ficheros
lidar (las y laz) y generar a partir de los rasters obtenidos otros productos
de utilidad en selvicultura y otras area de gestión del medio natural.

El proyecto está en fase alpha e incluye únicamente la herramienta "clidtwins".

clidtwins está destinada a buscar zonas similares a una(s) de referencia en
términos de determinadas variables dasoLidar (DLVs).

DLV: variable Lidar que describe algún aspecto de la estructura de una formación arbolada, arbustiva o de matorral.

>CartoLidar is a collection of tools to process lidar files "las" and "laz" and
>generate other products aimed to forestry and natural environment management.
>
>This project is in alpha version and includes only the "clidtwins" tool.
>
>"clidtwins" searchs for similar areas to a reference one in terms of dasoLidar Variables (DLVs)
>DLV: Lidar variables that describe or characterize forest structure (or vegetation in general).


Consultar documentación en: [cartolidar.org](http://cartolidar.org)

Documentation available at [cartolidar.org](http://cartolidar.org)

[Read the Docs](http://cartolidar.readthedocs.io/en/latest/)


Install
--------

1. Instalation of official version from [pypi - cartolidar](https://pypi.org/project/cartolidar/):
```
$ pip install cartolidar
```

2. Download of development version from [github - cartolidar](https://github.com/cartolid/cartolidar)

This version can be instaled in lib/site-packages (ie, using cmd in Windows):
```
$ cd path_to_project
$ pip install .
```

or the olther way (not recommendable):
```
$ cd path_to_project
$ python setup.py install
```

where:
  path_to_project is the path that contains setup.py


Requeriments
------------
cartolidar requires Python 3.7 or higher. See requirements.txt.


Use
--------
## Uso de cartolidar
### Uso en linea de comandos

1. Ejecutar el paquete cartolidar:
```
$ python -m cartolidar [ options ]
```
Se inicia un menu con modulos que usan las herramientas de cartolidar, como qlidtwins.py)

&nbsp;&nbsp;&nbsp;&nbsp;options:

...


2. Importar desde un script (.py) o desde el interprete interactivo; hay varias opciones:
```
import cartolidar
from cartolidar import clidtools
from cartolidar.clidtools import clidtwins
from cartolidar.clidtools.clidtwins import DasoLidarSource
```


to be continued...



[Ayuda Markdown](https://guides.github.com/features/mastering-markdown/)

[![Actions Status](https://github.com/cartolidar/cartolidar/workflows/Tests/badge.svg)](https://github.com/cartolidar/cartolidar/actions?query=workflow%3ATests)
