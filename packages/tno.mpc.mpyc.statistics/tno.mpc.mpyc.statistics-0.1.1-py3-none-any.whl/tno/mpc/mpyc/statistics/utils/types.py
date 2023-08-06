"""
Types to use for type hinting.
"""
from typing import List, TypeVar, Union

import numpy as np
import numpy.typing as npt

TemplateType = TypeVar("TemplateType")
Number = Union[float, int]

Vector = List[TemplateType]
Matrix = List[List[TemplateType]]
NumpyFloatArray = npt.NDArray[np.float_]
NumpyIntegerArray = npt.NDArray[np.int_]
NumpyObjectArray = npt.NDArray[np.object_]
NumpyNumberArray = Union[NumpyIntegerArray, NumpyFloatArray]
