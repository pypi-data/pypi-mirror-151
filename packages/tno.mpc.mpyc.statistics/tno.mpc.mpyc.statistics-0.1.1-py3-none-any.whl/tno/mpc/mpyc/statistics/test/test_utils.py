"""
Tests the utils
"""
import numpy as np
import pytest
from mpyc.runtime import mpc

from tno.mpc.mpyc.statistics.utils.types import Matrix
from tno.mpc.mpyc.statistics.utils.utils import matrix_transpose, vector_eq

secfloat = mpc.SecFxp()


@pytest.mark.parametrize(
    "mat_1",
    [[[31, 64], [32, 68], [33, 72], [34, 76]]],
)
@pytest.mark.parametrize(
    "mat_2",
    [[[31, 64], [32, 68]]],
)
def test_matrix_transpose(mat_1: Matrix[int], mat_2: Matrix[int]) -> None:
    """
    Test matrix transpose in the utils folder

    :param mat_1: Example matrix
    :param mat_2: Another example matrix
    """
    mat_1_t = matrix_transpose(mat_1)
    mat_2_t = matrix_transpose(mat_2)

    mat_1_t_np = np.transpose(mat_1).tolist()
    mat_2_t_np = np.transpose(mat_2).tolist()

    assert np.array_equal(mat_1_t, mat_1_t_np) and np.array_equal(mat_2_t, mat_2_t_np)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, -3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [1.0, -3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [2.1, 2.1, -44.2, 91.9, 22.1, 1.21, 0.0],
            [2.1, 2.1, -44.2, 91.9, 22.1, 123, 0.0],
        ],
    ],
)
async def test_vector_eq(values: Matrix[float]) -> None:
    """
    Test secure vector equality

    :param values: Vectors to be tested for equality
    """
    vec_1 = values[0]
    vec_2 = values[1]
    vec_3 = values[2]
    vec_4 = values[3]

    expected_is_same1 = np.array_equal(vec_1, vec_2)
    expected_is_same2 = np.array_equal(vec_3, vec_4)

    secure_val_1 = [secfloat(i) for i in vec_1]
    secure_val_2 = [secfloat(i) for i in vec_2]
    secure_val_3 = [secfloat(i) for i in vec_3]
    secure_val_4 = [secfloat(i) for i in vec_4]

    sec_cmp1 = vector_eq(secure_val_1, secure_val_2)
    sec_cmp2 = vector_eq(secure_val_3, secure_val_4)

    revealed_cmp1 = await mpc.output(sec_cmp1)
    revealed_cmp2 = await mpc.output(sec_cmp2)

    actual_is_same_1 = len(set(revealed_cmp1)) == 1
    actual_is_same_2 = len(set(revealed_cmp2)) == 1

    assert (actual_is_same_1 == expected_is_same1) and (
        actual_is_same_2 == expected_is_same2
    )
