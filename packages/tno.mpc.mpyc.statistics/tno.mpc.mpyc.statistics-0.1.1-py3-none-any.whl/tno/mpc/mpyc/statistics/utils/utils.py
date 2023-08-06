"""
Utilities to be used within the statistics package.
"""
from typing import TypeVar

from mpyc.runtime import mpc
from mpyc.sectypes import SecureFixedPoint

from .types import Matrix, Vector

AnyTV = TypeVar("AnyTV")


def matrix_transpose(matrix: Matrix[AnyTV]) -> Matrix[AnyTV]:
    """
    Transpose a list of lists.

    .. code-block:: python

        A = [[31, 64], [32, 68], [33, 72], [34, 76]]
        matrix_transpose(A) == [[31, 32, 33, 34], [64, 68, 72, 76]]

    :param matrix: Matrix stored as list of lists
    :return: Transpose of matrix
    """
    return list(map(list, zip(*matrix)))


def vector_eq(
    vec_1: Vector[SecureFixedPoint], vec_2: Vector[SecureFixedPoint]
) -> Vector[SecureFixedPoint]:
    """
    Performs equality check between two vectors

    :param vec_1:
    :param vec_2:
    :returns: A vector of equalities
    """
    return [mpc.eq(left, right) for left, right in zip(vec_1, vec_2)]
