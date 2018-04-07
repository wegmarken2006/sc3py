# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:31:52 2018

@author: Gigi
"""

import unittest
from typing import List
from sc3_1 import Ugen, Constant, Control, Rate, Primitive, Mce, Mrg, Proxy
from sc3_1 import extend, rate_of, mce_degree, mce_extend, mce_transform
from sc3_1 import mce_channels, proxify
from sc3_1 import NodeC, NodeK, NodeU, Graph, MMap
from sc3_1 import FromPort, FromPortC, FromPortK, FromPortU
from sc3_1 import node_c_value, node_k_default, mk_map
from sc3_1 import find_c_p, find_k_p, mk_node_c, mk_node_k, mk_node

ugens1: List[Ugen] = []
ugens1.append(Constant(value=1))
ugens1.append(Constant(value=3.3))
p1 = Primitive(rate=Rate.RateKr, name="P1", inputs=ugens1,	
               outputs=[Rate.RateKr, Rate.RateIr], index=0, special=0)
p2 = Primitive(rate=Rate.RateAr, name="P2")
mc1 = Mce(ugens=[p1, p1])
mc2 = Mce(ugens=[p1, p2])
mc3 = Mce(ugens=[p1, p2, mc1])
p3 = Primitive(name="P3", rate=Rate.RateKr, inputs=[mc1, mc3],
               outputs=[Rate.RateIr], special=0, index=0)
cs1 = Constant(11)
p4 = Primitive(rate = Rate.RateAr, name = "p4", inputs = [cs1, cs1],
                outputs=[Rate.RateIr], special=0, index=0)
#mc10 := mceTransform(p3)
#pp3 := mc10.(mce).ugens[2]
mg1 = Mrg(left = p1, right = mc1)
mg2 = Mrg(left = p2, right = p1)
mg3 = Mrg(left=mc1, right=p2)
ugens2 = extend(p1.inputs, 5)
ct1 = Control(rate=Rate.RateAr, name="Ct1")
exmg1 = mce_extend(3, mg1)
mc10 = mce_transform(p3)
mc11 = mce_channels(mg3)
mc12 = proxify(mc2)
nc1 = NodeC(nid = 10, value = 3)
nk1 = NodeK(nid = 11, default = 5, name = "nk1")
fpc1 = FromPortC(port_nid = 100)
fpk1 = FromPortK(port_nid = 101)
fpu1 = FromPortU(port_nid = 102, port_idx = 13)
ndc1 = NodeC(nid = 20, value = 320)
ndc2 = NodeC(nid = 21, value = 321)
ndk1 = NodeK(nid = 30, name = "ndk1")
ndk2 = NodeK(nid = 31, name = "ndk2")
ndu1 = NodeU(nid = 40, inputs = [mg1, mg2], outputs = [3,2,1],
              name = "ndu1", rate = Rate.RateAr, ugen_id = 2)

ndu2 = NodeU(nid = 41, inputs = [], outputs = [],
              name = "ndu2", rate = Rate.RateAr, ugen_id = 3)

gr1 = Graph(next_id=11, constants=[ndc1, ndc2], controls=[ndk1, ndk2],
            ugens=[ndu1, ndu2])
m1 = mk_map(gr1)
n1 = mk_node_c(Constant(value=320), gr1)
nn = n1[0]
ck1 = Control(name="ndk1", rate=Rate.RateKr, index=3)
n2 = mk_node_k(ck1, gr1)
nn2 = n2[0]
n3 = mk_node(Constant(320), gr1)
nn3 = n3[0]
n4 = mk_node(p4, gr1)
nn4 = n4[0]

class TestStringMethods(unittest.TestCase):
    

    def test(self):
        self.assertEqual(p1.name, "P1")
        self.assertEqual(p2.name, "P2")
        self.assertEqual(type(p3), Primitive)
        self.assertEqual(len(ugens2), 5)
        self.assertEqual(rate_of(ct1), Rate.RateAr)
        self.assertEqual(mce_degree(mc1), 2)
        self.assertEqual(len(exmg1), 3)
        self.assertEqual(type(mc10), Mce)
        self.assertEqual(type(mc10.ugens[2]), Primitive)
        self.assertEqual(mc10.ugens[2].name, "P3")
        self.assertEqual(len(mc11), 2)
        self.assertEqual(type(mc11[0]), Mrg)
        self.assertEqual(type(mc11[1]), Primitive)
        self.assertEqual(type(mc12.ugens[0]), Mce)
        self.assertEqual(type(mc12.ugens[1]), Primitive)
        self.assertEqual(node_c_value(nc1), 3)
        self.assertEqual(node_k_default(nk1), 5)
        self.assertEqual(m1.cs, [20, 21])
        self.assertEqual(m1.ks, [30, 31])
        self.assertEqual(m1.us, [40, 41])
        self.assertEqual(find_c_p(3, nc1), True)
        self.assertEqual(find_k_p("ndk1", ndk1), True)
        self.assertEqual(nn.nid, 20)
        self.assertEqual(nn2.nid, 30)
        self.assertEqual(nn3.nid, 20)
        self.assertEqual(nn4.name, "p4")
        

if __name__ == '__main__':
    unittest.main()