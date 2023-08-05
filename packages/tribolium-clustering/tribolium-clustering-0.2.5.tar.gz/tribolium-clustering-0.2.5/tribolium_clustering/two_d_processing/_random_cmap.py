def random_cmap(seed = 1):
    import numpy as np
    np.random.seed(seed)
    black = np.zeros((1,3), dtype=float)
    randcmap = np.append(black,(np.random.rand(255,3)),axis=0)
    return randcmap