import asyncio
import pandas as pd

from lsst.summit.utils.efdUtils import getEfdData
from lsst.summit.utils.tmaUtils import TMAState

from lsst.sitcom.tn092.utils import filter_by_block_id


__all__ = [
    "get_hp_minmax_forces",
    "script_configuration",
    "script_description",
    "script_states",
    "block_status",
]


def get_hp_minmax_forces(efd_client, tma_slew_events, event_type=TMAState.SLEWING):
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
    
    # Create a list of tasks to run concurrently
    tasks = [
        hp_forces_and_azimuth_elevation_per_event(efd_client, evt, event_type)
        for evt in tma_slew_events
    ]
    
    # Run all tasks concurrently and gather results
    loop = asyncio.get_event_loop()
    df_list = loop.run_until_complete(asyncio.gather(*tasks))
    df_list = [df for df in df_list if not df.isnull().any().any()]
    
    # Concatenate all DataFrames into one
    df = pd.concat(df_list, ignore_index=True)
        
    return df


async def hp_forces_and_azimuth_elevation_per_event(client, evt, event_type):
    """
    Retrieve the azimuth, elevation, and minimum/maximum forces for a
    specific TMA event.
    
    Parameters
    ----------
    client : EfdClient
        The EFD client to use for querying.
    evt : TMAEvent
        The TMA event to process.
    event_type : TMAState
        The type of event to filter for (e.g., TMAState.SLEWING).
    verbose : bool, optional
        If True, print detailed information about the event (default is False).
    
    Returns
    -------
    pd.DataFrame
        A DataFrame containing the azimuth, elevation, and forces data for the event.
    """
    if evt.type != event_type:
        return pd.DataFrame()

    if evt.endReason == TMAState.FAULT:
        print(f"Event {evt.seqNum} on {evt.dayObs} faulted. Ignoring it.")
        return pd.DataFrame()

    az = await mtmount_azimuth(client, evt)
    el = await mtmount_elevation(client, evt)
    forces = await m1m3_hp_minmax_measured_forces(client, evt)
    
    df = pd.concat([az, el, forces], axis=1)
    df["begin"] = evt.begin.isot
    df["end"] = evt.end.isot
    df["seq_num"] = evt.seqNum
    df["day_obs"] = evt.dayObs
    
    return df


async def m1m3_hp_minmax_measured_forces(efd_client, tma_slew_event):
    """
    Query the EFD for the minimum and maximum measured forces on the M1M3 hardpoints
    during a TMA slew event.
    
    Parameters
    ----------
    efd_client : EfdClient
        The EFD client to use for querying.
    tma_slew_event : TMAEvent
        The TMA event for the slew.
        
    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the minimum and maximum measured forces on the hardpoints.
    """

    # Create que query string
    query = f"""
        SELECT
            MIN(measuredForce0) AS min_forces_0,
            MAX(measuredForce0) AS max_forces_0,
            MIN(measuredForce1) AS min_forces_1,
            MAX(measuredForce1) AS max_forces_1,
            MIN(measuredForce2) AS min_forces_2,
            MAX(measuredForce2) AS max_forces_2,
            MIN(measuredForce3) AS min_forces_3,
            MAX(measuredForce3) AS max_forces_3,
            MIN(measuredForce4) AS min_forces_4,
            MAX(measuredForce4) AS max_forces_4,
            MIN(measuredForce5) AS min_forces_5,
            MAX(measuredForce5) AS max_forces_5
        FROM "lsst.sal.MTM1M3.hardpointActuatorData"
        WHERE time >= '{tma_slew_event.begin.isot}Z'
        AND time < '{tma_slew_event.end.isot}Z'
    """
    
    # Execute the query
    df_forces = await efd_client.influx_client.query(query)
    
    if pd.DataFrame(df_forces).empty:
        df_forces = pd.DataFrame(
            columns=[
                "min_forces_0", "max_forces_0",
                "min_forces_1", "max_forces_1",
                "min_forces_2", "max_forces_2",
                "min_forces_3", "max_forces_3",
                "min_forces_4", "max_forces_4",
                "min_forces_5", "max_forces_5",
                "min_forces", "max_forces"
            ],
            data=[[None] * 14]
        )
    else:
        df_forces["min_forces"] = df_forces.filter(like="min_forces").min(axis=1)
        df_forces["max_forces"] = df_forces.filter(like="max_forces").max(axis=1)

    return df_forces


def m1m3_hp_measured_forces(efd_client, tma_slew_event):
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


async def mtmount_azimuth(efd_client, tma_slew_event):
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
    query = f"""
        SELECT
            FIRST(actualPosition) AS az_start,
            LAST(actualPosition) AS az_end
        FROM "lsst.sal.MTMount.azimuth"
        WHERE time >= '{tma_slew_event.begin.isot}Z'
        AND time < '{tma_slew_event.end.isot}Z'
    """
    
    df_azimuth = await efd_client.influx_client.query(query)
    
    if pd.DataFrame(df_azimuth).empty:
        return pd.DataFrame(
            columns=["az_start", "az_end", "az_diff"],
            data=[[None, None, None]]
        )
    else:
        df_azimuth["az_diff"] = df_azimuth["az_end"] - df_azimuth["az_start"]

    return df_azimuth


async def mtmount_elevation(efd_client, tma_slew_event):
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

    query = f"""
        SELECT
            FIRST(actualPosition) AS el_start,
            LAST(actualPosition) AS el_end
        FROM "lsst.sal.MTMount.elevation"
        WHERE time >= '{tma_slew_event.begin.isot}Z'
        AND time < '{tma_slew_event.end.isot}Z'
    """

    df_elevation = await efd_client.influx_client.query(query)

    if pd.DataFrame(df_elevation).empty:
        return pd.DataFrame(
            columns=["el_start", "el_end", "el_diff"], 
            data=[[None, None, None]]
        )
    else:
        df_elevation["el_diff"] = df_elevation["el_end"] - df_elevation["el_start"]

    return df_elevation


def script_configuration(efd_client, start_day_obs, end_day_obs):
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


def script_description(efd_client, start_day_obs, end_day_obs, block_id=None):
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


def script_log_message(efd_client, start_day_obs, end_day_obs):
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


def script_states(efd_client, start_day_obs, end_day_obs, block_id=None):
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


def block_status(client, start_day_obs, end_day_obs, block_name=None):
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
    block_name : str, optional
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

    if block_name is not None:
        df_block = df_block[df_block.id == block_name]

    return df_block
