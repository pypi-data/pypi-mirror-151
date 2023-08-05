def transform_PCA_99(pca_pretrained, df_regprops, index):
    import pandas as pd
    x = df_regprops.loc[:, df_regprops.keys()].values
    
    principalComponents = pca_pretrained.transform(x)
    
    subset = principalComponents.T[:index+1].T
    
    subset_headings = ['PC #'+ str(i+1) for i in range(len(subset.T))]
    
    df_PCA_99 = pd.DataFrame(data = subset, columns = subset_headings)
    
    return df_PCA_99