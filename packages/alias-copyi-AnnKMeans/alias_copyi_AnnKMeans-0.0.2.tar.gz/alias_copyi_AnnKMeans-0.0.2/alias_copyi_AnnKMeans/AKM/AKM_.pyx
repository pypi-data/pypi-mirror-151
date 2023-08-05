cimport numpy as np
import numpy as np
np.import_array()

from .AKM_ cimport AKM

cdef class PyAKM:
    cdef AKM c_AKM

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, bool debug=False):
        self.c_AKM = AKM(X, c_true, debug)

    def opt(self, Cen, int ITER=300):

        self.c_AKM.opt(Cen, ITER)

    @property
    def y_pre(self):
        return np.array(self.c_AKM.Y)
    
    @property
    def n_iter_(self):
        return np.array(self.c_AKM.n_iter_)

    @property
    def cal_num_dist(self):
        return np.array(self.c_AKM.cal_num_dist)

    @property
    def dist_num_arr(self):
        return np.array(self.c_AKM.dist_num_arr)

    @property
    def time_arr(self):
        return np.array(self.c_AKM.time_arr)