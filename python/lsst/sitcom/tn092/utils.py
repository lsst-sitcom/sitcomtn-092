import re
from lsst.ts.xml.enums.Script import ScriptState


__all__ = [
    "convert_script_state",
    "filter_by_block_id"
]


def convert_script_state(state):
    """
    Convert the Script state to a string.

    Parameters
    ----------
    state : int
        The Script state.

    Returns
    -------
    str
        The string representation of the Script state.
    """
    return ScriptState(state).name


def filter_by_block_id(df, block_name):
    """
    Filter a DataFrame by the block name.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to filter.
    block_name : str
        The block name to filter by.

    Returns
    -------
    pandas.DataFrame
        The filtered DataFrame.
    """
    assert "blockId" in df.columns, "The DataFrame must have a 'blockId' column."
    block_number = int(re.search(r"\d+", block_name).group())
    block_id = f"{block_number:03d}"
    temp_df = df[df.blockId.str.contains(block_id)]
    return temp_df
