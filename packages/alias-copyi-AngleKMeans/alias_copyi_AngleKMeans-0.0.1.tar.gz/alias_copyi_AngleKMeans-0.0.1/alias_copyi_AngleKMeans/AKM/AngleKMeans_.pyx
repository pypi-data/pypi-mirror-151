# distutils: language = c++

cimport numpy as np
import numpy as np
np.import_array()

from AngleKMeans_ cimport AngleKMeans

cdef class PyAngleKMeans:
    cdef AngleKMeans c_AngleKMeans

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, int debug):
        self.c_AngleKMeans = AngleKMeans(X, c_true, debug)

    def opt(self, np.ndarray[int, ndim=2] Y, int ITER):
        self.c_AngleKMeans.opt(Y, ITER)


    @property
    def y_pre(self):
        ret = self.c_AngleKMeans.Y
        return np.array(ret)

    @property
    def times(self):
        ret = self.c_AngleKMeans.time_arr
        return np.array(ret)

    @property
    def iters(self):
        ret = self.c_AngleKMeans.iter_arr
        return np.array(ret)
    
    @property
    def cal_num_dist(self):
        return np.array(self.c_AngleKMeans.dist_num_total)

    @property
    def dist_num_arr(self):
        return np.array(self.c_AngleKMeans.dist_num_arr)

