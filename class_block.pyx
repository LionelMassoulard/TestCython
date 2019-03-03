# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:56:38 2019

@author: arwen
"""


cdef class CBlock(object):
    cdef readonly double left
    cdef public double right
    cdef double top
    cdef public double bottom

    
    def __init__(self, 
                 double left, 
                 double right,
                 double top,
                 double bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def width(self):
        return self.right - self.left
    
    def height(self):
        return self.bottom - self.top
    
    cpdef double cwidth(self): # callable from python AND c
        return self.right - self.left

    cdef double area(self):
        return (self.right - self.left) * (self.bottom - self.top)
		
    def print_area(self):
        print( self.area() ) #
	
        
cdef double delta_left(CBlock block1, CBlock block2):
    return block1.left - block2.left

def python_delta_left(CBlock b1, CBlock b2):
    return delta_left(b1,b2)
    
    
cpdef bint is_left(CBlock block1, CBlock block2):
    return block1.left <= block2.left

cpdef bint is_above(CBlock block1, CBlock block2):
    return block1.top <= block2.top

cpdef int compute_sum(list_blocks):
    cdef CBlock block1
    cdef CBlock block2
    
    cdef int i
    cdef int j
    
    cdef int s = 0
    for block1 in list_blocks:
        for block2 in list_blocks:
            if is_left(block1,block2):
                s += 1
    return s


def extract_above_and_left(CBlock block,all_blocks):
    cdef CBlock b
    result = []
    for b in all_blocks:
        if is_above(b, block) and is_left(b, block):
            result.append(b)
            
    return result

cdef double get_left(CBlock b):
    return b.left

def sorted_extract_above_and_left(CBlock block,all_blocks):
    cdef CBlock b
    result = []
    for b in all_blocks:
        if is_above(b, block) and is_left(b, block):
            result.append(b)
           
    result = sorted(result, key = get_left)
    return result
