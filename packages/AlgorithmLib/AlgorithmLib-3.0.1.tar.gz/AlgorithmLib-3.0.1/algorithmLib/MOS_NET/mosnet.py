import speechmetrics
import os
import numpy as np
import sys

sys.path.append('../')

window_length  = None

metrics = speechmetrics.load(['mosnet'], window_length)

path_to_estimate_file = 'D:/Task/4_VC/2_starganv2_vc/StarGANv2-VC-main/Models/cloud/9_VCTK18_NE2_modified_R_FM_2/test_new/'
# path_to_estimate_file = 'D:/Task/4_VC/3_data/recorded_24k_test/'
# path_to_estimate_file = 'D:/Task/4_VC/2_starganv2_vc/StarGANv2-VC-main/Data_VCTK20/'
# path_to_estimate_file = 'D:/Task/4_VC/1_vcc_challenge/2020/dataset/VCC2020-database-master/vcc2020_database_evaluation/vcc2020_database_evaluation/'
# path_to_estimate_file = 'D:/Task/4_VC/3_data/0_原始文件/集外/'

# scores = []
# for path, subdirs, files in os.walk(path_to_estimate_file, topdown=True):
#     for name in files:
#         if name.endswith(".wav"):
#             score = metrics(path + '/'+ name, None)
#             scores.append(score['mosnet'])
#
# print(np.mean(scores))

score = metrics('agora.wav', None)
print(score)
