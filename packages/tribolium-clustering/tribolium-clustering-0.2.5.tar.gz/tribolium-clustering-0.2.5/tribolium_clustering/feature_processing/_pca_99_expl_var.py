def pca_99_expl_var(df_reg_props_scaled):
    from sklearn.decomposition import PCA
    import pandas as pd
    pca = PCA()

    # Separating out the features
    x = df_reg_props_scaled.loc[:, df_reg_props_scaled.keys()].values
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
    
    return df_PCA_99