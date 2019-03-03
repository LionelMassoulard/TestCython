# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:24:36 2019

@author: arwen
"""

import sys
sys.path.append(r"E:\DocumentsWindows7\Python Scripts\TestCython\cython_package")


import numpy as np
import pandas as pd

def gen_random(n = 1000):
    all_blocks = []
    for _ in range(n):
        
        left,right,top,bottom = np.random.rand(4)
        
        block = {}
        block["left"] = min(left,right)
        block["right"] = max(left,right)
        block["top"] = min(top, bottom)
        block["bottom"] = max(top, bottom)
        
        all_blocks.append(block)
        
    return all_blocks

# In[]

import hello
assert hello.mafonction(12,45) == 61

# In[]
import pyximport
pyximport.install(reload_support=True)
from importlib import reload

import hello
reload(hello)

print(hello.mydouble(3.3))


# In[] : 
class Block(object):
    def __init__(self, left,right,bottom,top):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        
        
    def width(self):
        return self.right - self.left
    
    def height(self):
        return self.bottom - self.top
    
    
def python_is_left_of(b1,b2):
    return b1.left <= b2.left

def python_is_above_of(b1,b2):
    return b1.top <= b2.top

def python_extract_above_and_left(block, all_blocks):
    result = []
    for b in all_blocks:
        if python_is_above_of(b, block) and python_is_left_of(b, block):
            result.append(b)
            
    return result
    
# In[]
        
all_blocks = gen_random()
dico_block = all_blocks[0]


cblock = Block(**dico_block)
cblock.height()

# In[]
import pytest

import pyximport
pyximport.install(reload_support=True)
from importlib import reload

import class_block
reload(class_block)


cblock = class_block.CBlock(**dico_block)
cblock.height()

print( cblock.cwidth() )
print( cblock.width() )

cblock.left
cblock.right

with pytest.raises(AttributeError):
    cblock.top
    


with pytest.raises(AttributeError):
    cblock.area() # 

cblock.print_area()


cblock2 = class_block.CBlock(**all_blocks[1])
class_block.python_delta_left(cblock, cblock2)


class_block.is_left(cblock, cblock2)

class_block.compute_sum([cblock,cblock2])

class_block.extract_above_and_left(cblock,[cblock,cblock2])

class_block.sorted_extract_above_and_left(cblock,[cblock,cblock2])

# In[] : time test

from class_block import (CBlock, 
                         is_left, 
                         compute_sum,
                         extract_above_and_left,
                         sorted_extract_above_and_left)



np.random.seed(123)
all_dico_blocks = gen_random(10000)
all_Blocks  = [Block(**b) for b in all_dico_blocks]
all_CBlocks = [CBlock(**b) for b in all_dico_blocks]

def compute1(all_Blocks):
    s = 0
    for b1 in all_Blocks:
        for b2 in all_Blocks:
            r = python_is_left_of(b1,b2)
            if r:
                s += 1
                
    return s

def compute2(all_CBlocks):
    s = 0
    for b1 in all_CBlocks:
        for b2 in all_CBlocks:
            r = is_left(b1,b2)
            if r:
                s += 1
                
    return s

pd_all_blocks = pd.DataFrame(all_dico_blocks).loc[:,("left","right","top","bottom")]
np_all_blocks = pd_all_blocks.values

def compute3(np_all_blocks):
    s = 0
    for i in range(np_all_blocks.shape[0]):
        for j in range(np_all_blocks.shape[0]):
            if np_all_blocks[i,0] <= np_all_blocks[j,0]:
                s += 1
    return s

from numba import jit

compute4 = jit(compute3)

 


# In[]
from time import time

start = time()
s1 = compute1(all_Blocks)
stop = time()
print("Python ", stop - start) # 30 secs

start = time()
s2 = compute2(all_CBlocks)
stop= time()
print("Cython ",stop - start) # 15 secs

start = time()
s3 = compute3(np_all_blocks)
stop= time()
print("python np ",stop - start) #50sec


start = time()
s4 = compute4(np_all_blocks)
stop= time()
print("numba np ",stop - start) #0.34

start = time()
s5 = compute_sum(all_CBlocks) 
stop= time()
print("cython cython ",stop - start) #0.57

# In[] :
block = all_Blocks[0]
start = time()
for _ in range(1000):
    extract = python_extract_above_and_left(block, all_Blocks)

end = time()
print("extract python ", end - start)


block = all_Blocks[0]
start = time()
for _ in range(1000):
    extract = sorted(python_extract_above_and_left(block, all_Blocks),key=lambda b:b.left)
end = time()
print("sorted extract python ", end - start)



block = all_CBlocks[0]
start = time()
for _ in range(1000):
    extract = extract_above_and_left(block, all_CBlocks)
end = time()
print("extract cython ", end - start)

block = all_CBlocks[0]
start = time()
for _ in range(1000):
    extract = sorted_extract_above_and_left(block, all_CBlocks)
end = time()
print("sorted extract cython ", end - start)



# In[] : test string
import pyximport
pyximport.install(reload_support=True)
from importlib import reload

import class_block_string
reload(class_block_string)

block = class_block_string.CBlock(left=0.1,right=0.20,top=0.75,bottom=0.95,text="toto")

block.height
block.width
block.text

all_CBlocks = [class_block_string.CBlock(text="this is toto",**b) for b in all_dico_blocks]

block = all_CBlocks[0]
start = time()
for _ in range(1000):
    extract = class_block_string.sorted_extract_above_and_left(block, all_CBlocks)
end = time()
print("sorted extract cython ", end - start)





