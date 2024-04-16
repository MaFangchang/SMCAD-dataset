from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from single_feature import (BaseSheet, FlangHole, Swelling, BendGroove, Rib, Rip, CommonHole, CommonGroove, Vent,
                            Array, ProfiledGroove, ProfiledArray, Bend, Roll, EarPlate)


class Compound(object):
    def __init__(self, flange_length, flange_width, flange_thickness, bend_radius, bend_height, bend1_radius,
                 bend1_height, bend2_radius, bend2_length, bend3_radius, bend3_height, bend3_width, bend4_radius,
                 bend4_height, bend4_width, bend5_radius, bend5_length, bend5_width):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend_radius = float(bend_radius)  # 折弯半径（外）
        self.bend_height = float(bend_height)  # 折弯高度，这里指边线法兰的长度
        self.bend1_radius = float(bend1_radius)  # 一次折弯的半径
        self.bend1_height = float(bend1_height)  # 一次折弯延伸的长度
        self.bend2_radius = float(bend2_radius)  # 二次折弯的半径
        self.bend2_length = float(bend2_length)  # 二次折弯延伸的长度
        self.bend3_radius = float(bend3_radius)  # 三次折弯的半径
        self.bend3_height = float(bend3_height)  # 三次折弯的高度
        self.bend3_width = float(bend3_width)  # 三次折弯的宽度
        self.bend4_radius = float(bend4_radius)  # 三次折弯的半径
        self.bend4_height = float(bend4_height)  # 三次折弯的高度
        self.bend4_width = float(bend4_width)  # 三次折弯的宽度
        self.bend5_radius = float(bend5_radius)  # 四次折弯的半径
        self.bend5_length = float(bend5_length)  # 四次折弯延伸的长度
        self.bend5_width = float(bend5_width)  # 四次折弯的宽度

    def compound(self):  # 先绘制单个特征，再组合
        base_sheet = BaseSheet(self.flange_length, self.flange_width, self.flange_thickness, self.bend_radius,
                               self.bend_height, self.bend1_radius, self.bend1_height, self.bend2_radius,
                               self.bend2_length, self.bend3_radius, self.bend3_height, self.bend3_width, 7, 1.8,
                               self.bend4_radius, self.bend4_height, self.bend4_width, 6.3, 2, self.bend5_radius,
                               self.bend5_length, self.bend5_width, 5.2, 1.5)
        flang_hole1 = FlangHole(self.flange_length, self.flange_width, self.flange_thickness,
                                self.bend4_radius, self.bend4_height, 4, 5.5, 1)
        flang_hole2 = FlangHole(self.flange_length, self.flange_width, self.flange_thickness,
                                self.bend4_radius, self.bend4_height, 5, 4.5, 1.1)
        swelling1 = Swelling(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius,
                             self.bend1_height, self.bend2_radius, self.bend2_length, self.bend3_radius,
                             self.bend3_height, self.bend3_width, 5, 6, 1.5)
        swelling2 = Swelling(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius,
                             self.bend1_height, self.bend2_radius, self.bend2_length, self.bend3_radius,
                             self.bend3_height, self.bend3_width, 4, 5, 1.4)
        bend_groove1 = BendGroove(self.flange_length, self.flange_width, self.flange_thickness, self.bend_radius,
                                  self.bend_height, 90, 3, 20, 28, 6, 1.5)
        bend_groove2 = BendGroove(self.flange_length, self.flange_width, self.flange_thickness, self.bend_radius,
                                  self.bend_height, 60, 4, 17, 30.5, 7, 1.4)
        rib1 = Rib(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius, self.bend1_height,
                   self.bend2_radius, self.bend2_length, self.bend3_radius, self.bend3_height, self.bend3_width,
                   7, 3)
        rib2 = Rib(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius, self.bend1_height,
                   self.bend2_radius, self.bend2_length, self.bend3_radius, self.bend3_height, self.bend3_width,
                   6, 4)
        rip1 = Rip(self.flange_length, self.flange_width, self.flange_thickness, 11.7, 8.4)
        rip2 = Rip(self.flange_length, self.flange_width, self.flange_thickness, 14.3, 6.2)
        common_hole1 = CommonHole(self.flange_length, self.flange_width, self.flange_thickness, self.bend4_radius,
                                  self.bend4_height, self.bend4_width, 4, 2)
        common_hole2 = CommonHole(self.flange_length, self.flange_width, self.flange_thickness, self.bend4_radius,
                                  self.bend4_height, self.bend4_width, 6, 2.5)
        common_groove1 = CommonGroove(self.flange_length, self.flange_width, self.flange_thickness, 27, 45, 9, 6)
        common_groove2 = CommonGroove(self.flange_length, self.flange_width, self.flange_thickness, 25, 60, 8, 5)
        vent1 = Vent(self.flange_length, self.flange_width, self.flange_thickness, 25, 45, 1.1, 2, (1, 1.5, 2))
        vent2 = Vent(self.flange_length, self.flange_width, self.flange_thickness, 20, 38, 0.8, 2.3, (0.8, 1, 1, 1.2))
        array1 = Array(self.flange_length, self.flange_width, self.flange_thickness, 7.6, 1.5, 38, 30, 1.2, (1, 10))
        array2 = Array(self.flange_length, self.flange_width, self.flange_thickness, 7, 1, 9.5, 60, 1, (4, 2))
        profiled_groove1 = ProfiledGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                          self.bend_radius, self.bend_height, self.bend5_radius, self.bend5_width,
                                          33, 4, 5, 4, 4)
        profiled_groove2 = ProfiledGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                          self.bend_radius, self.bend_height, self.bend5_radius, self.bend5_width,
                                          39, 3, 6, 6, 3)
        profiled_array1 = ProfiledArray(self.flange_length, self.flange_width, self.flange_thickness,
                                        self.bend_radius, self.bend_height, 32, 2, 2.8, 2.5, 5)
        profiled_array2 = ProfiledArray(self.flange_length, self.flange_width, self.flange_thickness,
                                        self.bend_radius, self.bend_height, 27, 5.2, 1.6, 2.3, 4)
        bend1 = Bend(self.flange_length, self.flange_width, self.flange_thickness, self.bend4_radius, self.bend4_height,
                     self.bend4_width, 2, 60, 10)
        bend2 = Bend(self.flange_length, self.flange_width, self.flange_thickness, self.bend4_radius, self.bend4_height,
                     self.bend4_width, 1.5, 180, 11)
        roll1 = Roll(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius,
                     self.bend1_height, self.bend2_radius, self.bend2_length, self.bend3_radius, self.bend3_height,
                     self.bend3_width, 300, 7.5, 6, 4)
        roll2 = Roll(self.flange_length, self.flange_width, self.flange_thickness, self.bend1_radius,
                     self.bend1_height, self.bend2_radius, self.bend2_length, self.bend3_radius, self.bend3_height,
                     self.bend3_width, 270, 9, 6.5, 5)
        ear_plate1 = EarPlate(self.flange_length, self.flange_width, self.flange_thickness, 8, 6, 5, 2)
        ear_plate2 = EarPlate(self.flange_length, self.flange_width, self.flange_thickness, 10, 8, 4, 3)

        # 复合特征
        compound = BRepAlgoAPI_Cut(base_sheet.feature_local(), flang_hole1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), flang_hole1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), flang_hole2.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), flang_hole2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), swelling1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), swelling1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), swelling2.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), swelling2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), bend_groove1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend_groove1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), bend_groove2.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend_groove2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rib1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), rib1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rib2.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), rib2.feature_local())

        # 简单减材特征
        compound = BRepAlgoAPI_Cut(compound.Shape(), rip1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rip2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_hole1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_hole2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_groove1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_groove2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), vent1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), vent2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), array1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), array2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_groove1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_groove2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_array1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_array2.feature_local())

        # 简单增材特征
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), roll1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), roll2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), ear_plate1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), ear_plate2.feature_local())

        return \
            compound.Shape(), base_sheet, flang_hole1, flang_hole2, swelling1, swelling2, bend_groove1, \
            bend_groove2, rib1, rib2, rip1, rip2, common_hole1, common_hole2, common_groove1, common_groove2, \
            vent1, vent2, array1, array2, profiled_groove1, profiled_groove2, profiled_array1, profiled_array2, \
            bend1, bend2, roll1, roll2, ear_plate1, ear_plate2
