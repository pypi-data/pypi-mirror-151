def fit_pca_and_get_subset_limit(df_regprops):
    from sklearn.decomposition import PCA
    pca = PCA()

    # Separating out the features
    x = df_regprops.loc[:, df_regprops.keys()].values
    pca.fit(x)

    # getting the explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_expl_var = [sum(explained_variance[:i+1]) for i in range(len(explained_variance))]
    for i,j in enumerate(cumulative_expl_var):
        if j >= 0.99:
            pca_cum_var_idx = i
            break
    return pca, pca_cum_var_idx