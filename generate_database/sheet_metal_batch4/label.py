from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from feature_test import Compound


def ask_face_centroid(face):
    """Get centroid of B-Rep face."""
    mass_props = GProp_GProps()
    brepgprop.SurfaceProperties(face, mass_props)
    g_point = mass_props.CentreOfMass().Coord()
    coordinate = tuple(['{:.13f}'.format(i) for i in g_point])

    return coordinate


def centroid_list(faces):
    face_centroid = []
    for face in faces:
        point = ask_face_centroid(face)
        face_centroid.append(point)

    return face_centroid


class FaceLabel(object):
    def __init__(self, compound):
        self.compound = compound

    def generate_label(self):
        new_compound, feature0, feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8, \
            feature9, feature10, feature11, feature12, feature13, feature14, feature15, feature16, feature17, \
            feature18, feature19, feature20, feature21, feature22, feature23, feature24, feature25, feature26, \
            feature27, feature28 = Compound(50, 90, 0.8, 3, 44, 4, 5, 3, 28, 2, 30, 60, 3, 25, 33, 2.5, 17,
                                            50).compound()

        faces0 = TopologyExplorer(feature0.flange_part()).faces()
        faces0_1 = TopologyExplorer(feature0.bend_part()).faces()
        faces0_2 = TopologyExplorer(feature0.cut_flange()).faces()
        faces1 = TopologyExplorer(feature1.feature_local()).faces()
        faces2 = TopologyExplorer(feature2.feature_local()).faces()  # 0翻边孔的面集合
        faces3 = TopologyExplorer(feature3.feature_local()).faces()
        faces4 = TopologyExplorer(feature4.feature_local()).faces()  # 1凸包的面集合
        faces5 = TopologyExplorer(feature5.cut_flange()).faces()
        faces5_1 = TopologyExplorer(feature5.bend_part()).faces()
        faces6 = TopologyExplorer(feature6.cut_flange()).faces()
        faces6_1 = TopologyExplorer(feature6.bend_part()).faces()  # 2止裂槽的面集合
        faces7 = TopologyExplorer(feature7.feature_local()).faces()
        faces7_1 = TopologyExplorer(feature7.bend_part()).faces()
        faces8 = TopologyExplorer(feature8.feature_local()).faces()
        faces8_1 = TopologyExplorer(feature8.bend_part()).faces()  # 3 肋的面集合
        faces9 = TopologyExplorer(feature9.feature_local()).faces()
        faces10 = TopologyExplorer(feature10.feature_local()).faces()  # 4 切口的面集合
        faces11 = TopologyExplorer(feature11.feature_local()).faces()
        faces12 = TopologyExplorer(feature12.feature_local()).faces()  # 5普通孔的面集合
        faces13 = TopologyExplorer(feature13.feature_local()).faces()
        faces14 = TopologyExplorer(feature14.feature_local()).faces()  # 6普通槽的面集合
        faces15 = TopologyExplorer(feature15.feature_local()).faces()
        faces16 = TopologyExplorer(feature16.feature_local()).faces()  # 7通风孔的面集合
        faces17 = TopologyExplorer(feature17.feature_local()).faces()
        faces18 = TopologyExplorer(feature18.feature_local()).faces()  # 8方孔的面集合
        faces19 = TopologyExplorer(feature19.feature_local()).faces()
        faces19_1 = TopologyExplorer(feature19.bend_part()).faces()
        faces20 = TopologyExplorer(feature20.feature_local()).faces()
        faces20_1 = TopologyExplorer(feature20.bend_part()).faces()  # 9折弯槽的面集合
        faces21 = TopologyExplorer(feature21.feature_local()).faces()
        faces21_1 = TopologyExplorer(feature21.bend_part()).faces()
        faces22 = TopologyExplorer(feature22.feature_local()).faces()
        faces22_1 = TopologyExplorer(feature22.bend_part()).faces()  # 10 折弯方孔的面集合
        faces23 = TopologyExplorer(feature23.bend_part()).faces()
        faces24 = TopologyExplorer(feature24.bend_part()).faces()  # 10折弯的面集合
        faces25 = TopologyExplorer(feature25.feature_local()).faces()
        faces25_1 = TopologyExplorer(feature25.groove_part()).faces()
        faces26 = TopologyExplorer(feature26.feature_local()).faces()
        faces26_1 = TopologyExplorer(feature26.groove_part()).faces()  # 12卷圆的面集合
        faces27 = TopologyExplorer(feature27.feature_local()).faces()
        faces27_1 = TopologyExplorer(feature27.hole_part()).faces()
        faces28 = TopologyExplorer(feature28.feature_local()).faces()
        faces28_1 = TopologyExplorer(feature28.hole_part()).faces()  # 13耳板的面集合
        faces29 = TopologyExplorer(self.compound).faces()
        base_centroid = centroid_list(faces0)
        f0 = centroid_list(faces1) + centroid_list(faces2)
        f1 = centroid_list(faces3) + centroid_list(faces4)
        f2 = centroid_list(faces5) + centroid_list(faces6) + centroid_list(faces0_2)
        f3 = centroid_list(faces7) + centroid_list(faces8)
        f4 = centroid_list(faces9) + centroid_list(faces10)
        f5 = centroid_list(faces11) + centroid_list(faces12) + centroid_list(faces27_1) + centroid_list(faces28_1)
        f6 = centroid_list(faces13) + centroid_list(faces14) + centroid_list(faces19) + centroid_list(faces20) \
             + centroid_list(faces25_1) + centroid_list(faces26_1)
        f7 = centroid_list(faces15) + centroid_list(faces16)
        f8 = centroid_list(faces17) + centroid_list(faces18) + centroid_list(faces21) + centroid_list(faces22)
        f9_1 = centroid_list(faces23) + centroid_list(faces24) + centroid_list(faces5_1) + centroid_list(faces6_1) \
               + centroid_list(faces7_1) + centroid_list(faces8_1) + centroid_list(faces19_1) \
               + centroid_list(faces20_1) + centroid_list(faces21_1) + centroid_list(faces22_1) \
               + centroid_list(faces0_1)
        res1 = list(set(f9_1) & set(base_centroid))
        f9 = list(set(f9_1) - set(res1))
        f10_1 = centroid_list(faces25) + centroid_list(faces26)
        res2 = list(set(f10_1) & set(base_centroid))
        f10 = list(set(f10_1) - set(res2))
        f11 = centroid_list(faces27) + centroid_list(faces28)
        id_map = {}
        for i in faces29:
            point = ask_face_centroid(i)
            if point in f0:
                dic = {i: 0}
                id_map.update(dic)
            elif point in f1:
                dic = {i: 1}
                id_map.update(dic)
            elif point in f2:
                dic = {i: 2}
                id_map.update(dic)
            elif point in f3:
                dic = {i: 3}
                id_map.update(dic)
            elif point in f4:
                dic = {i: 4}
                id_map.update(dic)
            elif point in f5:
                dic = {i: 5}
                id_map.update(dic)
            elif point in f6:
                dic = {i: 6}
                id_map.update(dic)
            elif point in f7:
                dic = {i: 7}
                id_map.update(dic)
            elif point in f8:
                dic = {i: 8}
                id_map.update(dic)
            elif point in f9:
                dic = {i: 9}
                id_map.update(dic)
            elif point in f10:
                dic = {i: 10}
                id_map.update(dic)
            elif point in f11:
                dic = {i: 11}
                id_map.update(dic)
            else:
                dic = {i: 12}
                id_map.update(dic)

        return id_map
