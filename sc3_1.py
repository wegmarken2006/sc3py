# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 20:58:43 2018

@author: Gigi
"""
from typing import Union, cast, List, Tuple
from enum import Enum
from osc_1 import *
import ugens

uid = 0

def next_uid():
    global uid
    uid = uid + 1
    return uid


class Rate(Enum):
    RateIr = 0
    RateKr = 1
    RateAr = 2
    RateDr = 3


class Constant:
    def __init__(self, value):
        self.value = value


class Primitive:
    def __init__(self, name: str, rate: Rate = Rate.RateKr,
                 inputs: List['Ugen'] = [], outputs: List[Rate] = [], special=0, index=0) -> None:
        self.rate = rate
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.special = special
        self.index = index


class Control:
    def __init__(self, name: str, rate: Rate = Rate.RateKr, index=0) -> None:
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

Ugen = Union[Constant, Control, Primitive, Proxy, Mce, Mrg, FromPort]


class NodeC:
    def __init__(self, nid, value) -> None:
        self.nid = nid
        self.value = value


class NodeK:
    def __init__(self, nid, name: str,
                 default=0, rate: Rate = Rate.RateKr) -> None:
        self.nid = nid
        self.name = name
        self.rate = rate
        self.default = default


class NodeU:
    def __init__(self, nid, name: str,
                 inputs: List[Ugen], outputs: List[int],
                 ugen_id, special=0, rate: Rate = Rate.RateKr) -> None:
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


class MMap:
    def __init__(self, cs: List[int], ks: List[int], us: List[int]) -> None:
        self.cs = cs
        self.ks = ks
        self.us = us


class Input:
    def __init__(self, u: int, p: int) -> None:
        self.u = u
        self.p = p


def template(ugen: Ugen):
    if isinstance(ugen, Constant):
        # ugen = cast(Constant, ugen)
        pass
    elif isinstance(ugen, Control):
        pass
    elif isinstance(ugen, Primitive):
        pass
    elif isinstance(ugen, Proxy):
        pass
    elif isinstance(ugen, Mce):
        pass
    elif isinstance(ugen, Mrg):
        pass
    else:
        pass


def iota(n, init, step) -> List[int]:
    if n == 0:
        return []
    else:
        out = [init]
        out = out + iota(n - 1, init + step, step)
        return out


def extend(ugens: List[Ugen], newlen: int) -> List[Ugen]:
    ln = len(ugens)
    out: List[Ugen] = []
    if ln > newlen:
        out = ugens[0:newlen]
    else:
        out = ugens + ugens
        return extend(out, newlen)
    return out


def rate_id(rate: Rate) -> int:
    if rate == Rate.RateIr:
        return 0
    elif rate == Rate.RateKr:
        return 1
    elif rate == Rate.RateAr:
        return 2
    elif rate == Rate.RateDr:
        return 3
    return 0


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
        for ind in range(1, n + 1):
            out2 = out2 + [ugen]
        return out2


def is_mce(ugen: Ugen) -> bool:
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
        ins = [elem for elem in filter(is_mce, ugen.inputs)]
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
                in1: List[Ugen] = [elem for elem in filter(is_mce, ugen.inputs)]
                return len(in1) != 0
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
        ln = len(ugen.outputs)
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


def mk_ugen(name, inputs: List[Ugen], outputs: List[Rate], ind=0, sp=0,
            rate: Rate = Rate.RateKr):
    pr1 = Primitive(name=name, rate=rate, inputs=inputs,
                    outputs=outputs, special=sp, index=ind)
    return proxify(mce_expand(pr1))


def node_c_value(node: NodeC):
    return node.value


def node_k_default(node: NodeK):
    return node.default


def mk_map(graph: Graph) -> MMap:
    cs: List[int] = []
    ks: List[int] = []
    us: List[int] = []
    for el1 in graph.constants:
        cs.append(el1.nid)
    for el2 in graph.controls:
        ks.append(el2.nid)
    for el3 in graph.ugens:
        us.append(el3.nid)
    return MMap(cs=cs, ks=ks, us=us)


def fetch(val: int, lst: List[int]) -> int:
    for ind, elem in enumerate(lst):
        if elem == val:
            return ind
    raise Exception("fetch")


def find_c_p(val, node: Node) -> bool:
    if isinstance(node, NodeC):
        return val == node.value
    raise Exception("find_c_p")


def push_c(val, gr: Graph) -> Tuple[Node, Graph]:
    node = NodeC(nid=gr.next_id + 1, value=val)
    consts: List[NodeC] = [node]
    consts = consts + gr.constants
    gr1 = Graph(next_id=gr.next_id + 1, constants=consts, controls=gr.controls,
                ugens=gr.ugens)
    return node, gr1


def mk_node_c(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    if isinstance(ugen, Constant):
        val = ugen.value
        for nd in gr.constants:
            if find_c_p(val, nd):
                return nd, gr
        return push_c(val, gr)
    else:
        raise Exception("make_node_c")


def find_k_p(st: str, node: Node) -> bool:
    if isinstance(node, NodeK):
        return st == node.name
    raise Exception("find_k_p")


def push_k_p(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    if isinstance(ugen, Control):
        node = NodeK(nid=gr.next_id + 1, name=ugen.name, default=ugen.index,
                     rate=ugen.rate)
        contrs = [node]
        contrs = contrs + gr.controls
        gr1 = Graph(next_id=gr.next_id + 1, constants=gr.constants,
                    controls=contrs, ugens=gr.ugens)
        return node, gr1
    else:
        raise Exception("push_k_p")


def mk_node_k(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    if isinstance(ugen, Control):
        name = ugen.name
        for node in gr.controls:
            if find_k_p(name, node):
                return node, gr
        return push_k_p(ugen, gr)
    else:
        raise Exception("mk_node_k")


def find_u_p(ugen: Primitive, node: Node) -> bool:
    if isinstance(node, NodeU):
        b1 = node.rate == ugen.rate
        b2 = node.name == ugen.name
        b3 = node.ugen_id == ugen.index
        b4 = node.outputs == ugen.outputs
        b5 = node.special == ugen.special
        if b1 and b2 and b3 and b4 and b5:
            for ind, elem in enumerate(node.inputs):
                if not (elem.port_nid == ugen.inputs[ind].port_nid):
                    return False
            return True
        else:
            return False
    raise Exception("find_u_p")


def push_u(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    if isinstance(ugen, Primitive):
        #intrates = [elem for elem in map(rate_id, ugen.outputs)]
        node = NodeU(nid=gr.next_id + 1, name=ugen.name, rate=ugen.rate,
                     inputs=ugen.inputs, outputs=ugen.outputs, special=ugen.special,
                     ugen_id=ugen.index)
        ugens = [node]
        ugens = ugens + gr.ugens
        gr1 = Graph(next_id=gr.next_id + 1, constants=gr.constants,
                    controls=gr.controls, ugens=ugens)
        return node, gr1

    else:
        raise Exception("push_u")


def as_from_port(node: Node) -> Ugen:
    if isinstance(node, NodeC):
        return FromPortC(port_nid=node.nid)
    elif isinstance(node, NodeK):
        return FromPortK(port_nid=node.nid)
    elif isinstance(node, NodeU):
        return FromPortU(port_nid=node.nid, port_idx=0)


def mk_node_u(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    def acc(ll: List[Ugen], nn: List[Node], gr: Graph) -> Tuple[List[Node], Graph]:
        if len(ll) == 0:
            nn.reverse()
            return nn, gr
        else:
            ng = mk_node(ll[0], gr)
            ng1 = ng[0]
            ng2 = ng[1]
            nn = [ng1] + nn
            return acc(ll[1:], nn, ng2)

    if isinstance(ugen, Primitive):
        ng = acc(ugen.inputs, [], gr)
        gnew = ng[1]
        ng1 = ng[0]
        inputs2: List[Ugen] = []
        for nd in ng1:
            inputs2.append(as_from_port(nd))
        pr = Primitive(name=ugen.name, rate=ugen.rate, inputs=inputs2,
                       outputs=ugen.outputs, index=ugen.index, special=ugen.special)
        for nd2 in gnew.ugens:
            if find_u_p(ugen=pr, node=nd2):
                return nd2, gnew

        tup: Tuple[Node, Graph] = push_u(pr, gnew)
        return tup
    else:
        raise Exception("mk_node_u")


def mk_node(ugen: Ugen, gr: Graph) -> Tuple[Node, Graph]:
    if isinstance(ugen, Constant):
        return mk_node_c(ugen, gr)
    elif isinstance(ugen, Control):
        return mk_node_k(ugen, gr)
    elif isinstance(ugen, Primitive):
        return mk_node_u(ugen, gr)
    elif isinstance(ugen, Mrg):
        gn = mk_node(ugen.right, gr)
        g1 = gn[1]
        return mk_node(ugen.left, g1)
    elif isinstance(ugen, Mce):
        raise Exception("mk_node - Mce")
    elif isinstance(ugen, Proxy):
        raise Exception("mk_node - proxy")
    else:
        raise Exception("mk_node - other")



def implicit(num):
    rates: List[Rate] = []
    for ind in range(1, num + 1):
        rates.append(Rate.RateKr)
    node = NodeU(nid=-1, name="Control", inputs=[], outputs=rates, ugen_id=0, special=0, rate=Rate.RateKr)
    return node


def mrg_n(lst: List[Ugen]):
    if len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return Mrg(left=lst[0], right=lst[1])
    else:
        return Mrg(left=lst[0], right=mrg_n(lst[1:]))


def prepare_root(ugen: Ugen):
    if isinstance(ugen, Mce):
        return mrg_n(ugen.ugens)
    elif isinstance(ugen, Mrg):
        return Mrg(left=prepare_root(ugen.left), right=prepare_root(ugen.right))
    else:
        return ugen


def empty_graph() -> Graph:
    return Graph(0, [], [], [])


def synth(ugen: Ugen) -> Graph:
    root = prepare_root(ugen)
    gn = mk_node(root, empty_graph())
    gr = gn[1]
    cs = gr.constants
    ks = gr.controls
    us = gr.ugens
    us1 = us
    us1.reverse()
    if len(ks) != 0:
        us1 = [implicit(len(ks))] + us1
    grout = Graph(next_id=-1, constants=cs, controls=ks, ugens=us1)
    return grout


def encode_node_k(mm: MMap, node: NodeK) -> bytes:
    return str_pstr(node.name) + encode_i16(fetch(node.nid, mm.ks))


def encode_input(inp: Input) -> bytes:
    out = encode_i16(inp.u) + encode_i16(inp.p)
    return out


def make_input(mm: MMap, fp: Ugen) -> Input:
    if isinstance(fp, FromPortC):
        p = fetch(fp.port_nid, mm.cs)
        return Input(u=-1, p=p)
    elif isinstance(fp, FromPortK):
        p = fetch(fp.port_nid, mm.ks)
        return Input(u=0, p=p)
    if isinstance(fp, FromPortU):
        u = fetch(fp.port_nid, mm.us)
        return Input(u=u, p=fp.port_idx)
    else:
        raise Exception("make_input")


def encode_node_u(mm: MMap, nu: NodeU) -> bytes:
    def f1(ug: Ugen) -> Input:
        return make_input(mm, ug)

    l1 = [elem for elem in map(f1, nu.inputs)]
    i2 = [elem for elem in map(encode_input, l1)]
    intrates = [elem for elem in map(rate_id, nu.outputs)]
    o2 = [elem for elem in map(encode_i8, intrates)]
    a1 = str_pstr(nu.name)
    a2 = encode_i8(rate_id(nu.rate))
    a3 = encode_i16(len(nu.inputs))
    a4 = encode_i16(len(nu.outputs))
    a5 = encode_i16(nu.special)
    return a1 + a2 + a3 + a4 + a5 + b''.join(i2) + b''.join(o2)


def encode_graphdef(name: str, graph: Graph) -> bytes:
    mm = mk_map(graph)
    a1 = encode_str("SCgf")
    a2 = encode_i32(0)
    a3 = encode_i16(1)
    a4 = str_pstr(name)
    a41 = encode_i16(len(graph.constants))
    l1 = [elem for elem in map(node_c_value, graph.constants)]
    a5 = [elem for elem in map(encode_f32, l1)]
    a6 = encode_i16(len(graph.controls))
    l2 = [elem for elem in map(node_k_default, graph.controls)]
    a7 = [elem for elem in map(encode_f32, l2)]
    a8 = encode_i16(len(graph.controls))

    def f1(ks: NodeK) -> bytes:
        return encode_node_k(mm, ks)

    a9 = [elem for elem in map(f1, graph.controls)]
    a10 = encode_i16(len(graph.ugens))

    def f2(us: NodeU) -> bytes:
        return encode_node_u(mm, us)

    a11 = [elem for elem in map(f2, graph.ugens)]
    return a1 + a2 + a3 + a4 + a41 + b''.join(a5) + a6 + b''.join(a7) + a8 + b''.join(a9) + a10 + b''.join(a11)


def synthdef(name: str, ugen: Ugen) -> bytes:
    graph: Graph = synth(ugen)
    return encode_graphdef(name, graph)


def mk_osc_mce(rate: Rate, name: str, inputs: List[Ugen], ugen: Ugen, ou: int) -> Ugen:
    rl: List[Rate] = []
    for ii in range(0, ou):
        rl.append(rate)
    return mk_ugen(name=name, inputs=inputs + mce_channels(ugen), outputs=rl, ind=0, sp=0, rate=rate)


def mk_osc_id(rate: Rate, name: str, inputs: List[Ugen], ou: int) -> Ugen:
    rl: List[Rate] = []
    for ii in range(0, ou):
        rl.append(rate)
    return mk_ugen(name=name, inputs=inputs, outputs=rl, ind=next_uid(), sp=0, rate=rate)


def mk_oscillator(rate: Rate, name: str, inputs: List[Ugen], ou: int) -> Ugen:
    rl: List[Rate] = []
    for ii in range(0, ou):
        rl.append(rate)
    return mk_ugen(name=name, inputs=inputs, outputs=rl, ind=0, sp=0, rate=rate)


def mk_filter(name: str, inputs: List[Ugen], ou: int, sp: int = 0) -> Ugen:
    rates = [elem for elem in map(rate_of, inputs)]
    maxrate = max_rate(rates, Rate.RateIr)
    ou_list: List[Rate] = []
    for _ in range(0, ou):
        ou_list.append(maxrate)
    return mk_ugen(name=name, inputs=inputs, outputs=ou_list, ind=0, sp=sp, rate=maxrate)

def mk_filter_id(name: str, inputs: List[Ugen], ou: int, sp: int = 0) -> Ugen:
    rates = [elem for elem in map(rate_of, inputs)]
    maxrate = max_rate(rates, Rate.RateIr)
    ou_list: List[Rate] = []
    for _ in range(0, ou):
        ou_list.append(maxrate)
    return mk_ugen(name=name, inputs=inputs, outputs=ou_list, ind=next_uid(), sp=sp, rate=maxrate)

def mk_filter_mce(name: str, inputs: List[Ugen], ugen: Ugen, ou: int) -> Ugen:
    return mk_filter(name=name, inputs=inputs + mce_channels(ugen), ou=ou)


def mk_operator(name: str, inputs: List[Ugen], sp: int = 0) -> Ugen:
    rates = [elem for elem in map(rate_of, inputs)]
    maxrate = max_rate(rates, Rate.RateIr)
    return mk_ugen(name=name, inputs=inputs, outputs=[maxrate], ind=0, sp=sp, rate=maxrate)


def mk_unary_operator(sp: int, fun, op) -> Ugen:
    if isinstance(op, Constant):
        return Constant(fun(op.value))
    elif type(op) == int or type(op) == float:
        op = Constant(value=op)
    return mk_operator("UnaryOpUGen", [op], sp)


def mk_binary_operator(sp: int, fun, op1, op2) -> Ugen:
    if isinstance(op1, Constant) and isinstance(op2, Constant):
        return Constant(fun(op1.value, op2.value))
    elif type(op1) == int or type(op1) == float:
        op1 = Constant(value=op1)
    elif type(op2) == int or type(op2) == float:
        op2 = Constant(value=op2)
    return mk_operator("BinaryOpUGen", [op1, op2], sp)


def sc_start():
    osc_setport(57110)
    msg1 = Message(name="/notify", ldatum=[1])
    send_message(msg1)
    msg1 = Message(name="/g_new", ldatum=[1, ADD_TO_TAIL, 0])
    send_message(msg1)


def sc_stop():
    msg1 = Message(name="/g_deepFree", ldatum=[0])
    send_message(msg1)


def sc_play(ugen):
    name = "anonymous"
    if isinstance(ugen, List):
         ugen = Mce(ugens=ugen)
    synd = synthdef(name, ugens.out(0, ugen))
    msg1 = Message(name="/d_recv", ldatum=[synd])
    send_message(msg1)
    msg1 = Message(name="/s_new", ldatum=[name, -1, ADD_TO_TAIL, 1])
    send_message(msg1)
