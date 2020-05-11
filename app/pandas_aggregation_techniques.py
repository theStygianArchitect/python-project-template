#! /bin/env python
"""
Description: This module contains DataFrame aggregation techniques.

Title: pandas_aggregation_techniques.py

Author: theStygianArchitect
"""
import sys
from typing import Any
from typing import List
from typing import Text

try:
    import pandas
except ModuleNotFoundError as module_not_found_error:
    print(module_not_found_error)
    print('Please install required packages')
    sys.exit(1)


from logger import set_up_stream_logging


log = set_up_stream_logging()  # pylint: disable=C0103


def filter_data_where_column_eq_value(data_frame: pandas.DataFrame, column_name: Text,
                                      filter_value: Any) -> pandas.DataFrame:
    """Filter data_frame by a specific value.

    This function filters a pandas.DataFrame object by a that column
    where the column_name is equal to the filter_value.

    Args:
        data_frame(pandas.DataFrame): The DataFrame object being
            filtered.
        column_name(Text): The column that is being inspected.
        filter_value(Any): The value that column_name' value should
            equal.

    Returns:
        A tabular representation of the data filtered.

    """
    return data_frame.loc[data_frame[column_name] == filter_value]


def filter_data_where_column_neq_value(data_frame: pandas.DataFrame, column_name: Text,
                                       filter_value: Any) -> pandas.DataFrame:
    """Filter data_frame by a generic value.

    This function filters a pandas.DataFrame object by a that column
    where the column_name is not equal to the filter_value.

    Args:
        data_frame(pandas.DataFrame): The DataFrame object being
            filtered.
        column_name(Text): The column that is being inspected.
        filter_value(Any): The value that column_name's value should
            not equal.

    Returns:
        A tabular representation of the data filtered.

    """
    return data_frame.loc[data_frame[column_name] != filter_value]


def filter_data_where_column_isin_array(data_frame: pandas.DataFrame, column_name: Text,
                                        filter_array: List[Any]) -> pandas.DataFrame:
    """Filter data_frame by multiple values.

    This function filters a pandas.DataFrame object by a that column
    where the column_name's value is in filter_array.

    Args:
        data_frame(pandas.DataFrame): The DataFrame object being
            filtered.
        column_name(Text): The column that is being inspected.
        filter_array(List): The values that column_name's value should
            equal.

    Returns:
        A tabular representation of the data filtered.

    """
    return data_frame.loc[data_frame[column_name].isin(filter_array)]


def filter_data_where_column_is_not_in_array(data_frame: pandas.DataFrame, column_name: Text,
                                             filter_array: List[Any]) -> pandas.DataFrame:
    """Filter data_frame by multiple values.

    This function filters a pandas.DataFrame object by a that column
    where the column_name's value is not in filter_array.

    Args:
        data_frame(pandas.DataFrame): The DataFrame object being
            filtered.
        column_name(Text): The column that is being inspected.
        filter_array(List): The values that column_name's value should
            not equal.

    Returns:
        A tabular representation of the data filtered.

    """
    return data_frame.loc[~data_frame[column_name].isin(filter_array)]


def filter_data_by_columns(data_frame: pandas.DataFrame, columns: List) -> pandas.DataFrame:
    """Filter data_frame by columns.

    This function filters a pandas.DataFrame object to the supplied
    columns parameter.

    Args:
        data_frame(pandas.DataFrame): The DataFrame object being
            filtered.
        columns(List): The column that is being inspected.

    Returns:
        A tabular representation of the data filtered.

    """
    return data_frame[columns]
