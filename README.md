# 5GLab - KI Control

## Installation
1) Download and install Anaconda
2) Install SUMO
3) Install env

###Set up the conda environment
```
conda env create -f environment.yml
conda activate 5glab
```

###register the custom_env
```
python setup.py install
pip install -e .
```

###export SUMO path permanently (if possible) to bashrc
open .bashrc file and add:
```
export SUMO_HOME="your path to sumo"
export PYTHONPATH=$PYTONPATH:"your path to sumo/tools"
```

###tensorboard command on AGENT server:
```
tensorboard --logdir=/home/agent/workspace/5glab-ki-control/outputs/tensorboard/PPO
```
