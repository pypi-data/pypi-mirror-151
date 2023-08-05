def plot_predictions_onto_scatter_plot(prediction, datax, 
                                       datay, title = ' ', cmap_dict = None,
                                       spot_size = 1, non_noise_alpha = 0.3):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    np.random.rand
    np.random.seed(42)
    rand_colours = np.random.rand((max(prediction)+3))
    
    plt.figure(figsize = (10,10))
    
    if not cmap_dict:
        cmap_dict = sns.color_palette()
    
    clustered = (prediction >= 0)    
        
    plt.scatter(datax[~clustered],
                datay[~clustered],
                c=(0.6, 0.6, 0.6), s=spot_size, alpha=0.2)
    try:
        plt.scatter(datax[clustered],
                    datay[clustered],
                    c=[cmap_dict[int(x)] for x in prediction[clustered]],
                    s=spot_size, alpha= non_noise_alpha);
    except IndexError:
        plt.scatter(datax[clustered],
                    datay[clustered],
                    c=[rand_colours[x] for x in prediction[clustered]],
                    s=spot_size, alpha= non_noise_alpha);
    
    
    #plt.gca().set_aspect('equal', 'datalim')
    plt.title(title, fontsize=18)