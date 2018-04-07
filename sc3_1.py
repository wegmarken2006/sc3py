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

class Primitive:
    def __init__(self, name: str, rate: Rate=Rate.RateKr, 
        inputs: List['Ugen']=[], outputs: List[Rate]=[], special=0, index=0) -> None:
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
    def __init__(self, ugens: List['Ugen']) -> None:
        self.ugens = ugens
        
class Mrg:
    def __init__(self, left: 'Ugen', right: 'Ugen') -> None:
        self.left = left
        self.right = right
        
class FromPortC:
    def __init__(self, port_nid) -> None:
        self.port_nid = port_nid
    
class FromPortK:
    def __init__(self, port_nid) -> None:
        self.port_nid = port_nid

class FromPortU:
    def __init__(self, port_nid, port_idx) -> None:
        self.port_nid = port_nid
        self.port_idx = port_idx
        
FromPort = Union[FromPortC, FromPortK, FromPortU]
        
Ugen = Union[Constant, Control, Primitive, Proxy, Mce, Mrg]

class NodeC:
    def __init__(self, nid, value) -> None:
        self.nid = nid
        self.value = value

class NodeK:
    def __init__(self, nid, name: str, 
                 default=0, rate: Rate=Rate.RateKr) -> None:
        self.nid = nid
        self.name = name
        self.rate = rate
        self.default = default
        
class NodeU:
    def __init__(self, nid, name: str, 
                 inputs: List[Ugen], outputs: List[int],
                 ugen_id, special=0, rate: Rate=Rate.RateKr) -> None:
        self.nid = nid
        self.name = name
        self.rate = rate
        self.inputs = inputs
        self.outputs = outputs
        self.special = special
        self.ugen_id = ugen_id
        
Node = Union[NodeC, NodeK, NodeU]

class Graph:
    def __init__(self, next_id, constants: List[NodeC],
                 controls: List[NodeK], ugens: List[NodeU]) -> None:
        self.next_id = next_id
        self.constants = constants
        self.controls = controls
        self.ugens = ugens
        


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
    return False
    
def max_rate(nums: List[Rate], start: Rate) -> Rate:
    max1 = start
    for elem in nums:
        if elem.value > max1.value:
            max1 = elem
    return max1

def max_num(nums: List[int], start: int) -> int:
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
            rates.append(rate_of(elem))
        return max_rate(rates, Rate.RateKr)
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        return rate_of(ugen.left)
    else:
        return Rate.RateKr
    
def mce_degree(ugen: Ugen) -> int:
    if isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        return len(ugen.ugens)
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        return mce_degree(ugen.left)
    else:
        raise Exception("mce_degree")
 
def mce_extend(n, ugen: Ugen) -> List[Ugen]:
    if isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        return extend(ugen.ugens, n)
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        ex: List[Ugen] = mce_extend(n, ugen.left)
        if len(ex) > 0:
            out: List[Ugen] = [ugen]
            out = out + ex[1:]
            return out
        else:
            raise Exception("mce_extend")    
    else:
        out2: List[Ugen] = []
        for ind in range(1, n+1):
            out2 = out2 + [ugen]
        return out2
 
def is_mce(ugen:Ugen) -> bool:
    if isinstance(ugen, Mce):
        return True
    else:
        return False
    
def transposer(ugens: List[List[Ugen]]) -> List[List[Ugen]]:
    len1 = len(ugens)
    len2 = len(ugens[0])
    out: List[List[Ugen]] = []
    for ind in range(0, len2):
        out.append([])
    for ind2 in range(0, len2):
        for ind1 in range(0, len1):
            out[ind2].append(ugens[ind1][ind2])
    return out
        
def mce_transform(ugen: Ugen) -> Ugen:
    if isinstance(ugen, Primitive):
        ins = filter(is_mce, ugen.inputs)
        degs: List[int] = []
        for elem in ins:
            degs = degs + [mce_degree(elem)]
        upr = max_num(degs, 0)
        ext: List[List[Ugen]] = []
        for elem in ugen.inputs:
            ext.append(mce_extend(upr, elem))
        iet: List[List[Ugen]] = transposer(ext)
        out: List[Ugen] = []
        p = ugen
        for elem2 in iet:
            p.inputs = elem2
            out.append(p)
        return Mce(ugens=out)
    else:
        raise Exception("mce_transform")


def mce_expand(ugen: Ugen) -> Ugen:
    if isinstance(ugen, Mce):
        ugen = cast(Mce, ugen)
        lst: List[Ugen] = []
        for elem in ugen.ugens:
            lst.append(mce_expand(elem))
        return Mce(ugens=lst)
    elif isinstance(ugen, Mrg):
        ugen = cast(Mrg, ugen)
        ug1: Ugen = mce_expand(ugen.left)
        return Mrg(left=ug1, right=ugen.right)
    else:
        def rec(ugen: Ugen) -> bool:
            if isinstance(ugen, Primitive):
                ins: List[bool] = filter(is_mce, ugen.inputs)
                return len(ins) != 0
            else:
                return False
        if rec(ugen):
            return mce_expand(mce_transform(ugen))
        else:
            return ugen
        
def mce_channel(n, ugen: Ugen) -> Ugen:
    if isinstance(ugen, Mce):
        return ugen.ugens[n]
    else:
        raise Exception("mce_channel")
        
def mce_channels(ugen: Ugen) -> List[Ugen]:
    if isinstance(ugen, Mce):
        return ugen.ugens
    elif isinstance(ugen, Mrg):
        lst = mce_channels(ugen.left)
        if len(lst) > 1:
            mrg1 = Mrg(left=lst[0], right=ugen.right)
            out: List[Ugen] = [mrg1]
            out = out + lst[1:]
            return out
        else:
            raise Exception("mce_channels")
    else:
        return [ugen]
    
def proxify(ugen: Ugen) -> Ugen:
    if isinstance(ugen, Mce):
        lst: List[Ugen] = []
        for elem in ugen.ugens:
            lst.append(proxify(elem))
        return Mce(ugens=lst)   
    elif isinstance(ugen, Mrg):
        prx = proxify(ugen.left)
        return Mrg(left=prx, right=ugen.right)
    elif isinstance(ugen, Primitive):
        ln = len(ugen.inputs)
        if ln < 2:
            return ugen
        else:
            lst1 = iota(ln, 0, 1)
            lst2: List[Ugen] = []
            for ind in lst1:
                lst2.append(Proxy(primitive=ugen, index=ind))
            return Mce(ugens=lst2)
    else:
        raise Exception("proxify")
    
    