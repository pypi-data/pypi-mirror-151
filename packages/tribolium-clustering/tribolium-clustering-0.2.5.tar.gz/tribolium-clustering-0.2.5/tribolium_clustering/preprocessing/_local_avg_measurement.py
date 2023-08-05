def local_avg_measurement(measurementlist, gpu_labelimage, measurement_wo_bkgnd = True):
    import numpy as np
    import pyclesperanto_prototype as cle
    
    if measurement_wo_bkgnd:
        measurementlist_new = np.insert(measurementlist,0,0)    
    else:
        measurementlist_new = measurementlist
        
    # testing the cle functions for generation of outline image and cluster label image
    # first pushing of variables to GPU
    clelist = cle.push(measurementlist_new)

    #generation of cluster label image
    parametric_image = cle.replace_intensities(gpu_labelimage, clelist)
    clelist = None
    
    loc_val_img = cle.mean_of_touching_neighbors_map(parametric_image, gpu_labelimage)
    parametric_image = None
    
    temp_loc_val = cle.read_intensities_from_map(gpu_labelimage, loc_val_img)
    
    loc_val = cle.pull(temp_loc_val)[0][1:]
    gpu_labelimage = None
    loc_val_img = None
    temp_loc_val = None
    return loc_val

def local_avg_dataframe(dataframe, gpu_labelimage, measurement_wo_bkgnd = True,
                        exceptions = ['centroid-0', 'centroid-1', 'centroid-2']):
    import pandas as pd
    
    keylist = dataframe.keys()
    new_keylist = ['local avg '+ key for key in keylist]
    measurements = [dataframe[key].tolist() for key in keylist if key not in exceptions]
    loc_avg_measurements = [local_avg_measurement(measure, gpu_labelimage, measurement_wo_bkgnd = measurement_wo_bkgnd) for measure in measurements]
    gpu_labelimage = None
    loc_avg_dict = {k:v for k,v in zip(new_keylist,loc_avg_measurements)}
    
    return pd.DataFrame(loc_avg_dict)