# given an image from which blobs were detected and blobs list in format [[x,y,r]] returns boolean image
# with spots as True pixels 
def spot2image(image,spotlist):
    import numpy as np
    spot_image = np.zeros((image.shape), dtype=bool) # returns boolean image (only true = white and false = black) with original dimension
    for spot in spotlist:
        x, y, r = spot    # since scikit image returns x,y and radius coordinates we need 3 variables, even if one isn't used
        spot_image[int(x),int(y)] = True
    return spot_image