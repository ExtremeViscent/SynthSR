""" This scripts generates 3 examples of trainig data for joint SR/synthesis between low resolution (LR) and high
resolution (HR) T1 scans. We use here real HR T1 scans.
The synthetic scans are generated by sampling a Gaussian Mixture Model conditioned on label maps, which must
correspond to the real HR scans used as target regression. Both real and synthetic scans undergo the same spatial
augmentation (such that they are still aligned), and the synthetic scans are further augmented with artefacts and
intensity augmentations.
Then the synthetic scans are blurred and possibly downsampled to the simulated LR. If downsampled, the data will then
be upsampled back to HR, so that the downstream network is trained to super-resolved at HR. This upsampling step
mimics the process that will happen at test time.



If you use this code, please the SynthSR paper in:
https://github.com/BBillot/SynthSR/blob/master/bibtex.bib

Copyright 2020 Benjamin Billot

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.
"""

import os

from pathlib import Path
home_dir = '/media/hdd/viscent'

# change directory (to import SynthSR code) - NOT REQUIRED IF RUNNING FROM COMMAND LINE?
#os.chdir(home_dir+'/Python/github/SynthSR')

import sys
sys.path.insert(0,os.path.join(home_dir,'SynthSR'))

import time
import numpy as np
from ext.lab2im import utils
from SynthSR.brain_generator import BrainGenerator

data_dir = os.path.join(home_dir,'dHCP/synthsr_data')

# folder containing label maps to generate images from
#labels_folder = '../../data/labels'
#labels_folder = data_dir+'/labels'     # 0.5 mm isotropic
labels_folder = data_dir+'/labels_1mm'  # 1 mm isotropic

# folder containing corresponding images, that will be used as target regression
#images_folder = '../../data/images/'
#images_folder = data_dir+'/images_t1'      # 0.5 mm isotropic
images_folder = data_dir+'/images_t1_1mm'   # 1 mm isotropic

# result parameters
n_examples = 5  # number of generated examples
#result_dir = '../../data/generated_images/1-SR_real'  # folder where they will be saved
result_dir = data_dir+'/1-SR_real'

# general parameters
# We need to specify if each *synthetic* channel is going to be used as an input for the downstream regression network.
# Because we use real regression targets, then we only synthesise 1 channel (the LR T1 scans), we only provide here a
# boolean (this would be a list otherwise).
input_channels = True
# Out of all the synthesise targets, we need to indicate if one of them is going to be used as regression target. Here
# we set this parameter to None, since the regression targets are not synthetic, but real.
output_channel = None
# We have the possibility to generate training examples at a different resolution than the training label maps (e.g.
# when using ultra HR training label maps). Here we want to generate at the same resolution as the training label maps,
# so we set this to None.
target_res = None
# The generative model offers the possibility to randomly crop the training examples to a given size. In this first
# example, we do not randomly crop the generated pairs.
output_shape = None

# Here we specify the structures in the label maps for which we want to generate intensities.
# This is given as a list of label values. These label values do not need to be present in every label map.
# Example: generation_labels = [0, 259, 2, 3, 17]
#generation_labels = '../../data/labels_classes_priors/generation_labels.npy'
generation_labels = data_dir+'/labels_classes_priors/generation_labels.npy'

# We now regroup similar structures into K "intensity" classes, so that intensities of similar regions are sampled from
# the same Gaussian distribution. This must be a list of the same length as generation_labels, indicating the class of
# each label. Importantly the class values must be between 0 and K-1, where K is the total number of different classes.
# Example: (continuing the previous one) generation_classes = [0, 3, 1, 2, 2]
# This means that labels 3 and 17 are in the same *class* 2 (that has nothing to do with *label* 2), and thus will be
# associated to the same Gaussian distribution when sampling the GMM.
#generation_classes = '../../data/labels_classes_priors/generation_classes.npy'
generation_classes = data_dir+'/labels_classes_priors/generation_classes.npy'

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
prior_means = data_dir+'/labels_classes_priors/prior_means_t1.npy'

# same as for prior_means, but for the standard deviations of the GMM.
#prior_stds = '../../data/labels_classes_priors/prior_stds_t1_hr.npy'
prior_stds = data_dir+'/labels_classes_priors/prior_stds_t1.npy'

# blurring/downsampling parameters
# We specify here the slice spacing/thickness that we want the synthetic scans to mimic. The axes refer to the *RAS*
# axes, as all the provided data (label maps and images) will be automatically aligned to those axes during training.
# RAS refers to Right-left/Anterior-posterior/Superior-inferior axes, i.e. sagittal/coronal/axial directions.
#data_res = np.array([1., 1., 3.])  # slice spacing i.e. resolution to mimic
#thickness = np.array([1., 1., 3.])  # slice thickness

# Hyperfine resolution
data_res = np.array([1.5, 1.5, 5.])  # slice spacing i.e. resolution to mimic
thickness = np.array([1.5, 1.5, 5.])  # slice thickness

# Because we have a large gap between the resolution at which we sample the GMM (1mm iso) and the LR we want to
# simulate, we decide here to downsample the Gaussian image to LR. If downsampled, the data will then be upsampled back
# to the target HR resolution (the one of the training label maps by default). This downsampling/upsampling step
# enables to reproduce the process that will happen at test time: real LR scans will be upsampled to HR, and run through
# the network to obtain the HR regressed scan.
downsample = True
# In practice, the network will work better when adding an input channel indicating which slices are interpolated, and
# which are real. In order to add these additional inputs we set the following parameter to True.
build_reliability_maps = True

########################################################################################################

#from keras.backend import reset_uids
#reset_uids()

# instantiate BrainGenerator object
brain_generator = BrainGenerator(labels_dir=labels_folder,
                                 images_dir=images_folder,
                                 generation_labels=generation_labels,
                                 input_channels=input_channels,
                                 output_channel=output_channel,
                                 target_res=target_res,
                                 output_shape=output_shape,
                                 generation_classes=generation_classes,
                                 prior_means=prior_means,
                                 prior_stds=prior_stds,
                                 prior_distributions='uniform', # added by FV
                                 data_res=data_res,
                                 thickness=thickness,
                                 downsample=downsample,
                                 build_reliability_maps=build_reliability_maps)

# create result dir
utils.mkdir(result_dir)

for n in range(n_examples):

    # generate !
    start = time.time()
    input_channels, regression_target = brain_generator.generate_brain()
    end = time.time()
    print('generation {0:d} took {1:.01f}s'.format(n + 1, end - start))

    # save output image and label map
    utils.save_volume(np.squeeze(input_channels[..., 0]), brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 't1_input_%s.nii.gz' % (n + 1)))
    utils.save_volume(np.squeeze(input_channels[..., 1]), brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 'reliability_map_input_%s.nii.gz' % (n + 1)))
    utils.save_volume(np.squeeze(regression_target), brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 't1_target_%s.nii.gz' % (n + 1)))
