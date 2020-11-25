wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
conda create -n javis  python=3.8
conda activate javis
conda  install  -y -c anaconda numpy
conda install   -y -c anaconda flask
conda install   -y -c conda-forge flask-wtf
conda install  -y  -c conda-forge flask-restplus
conda install   -y -c conda-forge flask-jsonpify
conda install   -y -c conda-forge flask-socketio
conda install   -y -c conda-forge opencv
pip install Werkzeug==0.16.1