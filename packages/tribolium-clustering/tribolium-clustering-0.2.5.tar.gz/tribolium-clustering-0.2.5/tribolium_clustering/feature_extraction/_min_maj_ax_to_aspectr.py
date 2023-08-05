def min_maj_ax_to_aspectr(df_regprops, del_min_maj = True, min_ax_name = 'minor_axis_length', maj_ax_name = 'major_axis_length'):
    import numpy as np
    import pandas as pd
    keys = df_regprops.keys().tolist()
    min_maj_keys = [key for key in keys if key == min_ax_name or key == maj_ax_name]
    if len(min_maj_keys) < 2:
        return print('not enough axes to determine aspect ratio')
    else:
        min_axis_vals = np.array(df_regprops[min_ax_name].tolist())
        maj_axis_vals = np.array(df_regprops[maj_ax_name].tolist())
        
        aspect_ratio = {}
        aspect_ratio['aspect_ratio'] = maj_axis_vals/min_axis_vals
        aspect_ratio = pd.DataFrame(aspect_ratio).reset_index(drop=True)
        
        if del_min_maj:
            df_regprops = df_regprops.drop(min_maj_keys, axis = 1).reset_index(drop=True)
            
            return pd.concat([df_regprops,aspect_ratio], axis = 1)
        
        else:
            return pd.concat([df_regprops.reset_index(drop=True),aspect_ratio], axis = 1)