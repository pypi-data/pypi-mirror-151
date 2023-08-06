"""
Tests the statistics
"""
import sys
from math import isclose
from typing import Any, List, cast

import numpy as np
import pandas as pd  # type: ignore
import pytest
from mpyc.runtime import mpc
from mpyc.sectypes import SecureFixedPoint
from numpy import dtype, ndarray, signedinteger

from tno.mpc.mpyc.statistics import (
    contingency_table,
    correlation,
    correlation_matrix,
    covariance,
    covariance_matrix,
    frequency,
    iqr_count,
    unique_values,
)
from tno.mpc.mpyc.statistics.utils.types import Matrix, NumpyNumberArray, Vector

secfloat = mpc.SecFxp()
TOL_PERC = 0.15


def _off_by_percentage(
    expected_value: float,
    actual_value: float,
    decimal_percentage: float = TOL_PERC,
) -> bool:
    """
    Returns whether the expected value differs from the actual value by a
    certain percentage. If actual value is 0, then a default tolerance
    of 1e-3 is used.

    :param expected_value: Expected value
    :param actual_value: Actual value
    :param decimal_percentage: Decimal percentage of tolerance
    :return: If expected value differs from the actual value by a
        certain percentage, defaults to 0.05 (5%)
    """
    if actual_value != 0.0:
        return abs(expected_value - actual_value) / actual_value <= decimal_percentage
    return isclose(expected_value, actual_value, abs_tol=1e-3)


def _off_by_percentage_vector(
    expected_vector: Vector[float],
    actual_vector: Vector[float],
    decimal_percentage: float = TOL_PERC,
) -> bool:
    """
    Returns whether the expected vector's elements differ from the
    actual vector's elements  by a certain percentage. If actual value
     is 0, then a default tolerance of 1e-3 is used.

    :param expected_vector: Expected vector
    :param actual_vector: Actual vector
    :param decimal_percentage: Decimal percentage of tolerance
    :return: If expected value differs from the actual value by a
        certain percentage, defaults to 0.05 (5%)
    """
    return all(
        [
            _off_by_percentage(i, j, decimal_percentage=decimal_percentage)
            for i, j in zip(expected_vector, actual_vector)
        ]
    )


def _off_by_percentage_matrix(
    expected_matrix: Matrix[float],
    actual_matrix: Matrix[float],
    decimal_percentage: float = TOL_PERC,
) -> bool:
    """
    Returns whether the expected matrix's elements differ from the
    actual matrix's elements  by a certain percentage. If actual value
     is 0, then a default tolerance of 1e-3 is used.

    :param expected_matrix: Expected matrix
    :param actual_matrix: Actual matrix
    :param decimal_percentage: Decimal percentage of tolerance
    :return: If expected value differs from the actual value by a
        certain percentage, defaults to 0.05 (5%)
    """

    return all(
        [
            _off_by_percentage_vector(i, j, decimal_percentage=decimal_percentage)
            for i, j in zip(expected_matrix, actual_matrix)
        ]
    )


async def _reveal_matrix(mat: Matrix[SecureFixedPoint]) -> Matrix[float]:
    """
    Reveals matrix

    :param mat: Secret-shared matrix
    :returns: Revealed matrix
    """
    return [await mpc.output(i) for i in mat]


