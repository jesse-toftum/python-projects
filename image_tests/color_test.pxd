from cpython cimport bool

cdef class ImageGeneration:
    cdef public int seeds, random_seed, dim_x, dim_y
    cdef public double power, radius
    cdef public bool progress_bar