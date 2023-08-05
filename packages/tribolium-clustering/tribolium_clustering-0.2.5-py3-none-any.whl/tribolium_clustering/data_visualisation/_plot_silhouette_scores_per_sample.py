def plot_silhouette_scores_per_sample(clustering_data, cluster_labels, 
                                      n_clusters, cmap_dict, 
                                      labelling_starts_at = 0):
    from sklearn.metrics import silhouette_samples, silhouette_score
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax1 = plt.subplots(1, 1)
    fig.set_size_inches(7, 7)

    ax1.set_xlim([-0.2, 1])

    ax1.set_ylim([0, len(clustering_data) + (n_clusters + labelling_starts_at + 1) * 10])


    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(clustering_data, cluster_labels)
    silhouette_avg = silhouette_score(clustering_data, cluster_labels)

    y_lower = 10
    for i in range(labelling_starts_at,n_clusters + labelling_starts_at):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cmap_dict[i]
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])