def regprops_to_stdscld_categorised_pca_aslist(df_regprops):
    from sklearn import preprocessing
    from sklearn.decomposition import PCA
    import numpy as np
    import pandas as pd
    
    # retrieve keys from handed dataframe
    keys = df_regprops.keys()
    
    # train scaler and process data
    scaler = preprocessing.StandardScaler().fit(df_regprops)
    scaled = scaler.transform(df_regprops)
    
    # transposition needed for iteration purposes
    scaled = np.array(scaled).T
    
    #creation of an empty dictionary
    df_scaled = {}
    
    # iteration over keys and scaled columns and filling of the new dictionary
    for i,j in zip(keys, scaled):
        df_scaled[i]=j
    
    # conversion to pandas dataframe
    df_scaled = pd.DataFrame(df_scaled)
    
    regpropsshape_stdsc = df_scaled[['area', 'centroid-0','centroid-1',
                                     'centroid-2','feret_diameter_max',
                                     'major_axis_length','minor_axis_length',
                                     'solidity']]
    regpropsintensity_stdsc = df_scaled[['mean_intensity','max_intensity', 
                                         'min_intensity', 'image_stdev',
                                         'centroid-0','centroid-1',
                                         'centroid-2']]
    regpropstopology_stdsc = df_scaled[['touching neighbor count','avg distance of 2 closest points',
                                        'avg distance of 3 closest points',
                                        'avg distance of 4 closest points', 
                                        'centroid-0','centroid-1','centroid-2']]
    
    pca = PCA()

    # Separating out the features
    x = df_scaled.loc[:, df_scaled.keys()].values
    principalComponents = pca.fit_transform(x)

    # getting the explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_expl_var = [sum(explained_variance[:i+1]) for i in range(len(explained_variance))]
    for i,j in enumerate(cumulative_expl_var):
        if j >= 0.99:
            pca_cum_var_idx = i
            break
    
    subset = principalComponents.T[:pca_cum_var_idx+1].T
    subset_headings = ['PC #'+ str(i+1) for i in range(len(subset.T))]
    df_PCA_99 = pd.DataFrame(data = subset, columns = subset_headings)
    namelist = ['Original Regionprops', 'Regionprops Standardscaled', ' Regionprops Topology', 
                'Regionprops Shape', 'Regionprops Intensity', 'Regionprops PCA']
    return [df_regprops,df_scaled,regpropstopology_stdsc,regpropsshape_stdsc,
            regpropsintensity_stdsc, df_PCA_99], namelist