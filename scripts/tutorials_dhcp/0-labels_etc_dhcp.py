#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 18:31:09 2022

@author: frantisek
"""

# %% Generation of np files with dHCP labels for SynthSR tutorials

import os
import numpy as np

from pathlib import Path
home_dir = str(Path.home())

import sys
sys.path.insert(0,home_dir+'/Python/github/SynthSR-ANC')
sys.path.insert(0,home_dir+'/Python/github/SynthSR-ANC/SynthSR')

#os.chdir(home_dir+'/Python/github/SynthSR-ANC/SynthSR')
from estimate_priors import build_intensity_stats

data_dir = home_dir+'/Data/dHCP/synthsr_data'

# %% 1-1

# Here we specify the structures in the label maps for which we want to generate intensities.
# This is given as a list of label values. These label values do not need to be present in every label map.
# Example: generation_labels = [0, 259, 2, 3, 17]

# generation_labels = data_dir+'/labels_classes_priors/generation_labels.npy'

# 1 Cerebrospinal fluid (CSF)
# 2 Cortical grey matter (cGM)
# 3 White matter (WM)
# 4 Background
# 5 Ventricle
# 6 Cerebellum
# 7 Deep Grey Matter (GM)
# 8 Brainstem
# 9 Hippocampus

generation_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
np.save(data_dir+'/labels_classes_priors/generation_labels.npy',generation_labels)

# %% 1-2

# We now regroup similar structures into K "intensity" classes, so that intensities of similar regions are sampled from
# the same Gaussian distribution. This must be a list of the same length as generation_labels, indicating the class of
# each label. Importantly the class values must be between 0 and K-1, where K is the total number of different classes.
# Example: (continuing the previous one) generation_classes = [0, 3, 1, 2, 2]
# This means that labels 3 and 17 are in the same *class* 2 (that has nothing to do with *label* 2), and thus will be
# associated to the same Gaussian distribution when sampling the GMM.

# generation_classes = data_dir+'/labels_classes_priors/generation_classes.npy'

generation_classes = [i-1 for i in generation_labels] # same as above, but shifted to start at 0 // [0,1,2,3,4,5,1,6,7] #
np.save(data_dir+'/labels_classes_priors/generation_classes.npy',generation_classes)

# %% 1-3

# We specify here the hyperparameters governing the prior distribution of the GMM.
# As these prior distributions are Gaussians, they are each controlled by a mean and a standard deviation.
# Therefore, the numpy array pointed by prior_means is of size (2, K), where K is the total nummber of classes specified
# in generation_classes. The first row of prior_means correspond to the means of the Gaussian priors, and the second row
# correspond to standard deviations.
# Example: (continuing the previous one) prior_means = np.array([[0, 110, 95, 40]
#                                                                [0,  20, 15, 60]])
# This means that intensities of label 3 and 17 will be drawn from the same Gaussian distribution, whose mean will be
# sampled from distribution N(95, 15) (as this corresponds to prior_means[:, 2]). Here is the complete table of
# correspondance for this example:
# mean of Gaussian for label   0 drawn from N(0,0)=0
# mean of Gaussian for label 259 drawn from N(40,60)
# mean of Gaussian for label   2 drawn from N(110,20)
# mean of Gaussian for labels 3 and 17 drawn from N(95,15)
# These hyperparameters were estimated with the function SynthSR/estimate_priors.py/build_intensity_stats()
#prior_means = '../../data/labels_classes_priors/prior_means_t1_hr.npy'

# same as for prior_means, but for the standard deviations of the GMM.
#prior_stds = '../../data/labels_classes_priors/prior_stds_t1_hr.npy'

# build_intensity_stats(list_image_dir,
#                           list_labels_dir,
#                           result_dir,
#                           estimation_labels,
#                           estimation_classes=None,
#                           max_channel=3,
#                           rescale=True):

# t1
# build_intensity_stats(list_image_dir = data_dir+'/images_t1_skull',
#                           list_labels_dir = data_dir+'/labels',
#                           result_dir = data_dir+'/labels_classes_priors',
#                           estimation_labels = data_dir+'/labels_classes_priors/generation_labels.npy',
#                           estimation_classes = data_dir+'/labels_classes_priors/generation_classes.npy')

# rename above to "_t1"

# t2
build_intensity_stats(list_image_dir = data_dir+'/images_t2_skull',
                          list_labels_dir = data_dir+'/labels',
                          result_dir = data_dir+'/labels_classes_priors',
                          estimation_labels = data_dir+'/labels_classes_priors/generation_labels.npy',
                          estimation_classes = data_dir+'/labels_classes_priors/generation_classes.npy')

# rename above to "_t2"

# %% inspect means and stds generated above - renamed to "_t1"

#prior_means = np.load(data_dir+'/labels_classes_priors/prior_means_t1.npy')
#prior_stds = np.load(data_dir+'/labels_classes_priors/prior_stds_t1.npy')

