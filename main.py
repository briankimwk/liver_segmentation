# Data preparation from DICOM slices to NIFTII files in groups of 65 slices
# No patients have less than 65 slices

# input path
in_path = "/Users/briankim/Documents/PhD/Coursework/Monai/dicom_files/images"
out_path = "/Users/briankim/Documents/PhD/Coursework/Monai/dicom_groups/images"

from glob import glob
import shutil
import os

for patient in glob(in_path + '/*'):
    patient_name = os.path.basename(os.path.normpath(patient))
    number_folders = int(len(glob(patient+'/*'))/64)

    for i in range(number_folders):
        output_path_name = os.path.join(out_path, patient_name + '_' + str(i))
        os.mkdir(output_path_name)

        for i, file in enumerate(glob(patient+'/*')):
            if i == 64 + 1:
                break
            shutil.move(file, output_path_name)

# Convert all DICOM files of interest into NIFTIs

import dicom2nifti
import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()

in_path_images = "/Users/briankim/Documents/PhD/Coursework/Monai/dicom_groups/images/*"
in_path_labels = "/Users/briankim/Documents/PhD/Coursework/Monai/dicom_groups/labels/*"
out_path_images = "/Users/briankim/Documents/PhD/Coursework/Monai/nifti_files/images"
out_path_labels = "/Users/briankim/Documents/PhD/Coursework/Monai/nifti_files/labels"

list_images = glob(in_path_images)
list_labels = glob(in_path_labels)

for patient in list_images:
    '''
    Function from library changing patient files to compressed NIFTI files
    '''
    patient_name = os.path.basename(os.path.normpath(patient))
    dicom2nifti.dicom_series_to_nifti(patient, os.path.join(out_path_images, patient_name + ".nii.gz"))

for patient in list_labels:
    patient_name = os.path.basename(os.path.normpath(patient))
    dicom2nifti.dicom_series_to_nifti(patient, os.path.join(out_path_labels, patient_name + ".nii.gz"))
