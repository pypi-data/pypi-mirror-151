from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "ball_kmeans++_xd.cpp":
    pass

cdef extern from "BKM.cpp":
    pass

cdef extern from "BKM.h":
    cdef cppclass BKM:

        vector[vector[int]] Y
        vector[int] n_iter_
        vector[double] time_arr
        vector[int] cal_num_dist
        vector[vector[int]] dist_num_arr

        BKM() except +
        BKM(vector[vector[double]] &X, int c_true, bool debug) except +
        void opt(vector[vector[vector[double]]] &Cen, bool isRing, int ITER)