def np_contingency_table(
    row: NumpyNumberArray, cols: NumpyNumberArray
) -> NumpyNumberArray:
    """
    Returns (binary) contingency table

    :param row: Truth label
    :cols: Prediction label(s)
    :return: Contingency table
    """
    crosstab = pd.crosstab(index=row, columns=cols, dropna=False)
    return crosstab.to_numpy()  # type: ignore[no-any-return]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
        [1.0, 1.0, 1.0, 1.0],
        [2.2, 3.11, -4.01, 5.11],
    ],
)
async def test_unique_values(values: List[float]) -> None:
    """
    Test unique values

    :param values: Values for the test
    """
    secure_values = [secfloat(_) for _ in values]

    secure_unique = await unique_values(secure_values)
    revealed_unique_unsorted = await mpc.output(secure_unique)

    correct = list(set(values))
    revealed_unique = list(set(revealed_unique_unsorted))
    assert _off_by_percentage_vector(revealed_unique, correct)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [1.0, 1.0, 1.0, 1.0],
        [2.95, 3.1, 40.2, 5.05, 2],
    ],
)
async def test_iqr_count(values: List[float]) -> None:
    """
    Test IQR count

    :param values: Values for the test
    """

    secure_values = [secfloat(_) for _ in values]

    secure_iqr = iqr_count(secure_values)
    revealed_iqr = await mpc.output(secure_iqr)

    q_1 = np.percentile(values, 25, interpolation="midpoint")  # type: ignore[call-overload]
    q_3 = np.percentile(values, 75, interpolation="midpoint")  # type: ignore[call-overload]
    correct = q_3 - q_1
    assert _off_by_percentage(correct, revealed_iqr, decimal_percentage=0.01)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [],
    ],
)
async def test_iqr_count_corner_case(values: List[float]) -> None:
    with pytest.raises(ValueError):
        _ = iqr_count(values)  # type: ignore[arg-type]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
        [1.0, 1.0, 1.0, 1.0],
        [2.2, 3.11, -4.01, 5.111211],
    ],
)
async def test_frequency(values: List[float]) -> None:
    """
    Tests the frequency statistics

    :param values: Values for the test
    """
    secure_values = [secfloat(_) for _ in values]

    secure_elements_unordered, secure_freq_unordered = await frequency(secure_values)

    revealed_elements_unordered = await mpc.output(secure_elements_unordered)
    revealed_freq_unordered = await mpc.output(secure_freq_unordered)

    revealed_elements = list(set(revealed_elements_unordered))
    revealed_freq = list(set(revealed_freq_unordered))

    correct_array_1: ndarray[Any, dtype[signedinteger[Any]]]
    correct_array_2: ndarray[Any, dtype[signedinteger[Any]]]

    correct_array_1, correct_array_2 = np.unique(values, return_counts=True)
    correct_elements = list(set(correct_array_1))
    correct_freq = list(set(correct_array_2))

    assert _off_by_percentage_vector(
        correct_elements, revealed_elements, decimal_percentage=0.001
    ) and _off_by_percentage_vector(
        correct_freq, revealed_freq, decimal_percentage=0.001
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0],
        [1.0, 1.0, 1.0, 0.0],
    ],
)
async def test_boolean_frequency(values: List[float]) -> None:
    """
    Tests the boolean statistics

    :param values: Values for the test
    """
    secure_values = [secfloat(_) for _ in values]

    secure_elements_unordered, secure_freq_unordered = await frequency(
        secure_values, boolean=True
    )

    revealed_elements_unordered = await mpc.output(secure_elements_unordered)
    revealed_freq_unordered = await mpc.output(secure_freq_unordered)

    revealed_elements = list(set(revealed_elements_unordered))
    revealed_freq = list(set(revealed_freq_unordered))

    correct_array_1: ndarray[Any, dtype[signedinteger[Any]]]
    correct_array_2: ndarray[Any, dtype[signedinteger[Any]]]

    correct_array_1, correct_array_2 = np.unique(values, return_counts=True)
    correct_elements = list(set(correct_array_1))
    correct_freq = list(set(correct_array_2))

    assert sorted(correct_elements) == sorted(revealed_elements) and sorted(
        correct_freq
    ) == sorted(revealed_freq)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values_0",
    [
        [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
        [1.2, 1.91, 1.2, 1.0, 22.1, -111.9, 2.2],
        [2.0, 3.0, 4.0, -5.0, 1.0, 2.0, 2.1],
    ],
)
@pytest.mark.parametrize(
    "values_1",
    [
        [2.0, 11.0, -9.0, 0.1, 8.0, 2.0, 2.1],
        [2.0, 11.09, 9.11, 0.92, 2.1, 55.3, 213.2],
        [2.0, 11.0, 9.0, 0.0, 1.0, 0.2, -1.0],
    ],
)
async def test_covariance(values_0: List[float], values_1: List[float]) -> None:
    """
    Test covariance

    :param values_0: First list of values for the test
    :param values_1: Second list of values for the test
    """
    secure_values_0 = [secfloat(_) for _ in values_0]
    secure_values_1 = [secfloat(_) for _ in values_1]

    secure_cov = covariance(secure_values_0, secure_values_1)
    revealed_cov = await mpc.output(secure_cov)

    correct = np.cov(values_0, values_1)[0][1]
    assert _off_by_percentage(correct, revealed_cov, 0.005)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [
                [secfloat(1), secfloat(2)],
                [secfloat(1), secfloat(2)],
            ],
            [
                [secfloat(1), secfloat(2)],
                [secfloat(1), secfloat(2)],
            ],
        ],
        [
            [],
            [],
        ],
        [
            [1, 2],
            [1, 2],
        ],
    ],
)
async def test_covariance_matrix_corner_cases(values: Matrix[float]) -> None:
    """
    Test if the exceptions raised in the covariance matrix work

    :param values: Values for the test
    """
    with pytest.raises((ValueError, TypeError)):
        _ = covariance_matrix(values)  # type: ignore[arg-type]


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
async def test_covariance_matrix_private_stdevs(values: Matrix[float]) -> None:
    """
    Test covariance matrix with private standard deviations

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]
    secure_cov = covariance_matrix(secure_values)
    revealed_cov = await _reveal_matrix(secure_cov)

    correct = np.cov(values)

    assert _off_by_percentage_matrix(
        correct.tolist(), revealed_cov, decimal_percentage=0.005
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [2.0, 2.1, 44.2, 91.9, 22.1, 1.1, 0.0],
            [9.1, 5.13, 4.2, 1.9, 2.22, -1.1, 1.3],
        ],
    ],
)
async def test_covariance_matrix_public_stdevs(values: Matrix[float]) -> None:
    """
    Test covariance matrix with public standard deviations

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]

    secure_cov = covariance_matrix(secure_values)
    revealed_cov = await _reveal_matrix(secure_cov)

    correct = np.cov(values)

    assert _off_by_percentage_matrix(
        correct.tolist(), revealed_cov, decimal_percentage=0.05
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values_0",
    [
        [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
        [1.2, 1.91, 1.2, 1.0, 22.1, -111.9, 2.2],
        [2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 2.1],
    ],
)
@pytest.mark.parametrize(
    "values_1",
    [
        [2.0, 11.0, 9.0, 0.1, 8.0, 2.0, 2.1],
        [2.0, 11.09, 9.11, 0.92, 2.1, 55.3, 213.2],
        [2.0, 11.0, 9.0, 0.0, 1.0, 0.2, -1.0],
    ],
)
async def test_correlation_private_stdevs(
    values_0: List[float], values_1: List[float]
) -> None:
    """
    Test for correlation ooefficient with private standard deviations

    :param values_0: First list of values for the test
    :param values_1: Second list of values for the test
    """
    secure_values_0 = [secfloat(_) for _ in values_0]
    secure_values_1 = [secfloat(_) for _ in values_1]

    secure_corr = correlation(secure_values_0, secure_values_1)
    revealed_corr = await mpc.output(secure_corr)

    correct = np.corrcoef(values_0, values_1)[1][0]

    assert _off_by_percentage(correct, revealed_corr, 0.005)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values_0",
    [
        [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
        [1.2, 1.91, 1.2, 1.0, 22.1, -111.9, 2.2],
        [2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 2.1],
    ],
)
@pytest.mark.parametrize(
    "values_1",
    [
        [2.0, 11.0, 9.0, 0.1, 8.0, 2.0, 2.1],
        [2.0, 11.09, 9.11, 0.92, 2.1, 55.3, 213.2],
        [2.0, 11.0, 9.0, 0.0, 1.0, 0.2, -1.0],
    ],
)
async def test_correlation_public_stdevs(
    values_0: List[float], values_1: List[float]
) -> None:
    """
    Test for correlation ooefficient with private standard deviations

    :param values_0: First list of values for the test
    :param values_1: Second list of values for the test
    """
    sdev_c1 = np.std(values_0)
    sdev_c2 = np.std(values_1)
    secure_values_0 = [secfloat(_) for _ in values_0]
    secure_values_1 = [secfloat(_) for _ in values_1]

    secure_corr = correlation(
        secure_values_0, secure_values_1, sdev_c1=sdev_c1, sdev_c2=sdev_c2
    )
    revealed_corr = await mpc.output(secure_corr)

    correct = np.corrcoef(values_0, values_1)[1][0]

    assert _off_by_percentage(correct, revealed_corr)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [2.0, 11.09, 9.11, 0.92, 2.1, 55.3, 21.3, 99],
        ],
        [
            [1.0],
            [1.0, 2.0],
        ],
        [
            [[1.0, 2.0], [1.0, 2.0]],
            [1.0, 2.0],
        ],
        [
            [secfloat(1)],
            [secfloat(1)],
        ],
        [
            [secfloat(1), secfloat(1)],
            [secfloat(1), secfloat(1)],
        ],
    ],
)
async def test_correlation_corner_cases(values: List[float]) -> None:
    """
    Test correlation corner cases

    :param values: Values for the test
    """
    with pytest.raises(ValueError):
        _ = correlation(values[0], values[1], sdev_c1=1)  # type: ignore[arg-type]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [1.2, 1.91, 1.2, 1.0, 22.1, -111.9, 2.2],
            [2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 2.1],
        ],
    ],
)
async def test_correlation_matrix_private_stdevs(values: Matrix[float]) -> None:
    """
    Test for correlation matrix with private standard deviations

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]
    secure_corr = correlation_matrix(secure_values)
    revealed_corr = await _reveal_matrix(secure_corr)

    correct = np.corrcoef(values)

    assert _off_by_percentage_matrix(
        correct.tolist(), revealed_corr, decimal_percentage=0.01
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 6.0, 3.0],
            [2.0, 2.1, 44.2, 91.9, 22.1, 1.1, 0.0],
            [9.1, 5.13, 4.2, 1.9, 2.22, -1.1, 1.3],
        ],
    ],
)
async def test_correlation_matrix_public_stdevs(values: Matrix[float]) -> None:
    """
    Test for correlation matrix with public standard deviations

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]

    std_devs = [np.std(i) for i in values]
    secure_corr = correlation_matrix(secure_values, std_devs=std_devs)
    revealed_corr = await _reveal_matrix(secure_corr)

    correct = np.corrcoef(values)

    assert _off_by_percentage_matrix(correct.tolist(), revealed_corr)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 0.0, 3.0],
            [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
        ],
    ],
)
async def test_contingency_table(values: Matrix[float]) -> None:
    """
    Test two dimensional non-boolean contingency table

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]

    # No need to test the unique labels as it uses unique_values, which has been tested
    _, _, secure_contingency_table = await contingency_table(
        secure_values[0], secure_values[1], binary=False
    )

    revealed_contingency_table_elements = await _reveal_matrix(
        cast(List[List[SecureFixedPoint]], secure_contingency_table)
    )

    correct_contingency_table_elements = np_contingency_table(
        np.array(values[0]), np.array(values[1])
    )

    assert _off_by_percentage_matrix(
        correct_contingency_table_elements.tolist(),
        revealed_contingency_table_elements,
        decimal_percentage=0.0,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 0.0, 3.0],
            [
                [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
                [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
            ],
        ],
        [
            [0.0, 3.0, 2.0, 1.0, 5.0, 0.0, 3.0],
            [
                [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
                [1.0, 2.1, 2.0, 1.0, 22.1, 1.1],
            ],
        ],
        [
            [],
            [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
        ],
        [
            [1.0, 3.0, 2.0, 1.0, 5.0, 3.0],
            [1.0, 2.1, 2.0, 1.0, 22.1, 1.1, 0.0],
        ],
    ],
)
async def test_contingency_table_corner_cases(values: Matrix[float]) -> None:
    """
    Test corner cases for contingency tables

    :param values: Values for the test
    """
    with pytest.raises(ValueError):
        binary = False
        if values[1][0] == 0.0:  # random value
            binary = True
        # No need for converting values to sectypes, this should fail!
        _, _, _ = await contingency_table(
            values[0], values[1], binary=binary  # type: ignore[arg-type]
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [
            [1.0, 0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0, 1.0],
        ],
    ],
)
async def test_binary_contingency_table(values: Matrix[float]) -> None:
    """
    Test two dimensional boolean contingency table

    :param values: Values for the test
    """
    secure_values = [[secfloat(_) for _ in i] for i in values]

    # No need to test the unique labels as it uses unique_values, which has been
    # tested
    secure_contingency_table = await contingency_table(
        secure_values[0], secure_values[1], binary=True
    )

    revealed_contingency_table_elements = await _reveal_matrix(
        cast(List[List[SecureFixedPoint]], secure_contingency_table)
    )

    correct_contingency_table_elements = np_contingency_table(
        np.array(values[0]), np.array(values[1])
    )

    assert _off_by_percentage_matrix(
        correct_contingency_table_elements.tolist(),
        revealed_contingency_table_elements,
        decimal_percentage=0.0,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    [
        [1.0, 0.0, 1.0, 1.0],
    ],
)
@pytest.mark.parametrize(
    "values_2d",
    [
        [
            [1.0, 0.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 1.0],
        ]
    ],
)
@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
async def test_binary_contingency_table_3_dim(
    values: List[float],
    values_2d: Matrix[float],
) -> None:
    """
    Test three dimensional boolean contingency table

    Note that building a 3d contingency table requires
    Python 3.8+.

    :param values: First list of values for the test
    :param values_2d: Second list of values for the test
    """
    secure_values_actual = [secfloat(_) for _ in values]
    secure_values_pred = [[secfloat(_) for _ in i] for i in values_2d]

    # No need to test the unique labels as it uses unique_values, which has been
    # tested
    secure_contingency_table = await contingency_table(
        secure_values_actual, secure_values_pred, binary=True
    )

    revealed_contingency_table_elements = [
        await _reveal_matrix(cast(List[List[SecureFixedPoint]], i))
        for i in secure_contingency_table
    ]

    correct_contingency_table_elements = np_contingency_table(
        np.array(values), np.array(values_2d)
    )

    assert _off_by_percentage_matrix(
        correct_contingency_table_elements.tolist(),
        cast(List[List[float]], revealed_contingency_table_elements),
        decimal_percentage=0.0,
    )
