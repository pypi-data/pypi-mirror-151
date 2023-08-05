def add_centroids(regionprops, topologyprops, centroidnamelist = ['centroid-0','centroid-1','centroid-2']):
    import pandas as pd
    
    centroids_list = [regionprops[key] for key in centroidnamelist]
    centroids_list.append(topologyprops)
    top_props_wcentroid = pd.concat(centroids_list, axis = 1)
    
    return top_props_wcentroid