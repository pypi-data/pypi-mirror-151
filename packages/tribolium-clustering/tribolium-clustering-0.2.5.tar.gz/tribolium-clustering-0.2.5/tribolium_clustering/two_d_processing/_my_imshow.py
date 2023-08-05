def my_imshow(image):
    from matplotlib.pyplot import figure
    from skimage.io import imshow
    figure(figsize=(10,10)) # configure imshow dpi to make image larger
    imshow(image, cmap = 'gray')
