"""
Compute statistics that are currently not provided by MPyC
"""
from itertools import compress
from typing import List, Optional, Tuple, Union, cast

import mpyc
import numpy as np
from mpyc.runtime import mpc
from mpyc.seclists import seclist
from mpyc.sectypes import SecureFixedPoint

from tno.mpc.mpyc.statistics.utils.types import Matrix, Number, NumpyObjectArray, Vector
from tno.mpc.mpyc.statistics.utils.utils import matrix_transpose, vector_eq


def iqr_count(
    row: Vector[SecureFixedPoint],
) -> SecureFixedPoint:
    """
    Computes the interquartile range (IQR) for a given row of secret-shared values.
    The IQR is the difference between the third and first quartile.

    :param row: Row of secret shared values
    :raises ValueError: Row must be populated by at least one element.
    :return: IQR Count
    """
    if len(row) == 0:
        raise ValueError("Row must be populated by at least one element.")

    row = mpc.sorted(row)

    if len(row) % 2 == 0:
        q_1 = row[: len(row) // 2]
        q_3 = row[len(row) // 2 :]
    else:
        q_1 = row[: (len(row) + 1) // 2]
        q_3 = row[(len(row) - 1) // 2 :]

    q_1_med = _med_sorted(q_1)
    q_3_med = _med_sorted(q_3)
    iqr = mpc.sub(q_3_med, q_1_med)
    return iqr


def _med_sorted(
    sorted_row: Vector[SecureFixedPoint],
) -> SecureFixedPoint:
    """
    Computes the median of an already sorted list of secret shared values.

    :param sorted_row: Sorted row of secret shared values
    :return: Median
    """
    row_len = len(sorted_row)
    if row_len % 2 == 1:
        middle_index = int((row_len - 1) / 2)
        return sorted_row[middle_index]
    low_index = int((row_len - 2) / 2)
    high_index = low_index + 1
    return (sorted_row[low_index] + sorted_row[high_index]) / 2


async def unique_values(
    row: Vector[SecureFixedPoint],
) -> List[SecureFixedPoint]:
    """
    Returns unique values in the row.

    :param row: Row of secret shared values
    :return: Unique values
    """
    sorted_row = mpc.sorted(row)
    mask = vector_eq(sorted_row[1:], sorted_row[:-1])
    revealed_mask = [True, *map(lambda _: bool(_ - 1), await mpc.output(mask))]
    return list(compress(sorted_row, revealed_mask))


async def frequency(
    row: Vector[SecureFixedPoint],
    boolean: bool = False,
) -> Tuple[List[SecureFixedPoint], List[SecureFixedPoint]]:
    """
    Wrapper function to compute frequency, which returns
    a value list and a frequency list.

    :param row: Row of secret shared values
    :param binary: Flag to indicate whether contents of row are 0s and 1s,
        defaults to False
    :returns: Value list and a frequency list
    """
    if not boolean:
        unique_vals, frequency_table = await _freq(row)
    else:
        unique_vals, frequency_table = _bool_freq(row)

    return unique_vals, frequency_table


def _bool_freq(
    row: Vector[SecureFixedPoint],
) -> Tuple[List[SecureFixedPoint], List[SecureFixedPoint]]:
    """
    Computes frequency of elements in the boolean row.

    :param row: Row of secret shared values
    :return: Value list and a frequency list
    """
    stype = type(row[0])
    one_freq = mpc.sum(row)
    return [stype(0), stype(1)], [len(row) - one_freq, one_freq]


async def _freq(
    row: Vector[SecureFixedPoint],
) -> Tuple[List[SecureFixedPoint], List[SecureFixedPoint]]:
    """
    Computes frequency of elements in the row.

    :param row: Row of secret shared values
    :return: Value list and a frequency list
    """
    unique_vals = await unique_values(row)
    stype = type(row[0])
    frequency_table = [stype(0) for _ in range(len(unique_vals))]
    for i, label in enumerate(unique_vals):
        for label_2 in row:
            cond1 = mpc.eq(label, label_2)
            frequency_table[i] = mpc.add(frequency_table[i], cond1)
    return unique_vals, frequency_table


def covariance(
    row_1: Vector[SecureFixedPoint], row_2: Vector[SecureFixedPoint]
) -> SecureFixedPoint:
    """
    Calculates covariance by calling covariance_matrix
    and returning element [0][1] as it represents the
    covariance of these two rows

    :param row_1: Row of secret shared variables
    :param row_2: Row of secret shared variables
    :return: Covariance
    """
    return covariance_matrix([row_1, row_2])[0][1]


def covariance_matrix(
    matrix: Matrix[SecureFixedPoint],
) -> Matrix[SecureFixedPoint]:
    """
    Computes a covariance matrix.
    Uses numpy's implementation of the covariance matrix, which can be found:
    https://github.com/numpy/numpy/blob/v1.22.0/numpy/lib/function_base.py#L2462-L2681

    :param matrix: Matrix of secret shared values
    :raises ValueError: Matrix has more than two dimensions
    :raises ValueError: Empty matrix received
    :raises TypeError: Secure fixed-point or integer type required
    :return: Covariance matrix
    """
    if len(np.array(matrix).shape) > 2:
        raise ValueError("Matrix has more than two dimensions.")
    if len(matrix[0]) == 0:
        raise ValueError("Empty matrix received.")
    if not issubclass(type(matrix[0][0]), SecureFixedPoint):
        raise TypeError("Secure fixed-point or integer type required.")

    avg = []
    for row in matrix:
        mean_result = [mpyc.statistics.mean(row) for _ in range(0, len(row))]
        avg.append(mean_result)

    # normalisation factor
    fact = len(matrix[0]) - 1
    matrix = mpc.matrix_sub(matrix, avg)
    cov = mpc.matrix_prod(matrix, matrix_transpose(matrix))

    for i, _ in enumerate(cov):
        for j, _ in enumerate(cov[i]):
            cov[i][j] /= fact

    return cov


def correlation(
    row_1: Vector[SecureFixedPoint],
    row_2: Vector[SecureFixedPoint],
    sdev_c1: Optional[float] = None,
    sdev_c2: Optional[float] = None,
) -> SecureFixedPoint:
    r"""
    Returns secure Pearson correlation coefficient between
    row_1 and row_2. Cannot mix public and private standard deviations.

    This is normally done as so:

    .. math:: \\rho(X,Y) = \\frac{cov_{X,Y}}{\\sigma_X \\sigma_Y} }

    :param row_1: Row of secret shared variables
    :param row_2: Row of secret shared variables
    :param sdev_c1: Either a public standard deviation of row_1 or None
        which indicates that the public standard deviation of row_1 need
        to be computed, or a secret shared standard deviation
    :param sdev_c2: Either a public standard deviation of row_2 or None
        which indicates that the public standard deviation of row_2 need
        to be computed, or a secret shared standard deviation
    :raises ValueError: Row 1 and 2 are of different sizes
    :raises ValueError: Covariance requires at least two data points
    :return: Secure correlation coefficient
    """
    if np.array(row_1).shape != np.array(row_2).shape:
        raise ValueError("Row 1 and 2 are of different sizes.")
    if len(row_1) < 2 or len(row_2) < 2:
        raise ValueError("Covariance requires at least two data points.")
    if (sdev_c1 is None and sdev_c2 is not None) or (
        sdev_c2 is None and sdev_c1 is not None
    ):
        raise ValueError("Cannot mix public and private standard deviations.")
    mpc_flag = sdev_c1 is None or sdev_c2 is None

    if mpc_flag:
        corr = _corr_secret_sdev(row_1, row_2)
    else:
        corr = _corr_real_sdev(row_1, row_2, cast(float, sdev_c1), cast(float, sdev_c2))
    return corr


def _corr_secret_sdev(
    row_1: Vector[SecureFixedPoint],
    row_2: Vector[SecureFixedPoint],
) -> SecureFixedPoint:
    """
    Computes secure Pearson's correlation coefficient between
    row_1 and row_2.

    :param row_1: Row of secret shared variables
    :param row_2: Row of secret shared variables
    :return: Secure Pearson's Correlation Coefficient
    """
    sdev_c1 = mpyc.statistics.stdev(row_1)
    sdev_c2 = mpyc.statistics.stdev(row_2)
    cov = covariance(row_1, row_2)
    sdev_mul = mpc.mul(sdev_c1, sdev_c2)
    corr: SecureFixedPoint = mpc.div(cov, sdev_mul)
    return corr


def _corr_real_sdev(
    row_1: Vector[SecureFixedPoint],
    row_2: Vector[SecureFixedPoint],
    sdev_c1: Union[Number, SecureFixedPoint],
    sdev_c2: Union[Number, SecureFixedPoint],
) -> SecureFixedPoint:
    """
    Computes secure Pearson's correlation coefficient between
    row_1 and row_2.

    :param row_1: Row of secret shared variables
    :param row_2: Row of secret shared variables
    :param sdev_c1: Public standard deviation of row_1
    :param sdev_c2: Public standard deviation of row_2
    :return: Secure Pearson's Correlation Coefficient
    """

    cov = covariance(row_1, row_2)
    sdev_mul = sdev_c1 * sdev_c2
    corr = cov / sdev_mul
    return corr


def correlation_matrix(
    matrix: Matrix[SecureFixedPoint],
    std_devs: Optional[List[float]] = None,
) -> Matrix[SecureFixedPoint]:
    """
    Computes a correlation matrix.
    Uses numpy's implementation of the correlation matrix, which can be found:
    https://github.com/numpy/numpy/blob/v1.22.0/numpy/lib/function_base.py#L2689-L2839

    :param matrix: Matrix of secret shared values
    :param std_devs: List of public standard deviations
    :return: Covariance matrix
    """
    cov: NumpyObjectArray = np.array(covariance_matrix(matrix))
    standard_devs_public: List[SecureFixedPoint] = []
    if std_devs is None:
        # diagonalising the matrix to get the standard deviations
        diag_cov: NumpyObjectArray = np.diag(cov)
        standard_devs_public = [mpyc.statistics._fsqrt(elem) for elem in diag_cov]
        standard_devs_to_div: NumpyObjectArray = np.array(standard_devs_public)
    else:
        standard_devs_to_div: NumpyObjectArray = np.array(std_devs)  # type: ignore[no-redef]

    cov /= standard_devs_to_div[:, None]
    cov /= standard_devs_to_div[None, :]

    # just renaming for readability
    corr: List[List[SecureFixedPoint]] = cov.tolist()

    return corr


async def contingency_table(
    labels_actual: Vector[SecureFixedPoint],
    labels_prediction: Union[
        Vector[SecureFixedPoint], Vector[Vector[SecureFixedPoint]]
    ],
    binary: bool = True,
) -> Union[
    Matrix[SecureFixedPoint],
    Tuple[List[SecureFixedPoint], List[SecureFixedPoint], Matrix[SecureFixedPoint]],
]:
    """
    Computes either:

        1. A binary 2d-contingency table
        2. A binary n-dimensional table
        3. A non-binary 2d-contingency table

    :param labels_actual: The truth class labels
    :param labels_prediction: The prediction labels to evaluate
    :param binary: Flag to indicate whether contents of labels are 0s and 1s,
        defaults to True
    :raises ValueError: For n-dimensional contingency tables, only binary is supported
    :raises ValueError: Rows must be populated by at least one element
    :raises ValueError: Rows are of different sizes
    :return: If computing a non-binary table, he row labels (truth class), the column
        labels (prediction class) and a list containing the rows of the contingency
        table. If computing a binary table, only the rows of the table are returned
        as the row and column labels are just 0 and 1.
    """
    is_iter = hasattr(labels_prediction[0], "__iter__")

    if not binary and is_iter:
        raise ValueError(
            "For n-dimensional contingency tables, only binary is supported."
        )
    if len(labels_actual) == 0:
        raise ValueError("Rows must be populated by at least one element.")
    if not is_iter:
        if np.array(labels_actual).shape != np.array(labels_prediction).shape:
            raise ValueError(
                f"Rows are of different sizes: {np.array(labels_actual).shape} for labels_actual and {np.array(labels_actual).shape} for labels_predicted."
            )
    else:
        for lp in labels_prediction:
            if np.array(labels_actual).shape != np.array(lp).shape:
                raise ValueError(
                    f"Rows are of different sizes: {np.array(labels_actual).shape} for labels_actual and {np.array(lp).shape} for labels_predicted."
                )

    if binary and is_iter:
        return await _bin_cont_table_ndim(
            labels_actual,
            cast(Vector[Vector[SecureFixedPoint]], labels_prediction),
        )
    elif binary and not is_iter:
        return await _bin_cont_table(
            labels_actual, cast(Vector[SecureFixedPoint], labels_prediction)
        )
    else:
        return await _cont_table(
            labels_actual, cast(Vector[SecureFixedPoint], labels_prediction)
        )


async def _bin_cont_table(
    labels_actual: Vector[SecureFixedPoint],
    labels_prediction: Vector[SecureFixedPoint],
) -> Matrix[SecureFixedPoint]:
    """
    Computes a 2d contingency table from labels only containing 0 and 1.
    We know the labels are 0 and 1, so not returning it.

    :param labels_actual: The truth class labels
    :param labels_prediction: The prediction labels to evaluate
    :return: The row labels, the column labels and a list containing
            the rows of the contingency table
    """
    stype = type(labels_actual[0])

    table = seclist([0, 0, 0, 0], stype)  # type: ignore[no-untyped-call]

    for la, lp in zip(labels_actual, labels_prediction):
        index = mpc.add(la * 2, lp)
        index.integral = True
        table[index] += 1

    ret_table = [[table[0], table[1]], [table[2], table[3]]]
    return ret_table


async def _bin_cont_table_ndim(
    labels_actual: Vector[SecureFixedPoint],
    labels_predictions: Vector[Vector[SecureFixedPoint]],
) -> Matrix[SecureFixedPoint]:
    """
    Computes an n-dim contingency table from labels only containing 0 and 1.
    We know the labels are 0 and 1, so not returning it.

    :param labels_actual: The truth class labels
    :param labels_predictions: The prediction labels to evaluate
    :return: The row labels, the column labels and a list containing
            the rows of the contingency table
    """
    stype = type(labels_actual[0])
    dimensions = 2 ** (len(labels_predictions))
    table = seclist([0] * 2 * dimensions, stype)  # type: ignore[no-untyped-call]
    for i, la in enumerate(labels_actual):
        index_list = [la * dimensions]
        for j, l in enumerate(labels_predictions):
            scaler = 2 ** (len(labels_predictions) - (j + 1))
            index_list.append(scaler * l[i])
        index = mpc.sum(index_list)
        index.integral = True
        table[index] += 1

    ret_table = [
        [table[e] for e in range(0, dimensions)],
        [table[e] for e in range(dimensions, 2 * dimensions)],
    ]
    return ret_table


async def _cont_table(
    labels_actual: Vector[SecureFixedPoint],
    labels_prediction: Vector[SecureFixedPoint],
) -> Tuple[List[SecureFixedPoint], List[SecureFixedPoint], Matrix[SecureFixedPoint]]:
    """
    Computes a two-dimensional non-binary contingency table.

    :param labels_actual: The truth class labels
    :param labels_prediction: The prediction labels to evaluate
    :return: The row labels, the column labels and a list containing
            the rows of the contingency table
    """
    stype = type(labels_actual[0])

    unique_actual = await unique_values(labels_actual)
    unique_pred = await unique_values(labels_prediction)

    table = [
        [stype(0) for _ in range(len(unique_pred))] for i in range(len(unique_actual))
    ]
    for i, label in enumerate(unique_actual):
        for j, label_2 in enumerate(unique_pred):
            for x in zip(labels_actual, labels_prediction):
                cond1 = mpc.eq(label, x[0])
                cond2 = mpc.eq(label_2, x[1])
                one_or_zero = mpc.mul(cond1, cond2)
                table[i][j] = mpc.add(table[i][j], one_or_zero)

    return unique_pred, unique_actual, table
