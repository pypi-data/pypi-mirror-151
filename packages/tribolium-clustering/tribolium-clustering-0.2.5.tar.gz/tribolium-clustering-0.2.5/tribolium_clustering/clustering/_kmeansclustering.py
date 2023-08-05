# perform Kmeans clustering and return predictionlist
def kmeansclustering(measurements, clusternumber, iterations = 1000):
    from sklearn.cluster import KMeans
    import pandas as pd
    
    # scikit learn works with pandas dataframes so we will convert the dictionary into a dataframe
    data_frame = pd.DataFrame(measurements)
    
    # initialise clustering
    km = KMeans(n_clusters=clusternumber, max_iter=iterations, random_state =1000)

    # performing the clustering
    Y_pred = km.fit_predict(data_frame)

    # saving prediction as list for generating clustering image
    return Y_pred