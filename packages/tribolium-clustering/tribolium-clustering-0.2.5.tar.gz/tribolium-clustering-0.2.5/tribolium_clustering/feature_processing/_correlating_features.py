def correlating_features(df_regprops, corr_thresh = 0.95):
    import numpy as np
    correlation_df = df_regprops.corr().abs()
    correlation_matrix = correlation_df.to_numpy()

    corr_keys=correlation_df.keys()

    mask = np.ones(correlation_matrix.shape, dtype= bool)
    mask = np.triu(mask, k = 1)

    masked_array = correlation_matrix * mask

    highly_corr = np.where(masked_array >= corr_thresh)

    correlating_feats = [(corr_keys[i],corr_keys[j]) for i,j in zip(highly_corr[0],highly_corr[1])] 
    
    return correlating_feats