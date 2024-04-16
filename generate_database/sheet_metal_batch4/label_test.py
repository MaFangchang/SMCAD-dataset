from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Display.SimpleGui import init_display
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_StepModelType
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.STEPConstruct import stepconstruct_FindEntity
from OCC.Core.TCollection import TCollection_HAsciiString
from label import FaceLabel
from OCC.Core.AIS import AIS_Shape
from OCC.Display.OCCViewer import rgb_color
from feature_test import Compound
import os
import glob
from OCC.Extend.DataExchange import STEPControl_Reader
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.StepRepr import StepRepr_RepresentationItem


class SingleCompound(object):
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
        total_compound, base_sheet, flang_hole1, flang_hole2, swelling1, swelling2, bend_groove1, \
            bend_groove2, rib1, rib2, rip1, rip2, common_hole1, common_hole2, common_groove1, common_groove2, \
            vent1, vent2, array1, array2, profiled_groove1, profiled_groove2, profiled_array1, profiled_array2, \
            bend1, bend2, roll1, roll2, ear_plate1, ear_plate2 \
            = Compound(self.flange_length, self.flange_width, self.flange_thickness, self.bend_radius,
                       self.bend_height, self.bend1_radius, self.bend1_height, self.bend2_radius, self.bend2_length,
                       self.bend3_radius, self.bend3_height, self.bend3_width, self.bend4_radius, self.bend4_height,
                       self.bend4_width, self.bend5_radius, self.bend5_length, self.bend5_width).compound()

        # 复合特征
        compound = BRepAlgoAPI_Cut(base_sheet.feature_local(), flang_hole1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), flang_hole1.feature_local())
        #compound = BRepAlgoAPI_Cut(compound.Shape(), swelling2.cut_flange())
        #compound = BRepAlgoAPI_Fuse(compound.Shape(), swelling2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), bend_groove1.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend_groove1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), rib2.cut_flange())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), rib2.feature_local())

        # 简单减材特征
        compound = BRepAlgoAPI_Cut(compound.Shape(), rip2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_hole2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), common_groove2.feature_local())
        #compound = BRepAlgoAPI_Cut(compound.Shape(), vent1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), array1.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_groove2.feature_local())
        compound = BRepAlgoAPI_Cut(compound.Shape(), profiled_array1.feature_local())

        # 简单增材特征
        compound = BRepAlgoAPI_Fuse(compound.Shape(), bend2.feature_local())
        compound = BRepAlgoAPI_Fuse(compound.Shape(), roll2.feature_local())
        #compound = BRepAlgoAPI_Fuse(compound.Shape(), ear_plate2.feature_local())

        return compound.Shape()


def shape_with_fid_to_step(filename, shape, label_map):
    # 将组合体形状保存到step文件中

    # filename: step文件的名称.
    # shape: 要保存的组合体形状.
    # label_map: B-rep面及其匹配的特征标签，要求必须是字典类型.
    # return: None

    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_StepModelType(0))

    finder_p = writer.WS().TransferWriter().FinderProcess()

    face_set = list(TopologyExplorer(shape).faces())

    loc = TopLoc_Location()
    for face in face_set:
        item = stepconstruct_FindEntity(finder_p, face, loc)
        if item is None:
            print(face)
            continue
        item.SetName(TCollection_HAsciiString(str(label_map[face])))

    writer.Write(filename)


def check_face_in_map(topo, face_label):
    # 用来检查是否所有的B-rep面都被贴上了特征标签
    failure = False
    faces = list(topo.faces())

    for face in faces:
        if face not in face_label:
            failure = True
            break

    return failure


def read_step_with_labels(filename):
    # 依次读取生成的所有step文件，并返回形状实体、B-rep面的集合、以及匹配的特征标签
    if not os.path.exists(filename):
        print(filename, ' not exists')
        return

    reader = STEPControl_Reader()
    reader.ReadFile(filename)
    reader.TransferRoots()
    shape = reader.OneShape()

    treader = reader.WS().TransferReader()

    map_id = {}
    topo = TopologyExplorer(shape)
    faces = list(topo.faces())

    for face in faces:
        item = treader.EntityFromShapeResult(face, 1)
        if item is None:
            print(face)
            continue
        item = StepRepr_RepresentationItem.DownCast(item)
        name = item.Name().ToCString()
        if name:
            name_id = name
            map_id[face] = name_id

    return shape, topo, map_id


