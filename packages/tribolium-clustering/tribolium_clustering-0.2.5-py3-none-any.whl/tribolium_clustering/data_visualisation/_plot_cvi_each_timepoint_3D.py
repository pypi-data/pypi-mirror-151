def plot_cvi_each_timepoint_3D(cvi_scores_concatenated, timepoints_list, cluster_numbers, cvi_name = '', timepoint_label = 'Timepoints'):
    '''Plots a 3D plot displaying timepoint indices, cluster numbers and their cluster validation index scores
    
    Parameters
    ----------
    cvi_scores_concatenated : CVI scores list
        CVI scores in the form [cvi-t1,...,cvi-tn]2,...,[cvi-t1,...,cvi-tn]k concatenated
    timepoints_list : list
        Timepoints used as a list (can also just be indices)
    cluster_numbers : list
        cluster numbers used sorted: [2,..,k]
    cvi_name : string
        label for the axis of the CVI score 
    timepoint_label : string
        label for the timepoint axis
    

    '''
    
    import numpy as np
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm

    x = np.array(timepoints_list)
    y = np.array(cluster_numbers)
    z = cvi_scores_concatenated

    X, Y = np.meshgrid(x, y)
    Z = np.reshape(z, X.shape)  # Z.shape must be equal to X.shape = Y.shape

    fig = plt.figure(figsize = (20,20))
    ax = fig.add_subplot(projection='3d')

    ax.plot_surface(X, Y, Z,cmap=cm.coolwarm)

    ax.set_xlabel(timepoint_label)
    ax.set_ylabel('Number of Clusters')
    ax.set_zlabel(cvi_name)

    ax.view_init(elev=20., azim=65)

    plt.show()

