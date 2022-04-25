#!/bin/bash
# for a in /sys/bus/pci/devices/*; do echo 0 | sudo tee -a $a/numa_node; done
export PATH=/work/zhangyq/intel/oneapi/intelpython/latest/envs/synthsr/bin:$PATH
export LD_LIBRARY_PATH=/work/zhangyq/intel/oneapi/intelpython/latest/envs/synthsr/lib:$LD_LIBRARY_PATH
conda activate synthsr