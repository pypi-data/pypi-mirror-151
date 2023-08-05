def variance_filter(df_regprops, threshold = 0.01, print_variances = False):
    from sklearn.feature_selection import VarianceThreshold
    import pandas as pd
    import numpy as np
    keys = df_regprops.keys().tolist()
        
    stdevs = np.std(df_regprops, axis = 0).to_numpy()
    means = np.mean(df_regprops, axis = 0).to_numpy()

    coefficients_of_variation = stdevs/means

    filtered_keys_and_idx = [(key,i) for i, key in enumerate(keys) if coefficients_of_variation[i] < threshold]
    
    if print_variances:
        for i, key in enumerate(keys):
            print(key + ' has coeff of var: {}'.format(coefficients_of_variation[i]))
    
    for fkey,i in filtered_keys_and_idx:
        print(fkey + ' was filtered out with a coefficent of variance of {}'.format(coefficients_of_variation[i]))
        keys.remove(fkey)   
    
    filtered = df_regprops.copy([keys])
    return filtered