import re
import os
import pandas as pd

from matplotlib import pyplot as plt
from lsst.summit.utils.efdUtils import getEfdData
from lsst.ts.idl.enums.Script import ScriptState
from lsst.summit.utils.tmaUtils import TMAState

__all__ = [
    "convert_script_state",
    "filter_by_block_id",
    "get_hp_minmax_forces",
    "query_script_configuration",
    "query_script_description",
    "query_script_states",
    "query_block_status",
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


def get_hp_minmax_forces(efd_client, tma_slew_events, event_type=TMAState.SLEWING, verbose=False):
    """
    Retrieve the minimum and maximum hardpoint measured forces during TMA
    slewing events.

    Parameters:
    efd_client : object
        The EFD client used to query data.
    tma_slew_events : list
        A list of TMA slewing events to process.
    event_type : TMAState, optional
        The type of event to filter for (default is TMAState.SLEWING).
    verbose : bool, optional
        If True, print detailed information about each event
        (default is False).

    Returns:
    pd.DataFrame
        A DataFrame containing the sequence number, azimuth difference,
        elevation difference, minimum forces, and maximum forces for each
        valid event.
    """
    df = pd.DataFrame()

    for evt in tma_slew_events:

        if evt.type != event_type:
            continue

        if evt.endReason == TMAState.FAULT:
            print(f"Event {evt.seqNum} on {evt.dayObs} faulted. Ignoring it.")
            continue

        az = query_mtmount_azimuth(efd_client, evt)
        el = query_mtmount_elevation(efd_client, evt)
        forces = query_m1m3_hp_measured_forces(efd_client, evt)

        try:
            az_diff = az.actualPosition.iloc[-1] - az.actualPosition.iloc[0]
            el_diff = el.actualPosition.iloc[-1] - el.actualPosition.iloc[0]
        except AttributeError:
            continue

        if verbose:
            print(
                f"{evt.seqNum}, "
                f"{az_diff:8.2f}, "
                f"{el_diff:8.2f}, "
                f"{forces.min().min():8.2f}, "
                f"{forces.max().max():8.2f} "
            )

        my_dict = dict(
            seq_num=evt.seqNum,
            delta_az=az_diff,
            delta_el=el_diff,
            min_forces=forces.min().min(),
            max_forces=forces.max().max(),
        )

        my_df = pd.DataFrame([my_dict])
        df = pd.concat([df, my_df], ignore_index=True)

    return df


def plot_histogram_hp_minmax_forces(df, day_obs):
    """
    Plots histograms of the minimum and maximum forces measured on hardpoints
    during slews.
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the minimum and maximum forces data. It should
        have columns 'min_forces' and 'max_forces'.
    day_obs : int or str
        The observation day identifier to be included in the plot title and
        filename.
    Returns
    -------
    None
    """
    fig, (min_ax, max_ax) = plt.subplots(figsize=(10, 5), ncols=2, sharey=True)

    min_ax.hist(
        df["min_forces"],
        ec="white",
        alpha=0.75,
        label="Minimum forces",
        log=True,
    )
    max_ax.hist(
        df["max_forces"],
        ec="white",
        alpha=0.75,
        label="Maximum forces",
        log=True,
    )

    min_ax.grid(alpha=0.3)
    min_ax.set_xlabel("Minimum measured forces on\n the hardpoints during a slew [N]")
    min_ax.set_ylabel("Number of slews")
    min_ax.axvline(-450, ls=":", c="black", alpha=0.5, label="Operational limit", lw=2)
    min_ax.axvline(-900, ls="--", c="red", alpha=0.5, label="Fatigue limit", lw=2)
    min_ax.legend()

    max_ax.grid(alpha=0.3)
    max_ax.set_xlabel("Maximum measured forces on\n the hardpoints during a slew [N]")
    # max_ax.set_ylabel("Number of slews")
    max_ax.axvline(450, ls=":", c="black", alpha=0.5, label="Operational limit", lw=2)
    max_ax.axvline(900, ls="--", c="red", alpha=0.5, label="Fatigue limit", lw=2)
    max_ax.legend()

    fig.suptitle(
        f"Histogram with the number of slews with\n"
        f"different minimum and maximum measured forces on the hardpoints.\n"
        f"DayObs {day_obs}, total of {df.index.size} slews",
    )

    os.makedirs("./plots", exist_ok=True)
    fig.tight_layout()
    fig.savefig(f"./plots/histogram_hp_minmax_dayobs_{day_obs}.png")
    plt.show()


def query_m1m3_hp_measured_forces(efd_client, tma_slew_event):
    """
    Query the EFD for the measured forces of the M1M3 component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    tma_slew_event : TMAEvent
        The TMA event for the slew.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the measured forces of the M1M3 component.
    """
    df_forces = getEfdData(
        efd_client,
        "lsst.sal.MTM1M3.hardpointActuatorData",
        columns=[f"measuredForce{i}" for i in range(6)],
        event=tma_slew_event,
    )

    return df_forces


def query_mtmount_azimuth(efd_client, tma_slew_event):
    """
    Query the EFD for the azimuth of the MTMount component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    tma_slew_event : TMAEvent
        The TMA event for the slew.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the azimuth of the MTMount component.
    """
    df_azimuth = getEfdData(
        efd_client,
        "lsst.sal.MTMount.azimuth",
        columns=["actualPosition"],
        event=tma_slew_event,
    )

    return df_azimuth


def query_mtmount_elevation(efd_client, tma_slew_event):
    """
    Query the EFD for the elevation of the MTMount component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    tma_slew_event : TMAEvent
        The TMA event for the slew.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the elevation of the MTMount component.
    """
    df_elevation = getEfdData(
        efd_client,
        "lsst.sal.MTMount.elevation",
        columns=["actualPosition"],
        event=tma_slew_event,
    )

    return df_elevation


def query_script_configuration(efd_client, start_day_obs, end_day_obs):
    """
    Query the EFD for the configuration of the Script SAL component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    start_day_obs : int
        The first day of observations to query.
    end_day_obs : int
        The last day of observations to query.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the configuration of the Script SAL component.
    """
    df_configuration = getEfdData(
        efd_client,
        "lsst.sal.Script.command_configure",
        columns="*",
        begin=start_day_obs,
        end=end_day_obs,
    )

    return df_configuration


def query_script_description(efd_client, start_day_obs, end_day_obs, block_id=None):
    """
    Query the EFD for the description of the Script SAL component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    start_day_obs : int
        The first day of observations to query.
        end_day_obs : int
        The last day of observations to query.
    block_id : str, optional
        The block ID to filter by.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the description of the Script SAL component.
    """
    df_description = getEfdData(
        efd_client,
        "lsst.sal.Script.logevent_description",
        columns="*",
        begin=start_day_obs,
        end=end_day_obs,
    )

    return df_description


def query_script_log_message(efd_client, start_day_obs, end_day_obs):
    """
    Query the EFD for the log messages of the Script SAL component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    start_day_obs : int
        The first day of observations to query.
        end_day_obs : int
        The last day of observations to query.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the log messages of the Script SAL component.
    """
    df_log_message = getEfdData(
        efd_client,
        "lsst.sal.Script.logevent_logMessage",
        columns="*",
        begin=start_day_obs,
        end=end_day_obs,
    )

    return df_log_message


def query_script_states(efd_client, start_day_obs, end_day_obs, block_id=None):
    """
    Query the EFD for the state of the Script SAL component.

    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    start_day_obs : int
        The first day of observations to query.
    end_day_obs : int
        The last day of observations to query.
    block_id : str, optional
        The block ID to filter by.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the state of the Script SAL component.
    """
    df_state = getEfdData(
        efd_client,
        "lsst.sal.Script.logevent_state",
        columns="*",
        begin=start_day_obs,
        end=end_day_obs,
    )

    if block_id is not None:
        df_state = filter_by_block_id(df_state, block_id)

    return df_state


def query_block_status(client, start_day_obs, end_day_obs, block_name):
    """
    Query the EFD for the block status.

    Parameters
    ----------
    client : EfdClient
        The EFD client to use for querying.
    start_day_obs : int
        The first day of observations to query.
    end_day_obs : int
        The last day of observations to query.
    block_name : str
        The name of the block to query.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the block status.
    """
    df_block = getEfdData(
        client,
        "lsst.sal.Scheduler.logevent_blockStatus",
        columns="*",
        begin=start_day_obs,
        end=end_day_obs,
    )
    df_block = df_block[df_block.id == block_name]
    return df_block
