def sscale_with_pretrained_scaler(scaler,df_regprop):
    import numpy as np
    import pandas as pd
    keys = df_regprop.keys()
    scaled = scaler.transform(df_regprop)
    scaled = np.array(scaled).T
    output = {}
    for i,j in zip(keys, scaled):
        output[i]=j
    output = pd.DataFrame(output)
    return output  