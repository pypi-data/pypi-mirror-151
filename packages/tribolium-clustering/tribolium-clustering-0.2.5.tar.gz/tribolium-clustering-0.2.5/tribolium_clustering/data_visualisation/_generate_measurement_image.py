def generate_measurement_image(gpu_labelimage , measurementlist, measurement_wo_bkgnd = True):
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
    gpu_labelimage = None
    clelist = None
    
    output = cle.pull(parametric_image)
    parametric_image = None
    
    return output