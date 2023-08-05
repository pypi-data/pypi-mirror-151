def filterregprops_topology(df_regprops, avg_dist_nn_list = [2,3,4]):
    nn_avg_dist_keys =['avg distance of {} closest points'.format(i) for i in avg_dist_nn_list]
    regpropstopology = df_regprops[['touching neighbor count', 'centroid-0',
                                    'centroid-1','centroid-2']+nn_avg_dist_keys]
    return regpropstopology

def filterregprops_shape(df_regprops):
    regpropsshape = df_regprops[['area', 'centroid-0','centroid-1',
                                 'centroid-2','feret_diameter_max',
                                 'major_axis_length','minor_axis_length',
                                 'solidity']]
    return regpropsshape

def filterregprops_intensity(df_regprops):
    regpropsintensity = df_regprops[['mean_intensity','max_intensity', 
                                     'min_intensity', 'image_stdev', 
                                     'centroid-0','centroid-1',
                                     'centroid-2']]
    return regpropsintensity