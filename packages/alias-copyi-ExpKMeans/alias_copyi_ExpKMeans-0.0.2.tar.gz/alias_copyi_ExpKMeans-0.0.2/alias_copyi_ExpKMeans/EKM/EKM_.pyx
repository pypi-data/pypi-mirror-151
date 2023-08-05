cimport numpy as np
import numpy as np
np.import_array()

from .EKM_ cimport EKM

cdef class PyEKM:
    cdef EKM c_EKM

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, bool debug=False):
        self.c_EKM = EKM(X, c_true, debug)

    def opt(self, Cen, int ITER=300):

        self.c_EKM.opt(Cen, ITER)

    @property
    def y_pre(self):
        return np.array(self.c_EKM.Y)
    
    @property
    def n_iter_(self):
        return np.array(self.c_EKM.n_iter_)

    @property
    def cal_num_dist(self):
        return np.array(self.c_EKM.cal_num_dist)

    @property
    def dist_num_arr(self):
        return np.array(self.c_EKM.dist_num_arr)

    @property
    def time_arr(self):
        return np.array(self.c_EKM.time_arr)