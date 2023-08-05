import marshmallow_dataclass
import numpy as np
from marshmallow.fields import Field
from marshmallow_dataclass import NewType


@marshmallow_dataclass.dataclass
class PixelCoord:
    x: float
    y: float


@marshmallow_dataclass.dataclass
class GlobalCoord:
    x: float
    y: float
    z: float


class NumpyField(Field):
    def _deserialize(self, value, *args, **kwargs):
        if isinstance(value, dict):
            value = self._extract_list(value)
        return np.array(value)

    def _extract_list(self, value):
        value_as_list = []
        if "x" in value:
            value_as_list.append(value["x"])
        if "y" in value:
            value_as_list.append(value["y"])
        if "z" in value:
            value_as_list.append(value["z"])
        return value_as_list


NumpyArray = NewType("NdArray", np.ndarray, field=NumpyField)
