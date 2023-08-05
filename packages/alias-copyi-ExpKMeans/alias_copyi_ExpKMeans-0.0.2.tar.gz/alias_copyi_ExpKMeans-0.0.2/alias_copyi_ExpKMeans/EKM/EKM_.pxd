from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "exp_kmeanspp.cpp":
    pass

cdef extern from "EKM.cpp":
    pass

cdef extern from "EKM.h":
    cdef cppclass EKM:

        vector[vector[int]] Y
        vector[int] n_iter_
        vector[double] time_arr
        vector[int] cal_num_dist
        vector[vector[int]] dist_num_arr

        EKM() except +
        EKM(vector[vector[double]] &X, int c_true, bool debug) except +
        void opt(vector[vector[vector[double]]] &Cen, int ITER)
