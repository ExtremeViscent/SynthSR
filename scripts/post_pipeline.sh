sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1919 \
24 \
-T2 '/media/hdd/viscent/SynthSR/results/CHILD_T2_hf_brain_pred_200.nii.gz' \
-T1 '/media/hdd/viscent/SynthSR/results/CHILD_T1_hf_brain_pred_200.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 6

sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1920 \
24 \
-T2 '/media/hdd/viscent/SynthSR/results/CHILD_T2_hf_brain_pred_100.nii.gz' \
-T1 '/media/hdd/viscent/SynthSR/results/CHILD_T1_hf_brain_pred_100.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 6

sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1921 \
24 \
-T2 '/media/hdd/viscent/SynthSR/results/CHILD_T2_hf_brain_pred_inbox.nii.gz' \
-T1 '/media/hdd/viscent/SynthSR/results/CHILD_T1_hf_brain_pred_inbox.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 6

sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1922 \
24 \
-T2 '/media/hdd/viscent/SynthSR/results/CHILD_hf_brain_pred_inbox_hyperfine.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 6

sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1923 \
24 \
-T2 '/media/hdd/viscent/SynthSR/results/CHILD_T2_hf_brain_itk.nii.gz' \
-T1 '/media/hdd/viscent/SynthSR/results/CHILD_T1_hf_brain_itk.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 6

sudo nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v /media/hdd:/media/hdd --rm  biomedia/dhcp-structural-pipeline:latest \
114514 \
1924 \
24 \
-T2 '/media/hdd/shared/hyperfine_t1_t2/CHILD/siemens/12082019/highResStructural_9/T1.nii.gz' \
-d '/media/hdd/viscent/SynthSR/result/pipeline' \
-t 24