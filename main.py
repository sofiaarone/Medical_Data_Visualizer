from medical_data_visualizer import draw_cat_plot, draw_heat_map

if __name__ == "__main__":
    # generate the categorical plot showing counts of features by cardio
    print("generating catplot...")
draw_cat_plot()
print("saved as catplot.png")

# generate the heatmap showing correlation between features
print("generating heatmap...")
draw_heat_map()
print("saved as heatmap.png")