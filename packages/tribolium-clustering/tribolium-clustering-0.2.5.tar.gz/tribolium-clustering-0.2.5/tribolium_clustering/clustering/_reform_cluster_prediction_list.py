# function for reforming the prediction list as regionprops does not start at 0
def reform_cluster_prediction_list(labelimage, predictionlist):
    import numpy as np
    predictionlist_new = np.array(predictionlist) + 1
    for i in range(int(np.min(labelimage[np.nonzero(labelimage)]))):
        predictionlist_new = np.insert(predictionlist_new,i,0)
    return predictionlist_new