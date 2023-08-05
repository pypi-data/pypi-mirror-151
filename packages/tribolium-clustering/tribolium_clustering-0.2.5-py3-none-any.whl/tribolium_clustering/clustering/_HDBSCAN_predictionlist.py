def HDBSCAN_predictionlist(regionpropsdict, n_min_samples = 10, n_min_cluster = 50,UMAP = True, n_dimension_umap = 2, n_neighbors=30):
    import hdbscan
    import umap
    import pandas as pd
    
    # conversion to dataframe for handling by umap and hdbscan libraries
    dataframe = pd.DataFrame(regionpropsdict)
    
    if UMAP:
        # using UMAP to generate a dimension reduced non linear version of regionprops
        clusterable_embedding = umap.UMAP(
            n_neighbors=n_neighbors,
            min_dist=0.0,
            n_components=n_dimension_umap,
            random_state=42,
        ).fit_transform(dataframe)
        hdbscan_labels = hdbscan.HDBSCAN(min_samples=n_min_samples, min_cluster_size=n_min_cluster).fit_predict(clusterable_embedding)
    
    else:
        hdbscan_labels = hdbscan.HDBSCAN(min_samples=n_min_samples, min_cluster_size=n_min_cluster).fit_predict(dataframe)
    
    return hdbscan_labels