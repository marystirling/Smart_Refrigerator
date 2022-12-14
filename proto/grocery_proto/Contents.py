# automatically generated by the FlatBuffers compiler, do not modify

# namespace: grocery_proto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Contents(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Contents()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsContents(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Contents
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Contents
    def Veggies(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from proto.grocery_proto.Veggies import Veggies
            obj = Veggies()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contents
    def Drinks(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from proto.grocery_proto.Drinks import Drinks
            obj = Drinks()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contents
    def Milk(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from proto.grocery_proto.Milk_Order import Milk_Order
            obj = Milk_Order()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contents
    def MilkLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Contents
    def MilkIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # Contents
    def Bread(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from proto.grocery_proto.Bread_Order import Bread_Order
            obj = Bread_Order()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contents
    def BreadLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Contents
    def BreadIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

    # Contents
    def Meat(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from proto.grocery_proto.Meat_Order import Meat_Order
            obj = Meat_Order()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contents
    def MeatLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Contents
    def MeatIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

def ContentsStart(builder): builder.StartObject(5)
def Start(builder):
    return ContentsStart(builder)
def ContentsAddVeggies(builder, veggies): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(veggies), 0)
def AddVeggies(builder, veggies):
    return ContentsAddVeggies(builder, veggies)
def ContentsAddDrinks(builder, drinks): builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(drinks), 0)
def AddDrinks(builder, drinks):
    return ContentsAddDrinks(builder, drinks)
def ContentsAddMilk(builder, milk): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(milk), 0)
def AddMilk(builder, milk):
    return ContentsAddMilk(builder, milk)
def ContentsStartMilkVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def StartMilkVector(builder, numElems):
    return ContentsStartMilkVector(builder, numElems)
def ContentsAddBread(builder, bread): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(bread), 0)
def AddBread(builder, bread):
    return ContentsAddBread(builder, bread)
def ContentsStartBreadVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def StartBreadVector(builder, numElems):
    return ContentsStartBreadVector(builder, numElems)
def ContentsAddMeat(builder, meat): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(meat), 0)
def AddMeat(builder, meat):
    return ContentsAddMeat(builder, meat)
def ContentsStartMeatVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def StartMeatVector(builder, numElems):
    return ContentsStartMeatVector(builder, numElems)
def ContentsEnd(builder): return builder.EndObject()
def End(builder):
    return ContentsEnd(builder)