import matplotlib
matplotlib.use("Agg")  # use Agg backend to create plots without a GUI (for testing or headless environments)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# load the data from the csv file
df = pd.read_csv("medical_examination.csv")

# calculate bmi and create an "overweight" column
# bmi = weight (kg) / height (m)^2
# mark as 1 if bmi > 25, otherwise is 0
bmi = df["weight"] / (df["height"] / 100) ** 2
df["overweight"] = (bmi > 25).astype(int)

# normalize cholesterol and glucose so that 0 is always good and 1 is always bad
# if value == 1, then 0 (good)
# if value > 1, then 1 (bad)
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)


def draw_cat_plot():
    # reshape the dataframe with pd.melt so it can plot categorical variables
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"],
        var_name="feature",
        value_name="value",
    )

    # group by cardio, feature, and value to count occurrences
    df_cat = (
        df_cat.groupby(["cardio", "feature", "value"], as_index=False)
        .size()
        .rename(columns={"size": "total"})
    )

    # create the catplot with seaborn
    g = sns.catplot(
        data=df_cat,
        x="feature",
        y="total",
        hue="value",
        col="cardio",
        kind="bar",
        height=5,
        aspect=1.2,
        palette={0: "#c39bd3", 1: "#9b59b6"}
    )

    # make it easier to read
    g.set_axis_labels("feature", "count")
    g.set_titles("cardio = {col_name}")
    g.set_xticklabels(rotation=45)

    # get the figure object
    fig = g.fig

    # save the figure
    fig.savefig("catplot.png")
    return fig


def draw_heat_map():
    # clean the data to remove incorrect or extreme values
    df_heat = df.copy()

    # keep rows where diastolic pressure <= systolic pressure
    df_heat = df_heat[df_heat["ap_lo"] <= df_heat["ap_hi"]]

    # keep only height and weight within the 2.5th and 97.5th percentiles
    h_low, h_high = df_heat["height"].quantile([0.025, 0.975])
    w_low, w_high = df_heat["weight"].quantile([0.025, 0.975])

    df_heat = df_heat[(df_heat["height"] >= h_low) & (df_heat["height"] <= h_high)]
    df_heat = df_heat[(df_heat["weight"] >= w_low) & (df_heat["weight"] <= w_high)]

    # calculate the correlation matrix
    corr = df_heat.corr(numeric_only=True)

    # create a mask to hide the upper triangle of the heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # draw the heatmap with seaborn
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        linewidths=0.5,
        center=0,
        cmap="PuRd",
        cbar_kws={"shrink": 0.5},
        vmin=-0.1,
        vmax=0.3,
        ax=ax,
    )

    # save the figure (required for fcc tests)
    fig.savefig("heatmap.png")
    return fig


# run the plots if this file is executed directly
if __name__ == "__main__":
    draw_cat_plot()
    draw_heat_map()

from medical_data_visualizer import draw_cat_plot, draw_heat_map

if __name__ == "__main__":
    print("generating catplot...")
    draw_cat_plot()
    print("saved as catplot.png")

    print("generating heatmap...")
    draw_heat_map()
    print("saved as heatmap.png")