from libcpp.vector cimport vector

cdef extern from "AngleKMeans.cpp":
    pass

cdef extern from "AngleKMeans.h":
    cdef cppclass AngleKMeans:

        vector[vector[int]] Y
        vector[vector[int]] dist_num_arr
        vector[int] dist_num_total
        vector[double] time_arr
        vector[int] iter_arr

        AngleKMeans() except +
        AngleKMeans(vector[vector[double]]& X, int c_true, int debug) except +
        void opt(vector[vector[int]]& Y, int ITER)
