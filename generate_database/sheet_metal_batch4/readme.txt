21504~28671减材特征都在基体法兰和折弯上

single_feature.py文件是生成单个特征的脚本；
main.py文件是生成组合体并转成step文件的脚本；
label.py文件是生成面标签的脚本；
feature_test.py文件是将全部28个特征组合到一起的脚本，目的是看看特征有没有干涉，以及所有面的面心有没有重合；
label_test.py文件是测试面标签是否合理的脚本；
display_feature_test.py文件是测试所有特征是否出现干涉的脚本。


第四批每个特征的尺寸和位置参数
        bend = Bend(self.flange_length, self.flange_width, self.flange_thickness,
                    self.bend_radius, self.bend_height, 90)
        flang_hole1 = FlangHole(self.flange_length, self.flange_width, self.flange_thickness,
                                self.bend_radius, self.bend_height, 4, 6, 1.1)
        flang_hole2 = FlangHole(self.flange_length, self.flange_width, self.flange_thickness,
                                self.bend_radius, self.bend_height, 3, 7, 1.1)
        swelling1 = Swelling(self.flange_length, self.flange_width, self.flange_thickness,
                             self.bend_radius, self.bend_height, 8, 5, 1.3)
        swelling2 = Swelling(self.flange_length, self.flange_width, self.flange_thickness,
                             self.bend_radius, self.bend_height, 7, 6, 1.3)
        bend_groove1 = BendGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                  85, 4.5, 22, 31, 9, 2, 45.5)
        bend_groove2 = BendGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                  100, 4, 26, 37, 8, 2.5, 42.5)
        profiled_groove1 = ProfiledGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                          95, 3.6, 29, 31.5, 32.7, 9.4, 5.4)
        profiled_groove2 = ProfiledGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                          105, 4.8, 31.5, 29, 29.9, 8.2, 6.6)
        rib1 = Rib(self.flange_length, self.flange_width, self.flange_thickness, 90, 2.6, 25.7, 32.3, 7.8, 3.2, 14.5)
        rib2 = Rib(self.flange_length, self.flange_width, self.flange_thickness, 80, 3.3, 33.9, 27.5, 6.2, 4.3, 11.6)
        rip1 = Rip(self.flange_length, self.flange_width, self.flange_thickness, 10.6, 8.1, 12)
        rip2 = Rip(self.flange_length, self.flange_width, self.flange_thickness, 8.5, 6.6, 71)
        common_hole1 = CommonHole(self.flange_length, self.flange_width, self.flange_thickness, 24.5, 2.6)
        common_hole2 = CommonHole(self.flange_length, self.flange_width, self.flange_thickness, 17, 3.5)
        common_groove1 = CommonGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                      self.bend_radius, self.bend_height, 19.5, 60, 11, 6.2)
        common_groove2 = CommonGroove(self.flange_length, self.flange_width, self.flange_thickness,
                                      self.bend_radius, self.bend_height, 19.5, 60, 11, 6.2)
        vent1 = Vent(self.flange_length, self.flange_width, self.flange_thickness, 42, 27, 0.9, 2.1, (0.8, 0.9, 1, 1.1))
        vent2 = Vent(self.flange_length, self.flange_width, self.flange_thickness, 45, 28, 1.3, 2.5, (1, 1.6, 2.2))
        array1 = Array(self.flange_length, self.flange_width, self.flange_thickness,
                       self.bend_radius, self.bend_height, 6, 2, 1, (5, 3))
        array2 = Array(self.flange_length, self.flange_width, self.flange_thickness,
                       self.bend_radius, self.bend_height, 6, 2, 1, (5, 3))
        bend1 = Bend2(self.flange_length, self.flange_width, self.flange_thickness,
                      self.bend_radius, self.bend_height, 15, 90)
        bend2 = Bend2(self.flange_length, self.flange_width, self.flange_thickness,
                      self.bend_radius, self.bend_height, 14, 100)
        hem1 = Hem(self.flange_length, self.flange_width, self.flange_thickness,
                   self.bend_radius, self.bend_height, 1.8, 12.5)
        hem2 = Hem(self.flange_length, self.flange_width, self.flange_thickness,
                   self.bend_radius, self.bend_height, 2.4, 11)
        roll1 = Roll2(self.flange_length, self.flange_width, self.flange_thickness,
                      self.bend_radius, self.bend_height, 290, 10, 35, 3.2)
        roll2 = Roll2(self.flange_length, self.flange_width, self.flange_thickness,
                      self.bend_radius, self.bend_height, 240, 9, 25, 4.3)
        ear_plate1 = EarPlate(self.flange_length, self.flange_width, self.flange_thickness,
                              self.bend_radius, self.bend_height, 2, 100, 12, 10, 2.8)
        ear_plate2 = EarPlate(self.flange_length, self.flange_width, self.flange_thickness,
                              self.bend_radius, self.bend_height, 3, 90, 13.4, 10, 3.5)

        # 在基体法兰上先切特征
        compound = BRepAlgoAPI_Fuse(self.base_flange(), bend.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), flang_hole1.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), flang_hole2.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), swelling1.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), swelling2.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), bend_groove1.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), bend_groove2.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_groove1.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_groove2.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rib1.cut_flange())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rib2.cut_flange())
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

        # 再将剩余特征与上面形成的组合体求和
        compound = BRepAlgoAPI_Fuse(compound.Shape(), flang_hole1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), flang_hole2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), swelling1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), swelling2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend_groove1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend_groove2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), profiled_groove1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), profiled_groove2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), rib1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), rib2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), hem1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), hem2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), roll1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), roll2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), ear_plate1.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), ear_plate2.feature_local())