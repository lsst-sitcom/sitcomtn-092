import matplotlib.pyplot as plt
import os


def histogram_hp_minmax_forces(df, day_obs):
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
