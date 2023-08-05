"""Analysis tools"""

import os
import configparser
import argparse
import pandas as pd
import numpy as np


def input_parse():
    """
    Parse inputs

    :return: dict
        Dictionary of inputs
    """
    # Local vars
    config_inputs = configparser.ConfigParser()
    argparse_inputs = argparse.ArgumentParser()

    # Command line arguments (these get priority)
    argparse_inputs.add_argument(
        '-c',
        '--config_file',
        type=str,
        action='store',
        help='Path to configuration file',
        required=True
    )

    # Parse arguments
    argparse_inputs = argparse_inputs.parse_args()

    # Parse config file
    config_inputs.read(argparse_inputs.config_file)

    # Store inputs
    path_to_data = config_inputs['MAIN IO']['data']
    inputs = {
        'path_to_data': path_to_data,
        'path_to_6w_pae': os.path.join(
            path_to_data,
            config_inputs['INPUT']['path_to_6w_pae']
        ),
        'path_to_6w_power': os.path.join(
            path_to_data,
            config_inputs['INPUT']['path_to_6w_power']),
        'path_to_12w_pae': os.path.join(
            path_to_data,
            config_inputs['INPUT']['path_to_12w_pae']
        ),
        'path_to_12w_power': os.path.join(
            path_to_data,
            config_inputs['INPUT']['path_to_12w_power']),
        'path_to_all_objectives_viz': os.path.join(
            path_to_data,
            config_inputs['OUTPUT']['path_to_all_objectives_viz']
        ),
        'path_to_all_robust_metrics_viz': os.path.join(
            path_to_data,
            config_inputs['OUTPUT']['path_to_all_robust_metrics_viz']
        ),
        'path_to_nondom_robust_metrics_viz': os.path.join(
            path_to_data,
            config_inputs['OUTPUT']['path_to_nondom_robust_metrics_viz']
        )
    }

    return inputs


def awr_to_dataframe(
        path=None,
        df=None
):
    """
    Import awr output to DataFrame

    Parameters
    ----------
    path: str
        Path to awr file

    Returns
    -------
    df: DataFrame
        Processed dataframe in a standard format
    """
    # Import awr data
    if df is not None:
        df_awr = df
    else:
        df_awr = pd.read_csv(path, delimiter='\t')
    cols = df_awr.columns

    # Get dimension labels
    vertical_dim_label = cols[0].split(' ')[-1]
    content_label = cols[0].split(' ')[0]
    horizontal_dim_labs = []
    dimension_labs = cols[1].split(' ')
    for i, word in enumerate(dimension_labs):
        if word == '=':
            # Previous word is dimension
            horizontal_dim_labs.append(dimension_labs[i-1])

    # Transpose DataFrame to "long" form
    df_long = pd.melt(
        df_awr,
        id_vars=cols[0],
        value_vars=cols[1:],
        value_name=content_label
    )

    # Split columns
    df_split = df_long['variable'].str.split(' ', expand=True)
    for i in horizontal_dim_labs:
        # Get keyword column
        keyword_col = df_split.iloc[0] == i
        value_col = df_split.iloc[0].index[keyword_col][0] + 2
        # Add values
        df_long[i] = df_split[value_col]

    # Clean up
    df_long = df_long.rename(
        {
            cols[0]: vertical_dim_label
        },
        axis=1
    )
    df_long = df_long.drop('variable', axis=1)

    return df_long


def combine_output_single_device(df_ls):
    """
    Combine different outputs for single device

    Parameters
    ----------
    df_ls: list of DataFrames
        List of different outputs (e.g., power, PAE) DataFrames for single
        device

    Returns
    -------
    df_device: DataFrame
        DataFrame for single device
    """
    # Combine DataFrames
    df_device = pd.concat(df_ls, axis=1)

    # Remove duplicated columns
    unique_cols = ~df_device.columns.duplicated()
    df_device = df_device.loc[:, unique_cols]

    return df_device


def is_pareto_efficient(costs, return_mask=True):
    """Find the pareto-efficient points
    https://stackoverflow.com/questions/51397669/imports-inside-package-now-that-init-py-is-optional

    Parameters
    ----------
    costs : array
        An (n_points, n_costs) array
    return_mask : bool, optional
        Return index of points, by default True

    Returns
    -------
    array
        An array of indices of pareto-efficient points.
    """
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index < len(costs):
        nondominated_point_mask = np.any(
            costs < costs[next_point_index], axis=1
        )
        nondominated_point_mask[next_point_index] = True

        # Remove dominated points
        is_efficient = is_efficient[nondominated_point_mask]
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype=bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient


