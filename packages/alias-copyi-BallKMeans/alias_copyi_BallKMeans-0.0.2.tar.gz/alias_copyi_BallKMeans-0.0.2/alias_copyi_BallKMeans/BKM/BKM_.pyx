cimport numpy as np
import numpy as np
np.import_array()

from .BKM_ cimport BKM

cdef class PyBKM:
    cdef BKM c_BKM

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, bool debug=False):
        self.c_BKM = BKM(X, c_true, debug)

    def opt(self, Cen, bool isRing, int ITER=300):

        self.c_BKM.opt(Cen, isRing, ITER)

    @property
    def y_pre(self):
        return np.array(self.c_BKM.Y)
    
    @property
    def n_iter_(self):
        return np.array(self.c_BKM.n_iter_)

    @property
    def cal_num_dist(self):
        return np.array(self.c_BKM.cal_num_dist)

    @property
    def dist_num_arr(self):
        return np.array(self.c_BKM.dist_num_arr)

    @property
    def time_arr(self):
        return np.array(self.c_BKM.time_arr)