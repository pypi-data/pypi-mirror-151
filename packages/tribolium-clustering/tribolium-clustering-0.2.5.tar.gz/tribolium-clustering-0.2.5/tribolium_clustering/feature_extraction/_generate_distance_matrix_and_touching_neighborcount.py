# measure characteristics of neighbors for label image
def generate_distance_matrix_and_touching_neighborcount(gpu_labelimage):
    import pyclesperanto_prototype as cle
    cells = cle.push(gpu_labelimage)    
    
    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(cells)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(cells)
    
    gpu_distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)
    
       
    gpu_touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(gpu_touching_neighbor_count, 0, 0)
    
    return gpu_distance_matrix, gpu_touching_neighbor_count