def get_nondomintated(df, objs, max_objs=None):
    """
    Get nondominate filtered DataFrame

    Parameters
    ----------
    df: DataFrame
        DataFrame for nondomination
    objs: list
        List of strings correspond to column names of objectives
    max_objs: list (Optional)
        List of objective to maximize

    Returns
    -------
    df_nondom: DataFrame
        Nondominatated DataFrame
    """
    # Get flip maximum objectives
    df_temp = df.copy()
    try:
        df_temp[max_objs] = -1.0*df_temp[max_objs]
    except KeyError:
        pass

    # Nondominated sorting
    # ndf, _, _, _ = pg.fast_non_dominated_sorting(df_temp[objs].values)
    # nondom_idx = ndf[0]  # First front
    nondom_idx = is_pareto_efficient(df_temp[objs].values, return_mask=False)
    df_nondom = df.iloc[nondom_idx].reset_index(drop=True)

    return df_nondom


def get_states(df, df_states, dec_labs, cast_decs=True):
    """Get states of dataframe

    Parameters
    ----------
    df : DataFrame
        DataFrame to get states
    df_states : DataFrame
        DataFrame with states
    dec_labs : list
        Decision labels
    cast_decs :  boolean
        Whether to atempt to case the decisions

    Returns
    -------
    df : DataFrame
        Original DataFrame with states
    """
    if cast_decs:
        # Cast types
        df_states[dec_labs] = df_states[dec_labs].astype(float).round(6)
        df[dec_labs] = df[dec_labs].astype(float).round(6)

    # Expand to get all states
    df = pd.merge(
        df,
        df_states,
        left_on=dec_labs,
        right_on=dec_labs,
        how='left',
        copy=False
    )

    return df


def get_native_robust_metrics(
        df,
        dec_labs,
        state_labs,
        obj_labs,
        robust_types,
):
    """
    Get native robustness metrics for each objective. For example, find the
    minimum PAE for each range of frequencies for each design

    Parameters
    ----------
    df: DataFrame
        DataFrame to perform objective calculations
    dec_labs: list
        List of strings containing columns to group over (decisions)
    state_labs: list
        List of strings containing columns of states to group over
    obj_labs: list
        List of strings containing names of columns with objective values
    robust_types: list
        list of strings containing native_function_name

    Returns
    -------
    df_grouped: DataFrame
        Grouped DataFrame of all the objective values
    """
    list_df = []

    # Melt the states
    df = df.melt(id_vars=dec_labs+obj_labs, value_vars=state_labs)
    df = df.drop(['value', 'variable'], axis=1)

    # Get initial grouping
    df_grouped = df.groupby(dec_labs)

    # Get objectives for native methods
    for function in robust_types:
        # Compute objective
        df_robust = getattr(df_grouped, function)()

        # Rename objectives
        labs = dict(zip(obj_labs, [function + '_' + s for s in obj_labs]))
        df_robust = df_robust[obj_labs].rename(labs, axis=1)

        # Store
        list_df.append(df_robust)

    # Combine into single dataframe
    df_grouped = pd.concat(list_df, axis=1)

    # Ungroup
    df_robust = df_grouped.reset_index()

    return df_robust


def combine_device_df(
        df_list: list,
        labs: list
):
    """
    Combine different device dataframes. This works for different power
    ratings or different manufacturers. Basically, different model being run
    in awr.

    Parameters
    ----------
    df_list: list
        List of dataframes to be combined
    labs: list
        Labels for each of the associated dataframes

    Returns
    -------
    df_multi_device: DataFrame
        DataFrame combining the dataframes in `df_list` with the corresponding
        labels specified in `labs`
    """
    # Add device label
    for i, df in enumerate(df_list):
        df['Device Label'] = labs[i]

    # Combine devices
    df_multi_device = pd.concat(df_list)

    # Check if columns do not overlap
    if not all([set(df_list[0].columns) == set(df.columns) for df in df_list]):
        raise ValueError(
            'Columns are different in devices trying to be combined. Check'
            'that devices can actually be merged. If so, rename columns to'
            'ensure they all have the same name'
        )

    return df_multi_device
