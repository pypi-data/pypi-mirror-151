def topology_regionprops(gpu_output, nearest_neigh_list = [4,5,6], local = False):
    
    # Initialisation
    import pyclesperanto_prototype as cle
    import pandas as pd
    
    topology_props = {}
    
    avg_dmap_values = []
    stdev_dmap_values = []
    
    if local:
        loc_avg_dmap_values = []
        loc_stdev_dmap_values = []
    
    for n_count in nearest_neigh_list:
        # calculating the average distance of n nearest neighbours
        temp_avg_distance_map = cle.average_distance_of_n_closest_neighbors_map(gpu_output, n = n_count)
        temp_stdev_distance_map = cle.standard_deviation_of_touching_neighbors_map(temp_avg_distance_map, gpu_output, radius=2)
        
        # getting the values
        temp_avg_dmap_val = cle.read_intensities_from_map(gpu_output, temp_avg_distance_map)
        temp_stdev_dmap_val = cle.read_intensities_from_map(gpu_output, temp_stdev_distance_map)
        
        
        temp_stdev_distance_map = None
        
        #saving in lists for later processing
        avg_dmap_values.append(cle.pull(temp_avg_dmap_val)[0])
        stdev_dmap_values.append(cle.pull(temp_stdev_dmap_val)[0])
        temp_avg_dmap_val = None
        temp_stdev_dmap_val = None
        if local:
            temp_loc_avg_dmap = cle.mean_of_touching_neighbors_map(temp_avg_distance_map, gpu_output)
            
            temp_loc_stdev_dmap = cle.standard_deviation_of_touching_neighbors_map(temp_loc_avg_dmap, gpu_output, radius=2)
            
            temp_loc_avg_dmap_val = cle.read_intensities_from_map(gpu_output, temp_loc_avg_dmap)
            temp_loc_stdev_dmap_val = cle.read_intensities_from_map(gpu_output, temp_loc_stdev_dmap)
            
            temp_loc_avg_dmap = None
            temp_loc_stdev_dmap = None
            
            loc_avg_dmap_values.append(cle.pull(temp_loc_avg_dmap_val)[0])
            loc_stdev_dmap_values.append(cle.pull(temp_loc_stdev_dmap_val)[0])
            
            temp_loc_avg_dmap_val = None
            temp_loc_stdev_dmap_val = None
            
        temp_avg_distance_map = None
    if local:
        for avg_values, stdev_values, i in zip(loc_avg_dmap_values,loc_stdev_dmap_values,nearest_neigh_list):
            topology_props['local avg distance of {} closest points'.format(i)] = avg_values[1:]
            topology_props['local stddev distance of {} closest points'.format(i)] = stdev_values[1:]
            
    else:
        for avg_values, stdev_values, i in zip(avg_dmap_values,stdev_dmap_values,nearest_neigh_list):
            topology_props['avg distance of {} closest points'.format(i)] = avg_values[1:]
            topology_props['stddev distance of {} closest points'.format(i)] = stdev_values[1:]
            
    touch_matrix = cle.generate_touch_matrix(gpu_output)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    
    # detect touching neighbor count   
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    touching_n_count = cle.pull(touching_neighbor_count)[0][1:]
    
    touching_neighbor_count = None
    touch_matrix = None
    gpu_output = None
    topology_props['touching neighbor count']= touching_n_count
    
    return pd.DataFrame(topology_props)