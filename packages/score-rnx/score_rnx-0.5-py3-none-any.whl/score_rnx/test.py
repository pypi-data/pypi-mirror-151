from score_rnx.ScoreRnx import ScoreRnx
from RDMethod import RDMethod
from scipy.io import loadmat
from pandas import DataFrame
import  numpy as np
def loadData(path):

    raw_data = loadmat(path)
    data_key = list(raw_data.keys())[-1]
    data = raw_data[data_key]

    return data

# Data
matHD = np.transpose(np.loadtxt("../data/XinLego.dat", delimiter=',', unpack=True))
matLD = np.transpose(np.loadtxt("../data/URREA2DRAELego.dat", delimiter=',', unpack=True))
#h_h = loadData('../data/higado_hdmat.mat')
#l_h = loadData('../data/higado_ld_pca.mat')
#HD = loadData('../data/mnist_hd.mat')
#LD = loadData('../data/mnist_ld_pca.mat')
#face_ld_le = loadData('../data/face_ld_le_.mat')

matLD = DataFrame(matLD)

matLD = matLD[[0,1]]

print(matLD)
print("H", DataFrame(matHD))
print("L", matLD)

score_rnx = ScoreRnx(matHD)

score_rnx.add_method("DRAE3", matLD)

score_rnx.run()

score_rnx.generate_graph()
