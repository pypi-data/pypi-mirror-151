def standardscaler_for_dataframes(input_df):
    from sklearn import preprocessing
    import numpy as np
    import pandas as pd
    
    # retrieve keys from handed dataframe
    keys = input_df.keys()
    
    # train scaler and process data
    scaler = preprocessing.StandardScaler().fit(input_df)
    scaled = scaler.transform(input_df)
    
    # transposition needed for iteration purposes
    scaled = np.array(scaled).T
    
    #creation of an empty dictionary
    df_scaled = {}
    
    # iteration over keys and scaled columns and filling of the new dictionary
    for i,j in zip(keys, scaled):
        df_scaled[i]=j
    
    # conversion to pandas dataframe
    df_scaled = pd.DataFrame(df_scaled)
    
    return df_scaled