# function for generating image labelled by clusters given the labelimage and the clusterpredictionlist
def generate_parametric_cluster_image(labelimage,gpu_labelimage,predictionlist):
    
    import numpy as np
    import pyclesperanto_prototype as cle
    
    
    # reforming the prediction list this is done to account for cluster labels that start at 0
    # conviniently hdbscan labelling starts at -1 for noise, removing these from the labels
    predictionlist_new = np.array(predictionlist) + 1
    for i in range(int(np.min(labelimage[np.nonzero(labelimage)]))):
        predictionlist_new = np.insert(predictionlist_new,i,0)    

    # testing the cle functions for generation of outline image and cluster label image
    # first pushing of variables to GPU
    clelist = cle.push(predictionlist_new)

    #generation of cluster label image
    parametric_image = cle.replace_intensities(gpu_labelimage, clelist)
    gpu_labelimage = None
    clelist = None
    
    output = cle.pull(parametric_image).astype('uint32')
    parametric_image = None
    
    return output