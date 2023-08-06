# TriangleDrawer

This package will enable you to draw any triangle on screen and see its measurements.

## Installation
Install this package using `pip`
```
pip install triangle_drawer
```

## Usage
You can either create a triangle using the three side lengths:
```python
from triangle_drawer import Triangle

Triangle(3, 4, 5).draw()
```
Or you can create a triangle using two side lengths and the angle between them (in degrees):
```python
from triangle_drawer import Triangle

Triangle(3.5, 4.5, angle=45.6).draw()
```
## License

The project is licensed under the MIT license.