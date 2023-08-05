def napari_clusterimage_with_cmap(viewer, image, cmap, rotation = (-30,180,85)):
    viewer.add_image(image.astype('uint8'), rotate=rotation, colormap=cmap, opacity=0.6, interpolation= 'nearest')