def readcsv_as_cl_input(path):
    import pandas as pd
    csv = pd.read_csv(path)
    
    try:
        csv = csv.drop('Unnamed: 0', axis = 1)
    except:
        print('No Labels in Regionprops of {}'.format(path))
    try:
        csv = csv.drop('prediction', axis = 1)
    except:
        print('No Predictions in Regionprops of {}'.format(path))
    
    return csv