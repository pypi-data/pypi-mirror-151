def correlating_feature_filter(df_regprops,threshold):
    import numpy as np
    import pandas as pd
    import PySimpleGUI as sg

    # Actually finding the correlating features with pandas
    correlation_df = df_regprops.corr().abs()
    correlation_matrix = correlation_df.to_numpy()

    # using numpy to get the correlating features out of the matrix
    mask = np.ones(correlation_matrix.shape, dtype= bool)
    mask = np.triu(mask, k = 1)
    masked_array = correlation_matrix * mask
    highly_corr = np.where(masked_array >= threshold)

    # Using sets as a datatype for easier agglomeration of the features
    # afterwards conversion back to list
    correlating_feats = [{i,j} for i,j in zip(highly_corr[0],highly_corr[1])]    
    correlating_feats_agglo = agglomerate_corr_feats(correlating_feats)
    corr_ind_list = [sorted(list(i)) for i in correlating_feats_agglo]
    
    # getting the keys and then turning the indices into keys
    keys = df_regprops.keys()
    correlating_keys = [keys[ind].tolist() for ind in corr_ind_list]

    # gui part for selecting the features to keep from the 
    # correlating groups
    listboxes = [] 
    for i,keylist in enumerate(correlating_keys):
        listboxes.append([sg.Listbox(values=keylist, key='-CORFEAT{}-'.format(i), size=(30, 6))])

    layout = [[sg.Text("Choose which features to keep")]] + listboxes + [[sg.Button("OK")]]

    window = sg.Window('',layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break         
    window.close()

    # getting the chosen features from the gui
    kept_feats = []
    for i in range(len(correlating_keys)):
        kept_feats += values['-CORFEAT{}-'.format(i)]

    # getting all the feature keys that were correlating
    all_selectionfeats = correlating_feats[0]
    for i in correlating_feats:
        all_selectionfeats = all_selectionfeats|i

    all_selectionkeys = keys[list(all_selectionfeats)].tolist()

    # finding out which keys to drop and dropping them   
    dropkeys = [key for key in all_selectionkeys if key not in kept_feats]
    resulting_df = df_regprops.drop(dropkeys,axis = 1)

    return resulting_df    



def agglomerate_corr_feats(correlating_features_sets):
    new_sets = []
    for i in correlating_features_sets:
        unique_set = True
        
        for j in correlating_features_sets:
            intersect = i&j
            if len(intersect) > 0 and i != j:
                unique_set = False
                union = (i|j)
                if union not in new_sets:
                    new_sets.append(i|j)
                
        if unique_set:
            new_sets.append(i)
            
    if new_sets == correlating_features_sets:
        return new_sets
    else:
        return agglomerate_corr_feats(new_sets)