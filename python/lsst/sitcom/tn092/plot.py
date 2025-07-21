import matplotlib.pyplot as plt
import os

from lsst.summit.utils.tmaUtils import TMAState

__all__ = ["histogram_hp_minmax_forces"]


def histogram_hp_minmax_forces(df, day_obs, end_reason=None):
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
    end_reason = TMAState(end_reason) if end_reason is not None else None
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
    
    if end_reason is not None:
        mask = df["end_reason"] == end_reason
        min_ax.hist(
            df.loc[mask, "min_forces"],
            ec="white",
            fc="orange",
            alpha=0.5,
            label=f"Minimum forces ({end_reason.name})",
            log=True,
        )
        max_ax.hist(
            df.loc[mask, "max_forces"],
            ec="white",
            fc="orange",
            alpha=0.5,
            label=f"Maximum forces ({end_reason.name})",
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
