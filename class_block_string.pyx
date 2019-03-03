# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 17:33:17 2019

@author: arwen
"""


cdef class CBlock(object):
    cdef readonly double left
    cdef readonly double right
    cdef readonly double top
    cdef readonly double bottom
    
    cdef readonly str text
    
    def __init__(self, 
                 double left, 
                 double right,
                 double top,
                 double bottom,
                 str text
                 ):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.text = text
    
    @property
    def width(self):
        return self.right - self.left
    
    @property
    def height(self):
        return self.bottom - self.top
    
    cpdef double cwidth(self): # callable from python AND c
        return self.right - self.left

    cdef double area(self):
        return (self.right - self.left) * (self.bottom - self.top)
		
    def print_area(self):
        print( self.area() )
        
cpdef bint is_left(CBlock block1, CBlock block2):
    return block1.left <= block2.left

cpdef bint is_above(CBlock block1, CBlock block2):
    return block1.top <= block2.top



def sorted_extract_above_and_left(CBlock block, all_blocks):
    cdef CBlock b
    result = []
    for b in all_blocks:
        if is_above(b, block) and is_left(b, block):
            result.append(b)
            
    result = sorted(result, key = lambda b:b.left)
            
    return result


