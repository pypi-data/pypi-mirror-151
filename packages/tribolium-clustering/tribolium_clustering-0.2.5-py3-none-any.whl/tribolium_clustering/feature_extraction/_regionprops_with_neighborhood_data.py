def regionprops_with_neighborhood_data(labelimage,gpu_labelimage,originalimage, n_closest_points_list = [2,3,4]):
    from skimage.measure import regionprops_table
    import pyclesperanto_prototype as cle
    import numpy as np
    # get lowest label index to adjust sizes of measurement arrays
    min_label = int(np.min(labelimage[np.nonzero(labelimage)]))
   
    #  defining function for getting standarddev as extra property
    # arguments must be in the specified order, matching regionprops
    def image_stdev(region, intensities):
        # note the ddof arg to get the sample var if you so desire!
        return np.std(intensities[region], ddof=1)
    
    # get region properties from labels
    regionprops = regionprops_table(labelimage.astype(dtype = 'uint16'), intensity_image= originalimage, 
                                        properties= ('area', 'centroid','feret_diameter_max',
                                        'major_axis_length','minor_axis_length', 'solidity', 'mean_intensity',
                                        'max_intensity', 'min_intensity'),extra_properties=[image_stdev])
    print('Scikit Regionprops Done')
    
    # push labelimage to GPU
    cells = gpu_labelimage
    gpu_labelimage = None
    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(cells)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(cells)
    
    cells = None
    
    # generate a distance matrix
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)
    
    # detect touching neighbor count   
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(touching_neighbor_count, 0, 0)
    touch_matrix = None

    # conversion and editing of the distance matrix, so that it doesn't break cle.average_distance.....
    viewdist_mat = cle.pull(distance_matrix)
    distance_matrix = None
    
    tempdist_mat = np.delete(viewdist_mat, range(min_label), axis = 0)
    edited_distmat = np.delete(tempdist_mat, range(min_label), axis =1)

    #iterating over different neighbor numbers for avg neighbor dist calculation
    for i in n_closest_points_list:
        distance_of_n_closest_points = cle.pull(cle.average_distance_of_n_closest_points(cle.push(edited_distmat), n=i))[0]
    
        # addition to the regionprops dictionary
        regionprops['avg distance of {val} closest points'.format(val = i)]=distance_of_n_closest_points

    # processing touching neighborcount for addition to regionprops (deletion of background & not used labels)
    touching_neighbor_c = cle.pull(touching_neighbor_count)
    touching_neighbor_count = None
    touching_neighborcount_formated = np.delete(touching_neighbor_c, list(range(min_label)))
    
    # addition to the regionprops dictionary
    regionprops['touching neighbor count']= touching_neighborcount_formated
    print('Regionprops Completed')
    
    # clearing of memory
    touching_neighborcount_formated = None
    touching_neighbor_c = None
    tempdist_mat = None
    edited_distmat = None
    distance_of_n_closest_points = None
    
    return regionprops