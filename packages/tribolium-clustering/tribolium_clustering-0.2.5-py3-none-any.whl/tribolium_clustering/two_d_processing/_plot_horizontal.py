def plot_horizontal(image_list, title_list = None, size = (20,20)):
    import matplotlib.pyplot as plt
    fig,axs = plt.subplots(1,len(image_list),figsize = size)
    for i,j in zip(image_list, range(len(image_list))):
        axs[j].imshow(i, cmap = 'gray')
        if title_list != None:
            axs[j].set_title(title_list[j])
    plt.show()