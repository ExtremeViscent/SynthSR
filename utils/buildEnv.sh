#!/bin/bash
source ~/.bashrc
conda deactivate
conda env remove -n synthsr
conda create -n synthsr python=3.7
conda activate synthsr
pip install --no-cache-dir -r requirements.txt
