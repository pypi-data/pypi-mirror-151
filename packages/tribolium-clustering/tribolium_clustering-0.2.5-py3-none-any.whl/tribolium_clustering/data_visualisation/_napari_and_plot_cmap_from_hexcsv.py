import pandas as pd
from vispy.color import Colormap

def napari_and_plot_cmap_from_hexcsv(csv_file_location = None):
    

    if csv_file_location == None:
        csv_file_location = 'C://Users//ryans//OneDrive//Documents//Master Thesis//More Serious code//Nice Colourmap Set3 (256) hex.csv'

    colormap_raw_hex = pd.read_csv(csv_file_location)['colours'].tolist()
    colormap_raw_rgba = hex_colormap_to_rgba(colormap_raw_hex)
    colormap_plots = hex_colormap_to_plot_dictionary(colormap_raw_hex)

    napari_colormap = Colormap(colormap_raw_rgba, interpolation='zero')

    return napari_colormap, colormap_plots

def hex_colormap_to_rgba(hex_color_list, invisible_first_color = True):
    if invisible_first_color:
        rgba_palette_list = [list(int(h[i:i+2], 16)/255 for i in (1, 3, 5))+[1] for h in hex_color_list]
        rgba_palette_list[0][3] = 0
    else:
        rgba_palette_list = [list(int(h[i:i+2], 16)/255 for i in (1, 3, 5))+[1] for h in hex_color_list]
    
    return rgba_palette_list

def hex_colormap_to_plot_dictionary(hex_color_list, first_color_is_background = True):
    if first_color_is_background:
        colormap = [tuple(int(h[i:i+2], 16)/255 for i in (1, 3, 5)) for h in hex_color_list[1:]]
    else:
        colormap = [tuple(int(h[i:i+2], 16)/255 for i in (1, 3, 5)) for h in hex_color_list]
    
    
    colormap_dict = {i:color for i, color in enumerate(colormap)}  
    colormap_dict[-1] = (0.7,0.7,0.7)
    
    return colormap_dict

def napari_label_cmap(csv_file_location = None):
    if csv_file_location == None:
        csv_file_location = 'C://Users//ryans//OneDrive//Documents//Master Thesis//More Serious code//Nice Colourmap Set3 (256) hex.csv'

    colormap_raw_hex = pd.read_csv(csv_file_location)['colours'].tolist()
    colormap_raw_rgba = hex_colormap_to_rgba(colormap_raw_hex)

    napari_labels_cmap_dict = {k:v for k, v in enumerate(colormap_raw_rgba)}

    return napari_labels_cmap_dict

def plot_cmap(csv_file_location = None):
    if csv_file_location == None:
        csv_file_location = 'C://Users//ryans//OneDrive//Documents//Master Thesis//More Serious code//Nice Colourmap Set3 (256) hex.csv'

    colormap_raw_hex = pd.read_csv(csv_file_location)['colours'].tolist()
    colormap_plots = hex_colormap_to_plot_dictionary(colormap_raw_hex)

    return colormap_plots
    