def create_graphs(step_path):
    try:
        shape, topo, label_map = read_step_with_labels(step_path)
        failure_test = check_face_in_map(topo, label_map)

        if failure_test:
            print("Issue with face map")
        else:
            print(topo)
            print(label_map)

    except Exception as error:
        print(error)


def fill_color(face, rgb_value=()):
    ais_shape = AIS_Shape(face)
    ais_shape.SetColor(rgb_color(rgb_value[0], rgb_value[1], rgb_value[2]))
    ais_shape.SetDisplayMode(1)
    context.Display(ais_shape, True)
    context.SetTransparency(ais_shape, 0, True)
    drawer = ais_shape.DynamicHilightAttributes()
    context.HilightWithColor(ais_shape, drawer, False)


if __name__ == '__main__':
    new_compound = SingleCompound(50, 90, 0.8, 3, 44, 4, 5, 3, 28, 2, 30, 60, 3, 25, 33, 2.5, 17, 50).compound()

    display, start_display, add_menu, add_function_to_menu = init_display()  # 初始化
    context = display.Context
    context.SetAutoActivateSelection(False)
    id_map = FaceLabel(new_compound).generate_label()
    # n用来统计每个特征被标记的面的数量，通过更改value值来更换要统计的特征
    n0 = n1 = n2 = n3 = n4 = n5 = n6 = n7 = n8 = n9 = n10 = n11 = n12 = 0
    for key, value in id_map.items():  # 计算字典id_map里面包含的某种特征的面的标签个数n
        if value == 0:
            fill_color(key, (0.1, 0.1, 0.1))
            n0 = n0 + 1
        if value == 1:
            fill_color(key, (0., 0., 1.0))
            n1 = n1 + 1
        if value == 2:
            fill_color(key, (1.0, 0., 0.))
            n2 = n2 + 1
        if value == 3:
            fill_color(key, (1.0, 1.0, 0.))
            n3 = n3 + 1
        if value == 4:
            fill_color(key, (0., 0., 1.0))
            n4 = n4 + 1
        if value == 5:
            fill_color(key, (1.0, 0., 0.))
            n5 = n5 + 1
        if value == 6:
            fill_color(key, (0., 1.0, 0.))
            n6 = n6 + 1
        if value == 7:
            fill_color(key, (0., 0., 1.0))
            n7 = n7 + 1
        if value == 8:
            fill_color(key, (0.5, 0., 0.5))
            n8 = n8 + 1
        if value == 9:
            fill_color(key, (0., 0., 0.))
            n9 = n9 + 1
        if value == 10:
            fill_color(key, (0.7, 0.1, 0.5))
            n10 = n10 + 1
        if value == 11:
            fill_color(key, (0., 0.2, 0.8))
            n11 = n11 + 1
        if value == 12:
            fill_color(key, (0.7, 0.8, 0.9))
            n12 = n12 + 1

    print(id_map)
    print("n0=", n0, ";", "n1=", n1, ";", "n2=", n2, ";", "n3=", n3, ";", "n4=", n4, ";", "n5=", n5, ";", "n6=", n6,
          ";", "n7=", n7, ";", "n8=", n8, ";", "n9=", n9, ";", "n10=", n10, ";", "n11=", n11, ";", "n12=", n12)

    shape_with_fid_to_step(f'D:\\Users Files\\Layout\\file10.step', new_compound, id_map)

    # 下面代码用来查看是否所有面都被标记，不是的话会返回"Issue with face map"
    step_files = glob.glob("D:\\Users Files\\Layout\\file10.step")
    for step_file in step_files:
        create_graphs(step_file)

    display.View_Iso()
    display.FitAll()
    start_display()
