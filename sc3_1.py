# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 20:58:43 2018

@author: Gigi
"""
from typing import Union, cast, List
from enum import Enum


class Rate(Enum):
    RateKr = 0
    RateIr = 1
    RateAr = 2
    RateDr = 3

class Constant:
    def __init__(self, value):
        self.value = value

Ugen = Union[Constant]

class Primitive:
    def __init__(self, name: str, rate: Rate=Rate.RateKr, 
        inputs: List[Ugen]=[], outputs: List[Rate]=[], special=0, index=0) -> None:
        self.rate = rate
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.special = special
        self.index = index

class Control:
    def __init__(self, name: str, rate: Rate=Rate.RateKr, index=0) -> None:
        self.rate = rate
        self.name = name
        self.index = index
        
        
class Proxy:
    def __init__(self, primitive: Primitive, index=0) -> None:
        self.primitive = primitive
        self.index = index

class Mce:
    def __init__(self, ugens: List[Ugen]) -> None:
        self.ugens = ugens
        
class Mrg:
    def __init__(self, left: Ugen, right: Ugen) -> None:
        self.left = left
        self.right = right
        
        
Ugen = Union[Constant, Control, Primitive, Proxy, Mce, Mrg]

def template(ugen: Ugen):
    if isinstance(ugen, Constant):
        ugen = cast(Constant, ugen)
        pass
    elif isinstance(ugen, Control):
        ugen = cast(Control, ugen)
        pass
    elif isinstance(ugen, Primitive):
        ugen = cast(Primitive, ugen)
        pass
    elif isinstance(ugen, Proxy):
        ugen = cast(Proxy, ugen)
        pass
    elif isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        pass
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        pass
    else:
        pass

def iota(n, init, step) -> List[int]:
    if n == 0:
        return []
    else:
        out = [init]
        out = out + iota(n-1, init+step, step)
        return out
    
def extend(ugens: List[Ugen], newlen) -> List[Ugen]:
    ln = len(ugens)
    out: List[Ugen] = []
    if ln > newlen:
        out = ugens[0:newlen]
    else: 
        out = ugens + ugens
        return extend(out, newlen)
    return out
    
    
def is_sink(ugen: Ugen) -> bool:
    if isinstance(ugen, Primitive):
        ugen = cast(Primitive, ugen)
        if len(ugen.inputs) == 0:
            return True
        else:
            return False
    elif isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        for elem in ugen.ugens:
            if is_sink(elem):
                return True
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        if is_sink(ugen.left):
            return True
    else:
        return False
    
def max_num(nums: List[int], start):
    max1 = start
    for elem in nums:
        if elem > max1:
            max1 = elem
    return max1

def rate_of(ugen: Ugen) -> Rate:
    if isinstance(ugen, Control):
        ugen = cast(Control, ugen)
        return ugen.rate
    elif isinstance(ugen, Primitive):
        ugen = cast(Primitive, ugen)
        return ugen.rate
    elif isinstance(ugen, Proxy):
        ugen = cast(Proxy, ugen)
        return ugen.primitive.rate
    elif isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        rates: List[Rate] = []
        for elem in ugen.ugens:
            rates = rates + rate_of(elem)
        return max_num(rates, Rate.RateKr)
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        return rate_of(ugen.left)
    else:
        return Rate.RateKr
    

