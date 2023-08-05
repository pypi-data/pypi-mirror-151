from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "ann_kmeanspp.cpp":
    pass

cdef extern from "AKM.cpp":
    pass

cdef extern from "AKM.h":
    cdef cppclass AKM:

        vector[vector[int]] Y
        vector[int] n_iter_
        vector[double] time_arr
        vector[int] cal_num_dist
        vector[vector[int]] dist_num_arr

        AKM() except +
        AKM(vector[vector[double]] &X, int c_true, bool debug) except +
        void opt(vector[vector[vector[double]]] &Cen, int ITER)
