def plot_predictions_onto_UMAP(embedding, prediction, title = ' ', HDBSCAN = True):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    np.random.rand
    np.random.seed(42)
    rand_colours = np.random.rand((max(prediction)+3))
    plt.figure(figsize = (10,10))
    
    
    if HDBSCAN:
        clustered = (prediction >= 0)
        
        plt.scatter(embedding[~clustered, 0],
                    embedding[~clustered, 1],
                    c=(0.6, 0.6, 0.6), s=10, alpha=0.3)
        try:
            plt.scatter(embedding[clustered, 0],
                        embedding[clustered, 1],
                        c=[sns.color_palette()[int(x)] for x in prediction[clustered]],
                        s=10);
        except IndexError:
            plt.scatter(embedding[clustered, 0],
                        embedding[clustered, 1],
                        c=[rand_colours[x] for x in prediction[clustered]],
                        s=10);
    else:
        try:
            plt.scatter(embedding[:, 0],
                        embedding[:, 1],
                        c=[sns.color_palette()[int(x)] for x in prediction],
                        s=10);
        except IndexError:
            plt.scatter(embedding[:, 0],
                        embedding[:, 1],
                        c=[rand_colours[x] for x in prediction],
                        s=10);
    
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(title, fontsize=18)