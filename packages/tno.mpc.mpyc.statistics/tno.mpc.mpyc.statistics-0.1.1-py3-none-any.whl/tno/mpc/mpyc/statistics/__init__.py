"""
Initialization of the statistics package
"""
import sys

# Make sphinx happy (name collisions between mpyc.statistics, statistics and tno.mpc.mpyc.statistics)

if "sphinx.cmd.build" not in sys.modules:
    # Explicit re-export of all functionalities, such that they can be imported properly. Following
    # https://www.python.org/dev/peps/pep-0484/#stub-files and
    # https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
    from mpyc.statistics import mean as mean
    from mpyc.statistics import median as median
    from mpyc.statistics import stdev as stdev

    from .statistics import contingency_table as contingency_table
    from .statistics import correlation as correlation
    from .statistics import correlation_matrix as correlation_matrix
    from .statistics import covariance as covariance
    from .statistics import covariance_matrix as covariance_matrix
    from .statistics import frequency as frequency
    from .statistics import iqr_count as iqr_count
    from .statistics import unique_values as unique_values
else:

    class LinearRegression:
        pass


__version__ = "0.1.1"
