import pandas as pd
import numpy as np
from skimage import io
from vispy import color
import tribolium_clustering as tc

class processed_dataset:
    def __init__(self, directory_name: str):
        self.directory_name = directory_name
        self.timepoints = np.load(directory_name + 'timepoints.npy')
        self.rotation = np.load(directory_name + 'rotation.npy')


    def get_intensity_image(self, index):
        return io.imread(self.directory_name + 'rescaled t = {}s.tif'.format(self.timepoints[index]))

    def get_labels(self, index):
        return io.imread(self.directory_name + 'workflow t = {}s.tif'.format(self.timepoints[index]))

    def get_regionprops_timepoint(self, index):
        csv = pd.read_csv(self.directory_name + 'complete regionprops of t = {}s.csv'.format(self.timepoints[index]))
    
        try:
            csv = csv.drop('Unnamed: 0', axis = 1)
        except:
            print('No Labels in Regionprops of {}'.format(self.directory_name))
        try:
            csv = csv.drop('prediction', axis = 1)
        except:
            print('No Predictions in Regionprops of {}'.format(self.directory_name))
        
        return csv

    def get_all_regionprops_list(self):
        
        filelist = [self.directory_name+'complete regionprops of t = ' + str(i) + 's.csv' for i in self.timepoints]
        
        regpropslist = []

        for propname in filelist:
            try:
                regpropslist.append(pd.read_csv(propname))
            except FileNotFoundError:
                pass

        regpropslist = [pd.read_csv(i) for i in filelist]
        try:
            regpropslist = [i.drop('Unnamed: 0', axis = 1) for i in regpropslist]
        except:
            print('No Labels in Regionprops of {}'.format(self.directory_name))
        try:
            regpropslist = [i.drop('prediction', axis = 1) for i in regpropslist]
        except:
            print('No Predictions in Regionprops of {}'.format(self.directory_name))
        
        if regpropslist == []:
            print('No FIles Opened')
        
        else:
            return regpropslist

    def get_combined_regionprops(self):
        return pd.concat(self.get_all_regionprops_list(), axis = 0)
    
    def label_lengths(self):
        single_timepoint_lengths = [df.shape[0] for df in self.get_all_regionprops_list()]
        return single_timepoint_lengths
    
    def cumulative_label_lengths(self):
        return np.insert(np.cumsum(self.label_lengths()),0,0)

    def get_combined_thesis_props_no_correlation(self):
        thesis_uncorrelating_subselection = ['area', 'bbox_area', 'extent', 'feret_diameter_max', 'max_intensity',
                                     'mean_intensity', 'min_intensity', 'solidity', 'centroid-0',
                                     'centroid-1', 'centroid-2', 'image_stdev',
                                     'avg distance of 6 closest points',
                                     'stddev distance of 6 closest points', 'touching neighbor count',
                                     'aspect_ratio']
        props = tc.min_maj_ax_to_aspectr(self.get_combined_regionprops(),del_min_maj=False)
        subselection = props[thesis_uncorrelating_subselection]
    
        return subselection

    def get_combined_thesis_props(self):
            thesis_subselection = ['area', 'equivalent_diameter', 'minor_axis_length','major_axis_length','bbox_area', 'extent', 'feret_diameter_max', 'max_intensity',
                                                'mean_intensity', 'min_intensity', 'solidity', 'centroid-0',
                                                'centroid-1', 'centroid-2', 'image_stdev',
                                                'avg distance of 4 closest points',
                                                'stddev distance of 4 closest points',
                                                'avg distance of 5 closest points',
                                                'stddev distance of 5 closest points',
                                                'avg distance of 6 closest points',
                                                'stddev distance of 6 closest points', 'touching neighbor count',
                                                'aspect_ratio'
                                                ]
            props = tc.min_maj_ax_to_aspectr(self.get_combined_regionprops(),del_min_maj=False)
            subselection = props[thesis_subselection]
        
            return subselection


    def cluster_movie(self, preprocessing_function, clusterer, save_data_location, name, napari_label_cmap, interval = 1, start_index = 0):

        processed_data = preprocessing_function(self.get_combined_regionprops())

        all_predictions = clusterer.fit_predict(processed_data)
        cum_indices = self.cumulative_label_lengths()

        from qtpy.QtCore import QTimer
        import napari 
        import pyclesperanto_prototype as cle

        for i in range(start_index,len(self.timepoints),interval):
            intensity_image = self.get_intensity_image(i)
            workflow = self.get_labels(i)
            prediction = all_predictions[cum_indices[i]:cum_indices[i+1]]
            current_prop = self.get_regionprops_timepoint(i)

            regprop_with_predict = pd.concat([current_prop,pd.DataFrame(prediction, columns = ['prediction'],
                                     index = current_prop.index)], axis = 1)
            regprop_with_predict.to_csv(save_data_location + 'regprops with ' + name +' t{}.csv'.format(i))

            cluster_image = tc.generate_parametric_cluster_image(workflow,cle.push(workflow),prediction)

            with napari.gui_qt() as app:
                viewer = napari.Viewer(ndisplay=3)
                viewer.add_image(intensity_image, rotate= self.rotation)
                viewer.add_labels(cluster_image, rotate= self.rotation, color = napari_label_cmap)
            
                viewer.screenshot(save_data_location + name + ' t{}.tif'.format(i))
                
                time_in_msec = 1000
                QTimer().singleShot(time_in_msec, app.quit)
                viewer.close()


