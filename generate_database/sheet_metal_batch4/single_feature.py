from math import sin, cos, radians
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Circ, gp_Vec
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle, GC_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace


class BaseSheet(object):  # 基体
    def __init__(self, flange_length, flange_width, flange_thickness, bend_radius, bend_height, bend1_radius,
                 bend1_height, bend2_radius, bend2_length, bend3_radius, bend3_height, bend3_width, groove1_length,
                 groove1_width, bend4_radius, bend4_height, bend4_width, groove2_length, groove2_width, bend5_radius,
                 bend5_length, bend5_width, groove3_length, groove3_width):

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
        self.groove1_length = float(groove1_length)  # 止裂口的长
        self.groove1_width = float(groove1_width)  # 止裂口的宽
        self.bend4_radius = float(bend4_radius)  # 四次折弯的半径
        self.bend4_height = float(bend4_height)  # 四次折弯的高度
        self.bend4_width = float(bend4_width)  # 四次折弯的宽度
        self.groove2_length = float(groove2_length)  # 止裂口的长
        self.groove2_width = float(groove2_width)  # 止裂口的宽
        self.bend5_angle = float(radians(70))  # 五次折弯的角度
        self.bend5_radius = float(bend5_radius)  # 五次折弯的半径
        self.bend5_length = float(bend5_length)  # 五次折弯延伸的长度
        self.bend5_width = float(bend5_width)  # 五次折弯的宽度
        self.groove3_length = float(groove3_length)  # 止裂口的长
        self.groove3_width = float(groove3_width)  # 止裂口的宽

    def base_flange(self):  # 生成基体法兰
        p1 = gp_Pnt(0., 0., 0.)  # 定义原点
        p2 = gp_Pnt(self.flange_length, 0., 0.)
        p3 = gp_Pnt(0., self.flange_width, 0.)
        p4 = gp_Pnt(self.flange_length, self.flange_width, 0.)  # 定义正方形另外三个顶点
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()  # 正方形四条拓扑边
        f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e1, e2, e3, e4).Wire())  # 生成底面
        flange = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到基体法兰

        return flange.Shape()

    def bend_part1(self):
        c1 = gp_Pnt(0., 0., self.bend_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(180), radians(270), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(180), radians(270), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        p1 = gp_Pnt(-self.bend_radius, 0., self.bend_radius)
        p2 = gp_Pnt(self.flange_thickness - self.bend_radius, 0., self.bend_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(0., 0., 0.), gp_Pnt(0., 0., self.flange_thickness)).Value())
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc1 = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.flange_width, 0.))  # 生成折弯弧

        c2 = gp_Pnt(self.flange_length, 0., self.bend1_radius)  # 圆心坐标
        circle3 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 1., 0.)), self.bend1_radius)  # 外圆
        circle4 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 1., 0.)), self.bend1_radius - self.flange_thickness)  # 内圆
        circle_arc3 = GC_MakeArcOfCircle(circle3, radians(90), radians(180), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc3.Value())  # 外圆弧边
        circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value())  # 内圆弧边
        p3 = gp_Pnt(self.flange_length + self.bend1_radius, 0., self.bend1_radius)
        p4 = gp_Pnt(self.flange_length + self.bend1_radius - self.flange_thickness, 0., self.bend1_radius)
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(self.flange_length, 0., 0.),
                                                    gp_Pnt(self.flange_length, 0., self.flange_thickness)).Value())
        circle_arc_w2 = BRepBuilderAPI_MakeWire(circle_arc_e3.Edge(), e3.Edge(), circle_arc_e4.Edge(), e4.Edge())
        circle_arc_f2 = BRepBuilderAPI_MakeFace(circle_arc_w2.Wire())  # 生成圆弧环面
        arc2 = BRepPrimAPI_MakePrism(circle_arc_f2.Face(), gp_Vec(0., self.flange_width, 0.))  # 生成折弯弧

        c3 = gp_Pnt(self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness, 0.,
                    self.bend1_radius + self.bend1_height)  # 圆心坐标
        circle5 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 1., 0.)), self.bend2_radius)  # 外圆
        circle6 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 1., 0.)), self.bend2_radius - self.flange_thickness)  # 内圆
        circle_arc5 = GC_MakeArcOfCircle(circle5, -radians(90), radians(0), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc6 = GC_MakeArcOfCircle(circle6, -radians(90), radians(0), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e5 = BRepBuilderAPI_MakeEdge(circle_arc5.Value())  # 外圆弧边
        circle_arc_e6 = BRepBuilderAPI_MakeEdge(circle_arc6.Value())  # 内圆弧边
        p5 = gp_Pnt(self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness, 0.,
                    self.bend1_radius + self.bend1_height + self.bend2_radius)
        p6 = gp_Pnt(self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness, 0.,
                    self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness)
        p7 = gp_Pnt(self.flange_length + self.bend1_radius, 0., self.bend1_radius + self.bend1_height)
        p8 = gp_Pnt(self.flange_length + self.bend1_radius - self.flange_thickness, 0.,
                    self.bend1_radius + self.bend1_height)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w3 = BRepBuilderAPI_MakeWire(circle_arc_e5.Edge(), e5.Edge(), circle_arc_e6.Edge(), e6.Edge())
        circle_arc_f3 = BRepBuilderAPI_MakeFace(circle_arc_w3.Wire())  # 生成圆弧环面
        arc3 = BRepPrimAPI_MakePrism(circle_arc_f3.Face(), gp_Vec(0., self.flange_width, 0.))  # 生成折弯弧
        bend_arc = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(arc1.Shape(), arc2.Shape()).Shape(), arc3.Shape())

        return bend_arc.Shape()

    def flange_part1(self):  # 生成折弯特征
        p1 = gp_Pnt(-self.bend_radius, 0., self.bend_radius)
        p2 = gp_Pnt(self.flange_thickness - self.bend_radius, 0., self.bend_radius)
        p3 = gp_Pnt(-self.bend_radius, self.flange_width, self.bend_radius)
        p4 = gp_Pnt(self.flange_thickness - self.bend_radius, self.flange_width, self.bend_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        edge_flange_f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e1, e2, e3, e4).Wire())  # 绘制边线法兰的底面
        flange1 = BRepPrimAPI_MakePrism(edge_flange_f1.Face(), gp_Vec(0., 0., self.bend_height))  # 生成边线法兰

        p5 = gp_Pnt(self.flange_length + self.bend1_radius, 0., self.bend1_radius)
        p6 = gp_Pnt(self.flange_length + self.bend1_radius - self.flange_thickness, 0., self.bend1_radius)
        p7 = gp_Pnt(self.flange_length + self.bend1_radius, self.flange_width, self.bend1_radius)
        p8 = gp_Pnt(self.flange_length + self.bend1_radius - self.flange_thickness, self.flange_width,
                    self.bend1_radius)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p7).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p8).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        edge_flange_f2 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e5, e6, e7, e8).Wire())  # 绘制边线法兰的底面
        flange2 = BRepPrimAPI_MakePrism(edge_flange_f2.Face(), gp_Vec(0., 0., self.bend1_height))  # 生成边线法兰

        inter_radius = self.bend2_radius - self.flange_thickness
        p9 = gp_Pnt(self.flange_length + self.bend1_radius + inter_radius, 0.,
                    self.bend1_radius + self.bend1_height + self.bend2_radius)
        p10 = gp_Pnt(self.flange_length + self.bend1_radius + inter_radius, 0.,
                     self.bend1_radius + self.bend1_height + inter_radius)
        p11 = gp_Pnt(self.flange_length + self.bend1_radius + inter_radius, self.flange_width,
                     self.bend1_radius + self.bend1_height + self.bend2_radius)
        p12 = gp_Pnt(self.flange_length + self.bend1_radius + inter_radius, self.flange_width,
                     self.bend1_radius + self.bend1_height + inter_radius)
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value()).Edge()
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p11).Value()).Edge()
        e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p12).Value()).Edge()
        e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value()).Edge()
        edge_flange_f3 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e9, e10, e11, e12).Wire())  # 绘制边线法兰的底面
        flange3 = BRepPrimAPI_MakePrism(edge_flange_f3.Face(), gp_Vec(self.bend2_length, 0., 0.))  # 生成边线法兰
        flange = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(flange1.Shape(), flange2.Shape()).Shape(), flange3.Shape())
        bend_flange = BRepAlgoAPI_Fuse(flange.Shape(), self.base_flange())

        return bend_flange.Shape()

    def cut_flange(self):
        p1 = gp_Pnt(self.flange_length/2 - self.bend4_width/2 - self.groove2_width, 0., 0.)
        p2 = gp_Pnt(self.flange_length/2 - self.bend4_width/2 - self.groove2_width, self.groove2_length, 0.)
        p3 = gp_Pnt(self.flange_length/2 - self.bend4_width/2, self.groove2_length, 0)
        p4 = gp_Pnt(self.flange_length/2 - self.bend4_width/2, self.bend4_radius, 0.)
        p5 = gp_Pnt(self.flange_length/2 + self.bend4_width/2, self.bend4_radius, 0.)
        p6 = gp_Pnt(self.flange_length/2 + self.bend4_width/2, self.groove2_length, 0.)
        p7 = gp_Pnt(self.flange_length/2 + self.bend4_width/2 + self.groove2_width, self.groove2_length, 0.)
        p8 = gp_Pnt(self.flange_length/2 + self.bend4_width/2 + self.groove2_width, 0., 0.)  # 定义全部顶点
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p7).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p8, p1).Value()).Edge()  # 定义全部拓扑边
        w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)
        w1.Add(BRepBuilderAPI_MakeWire(e5, e6, e7, e8).Wire())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成底面
        cut1 = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到基体法兰

        inter_radius = self.bend2_radius - self.flange_thickness
        x1 = self.flange_length + self.bend1_radius + inter_radius + self.bend2_length
        z1 = self.bend1_radius + self.bend1_height + inter_radius
        p9 = gp_Pnt(x1, self.flange_width/2 - self.bend3_width/2 - self.groove1_width, z1)
        p10 = gp_Pnt(x1 - self.groove1_length, self.flange_width/2 - self.bend3_width/2 - self.groove1_width, z1)
        p11 = gp_Pnt(x1 - self.groove1_length, self.flange_width/2 - self.bend3_width/2, z1)
        p12 = gp_Pnt(x1 - self.bend3_radius, self.flange_width/2 - self.bend3_width/2, z1)
        p13 = gp_Pnt(x1 - self.bend3_radius, self.flange_width/2 + self.bend3_width/2, z1)
        p14 = gp_Pnt(x1 - self.groove1_length, self.flange_width/2 + self.bend3_width/2, z1)
        p15 = gp_Pnt(x1 - self.groove1_length, self.flange_width/2 + self.bend3_width/2 + self.groove1_width, z1)
        p16 = gp_Pnt(x1, self.flange_width/2 + self.bend3_width/2 + self.groove1_width, z1)  # 定义全部顶点
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value()).Edge()
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p11).Value()).Edge()
        e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value()).Edge()
        e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p12, p13).Value()).Edge()
        e13 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p13, p14).Value()).Edge()
        e14 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p14, p15).Value()).Edge()
        e15 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p15, p16).Value()).Edge()
        e16 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p16, p9).Value()).Edge()  # 定义全部拓扑边
        w2 = BRepBuilderAPI_MakeWire(e9, e10, e11, e12)
        w2.Add(BRepBuilderAPI_MakeWire(e13, e14, e15, e16).Wire())
        f2 = BRepBuilderAPI_MakeFace(w2.Wire())  # 生成底面
        cut2 = BRepPrimAPI_MakePrism(f2.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到基体法兰

        y2 = self.flange_width / 2
        z2 = self.bend_radius + self.bend_height
        p17 = gp_Pnt(-self.bend_radius, y2 - self.bend5_width / 2 - self.groove3_width, z2)
        p18 = gp_Pnt(-self.bend_radius, y2 - self.bend5_width / 2 - self.groove3_width, z2 - self.groove3_length)
        p19 = gp_Pnt(-self.bend_radius, y2 - self.bend5_width / 2, z2 - self.groove3_length)
        p20 = gp_Pnt(-self.bend_radius, y2 - self.bend5_width / 2, z2 - self.bend5_radius)
        p21 = gp_Pnt(-self.bend_radius, y2 + self.bend5_width / 2, z2 - self.bend5_radius)
        p22 = gp_Pnt(-self.bend_radius, y2 + self.bend5_width / 2, z2 - self.groove3_length)
        p23 = gp_Pnt(-self.bend_radius, y2 + self.bend5_width / 2 + self.groove3_width, z2 - self.groove3_length)
        p24 = gp_Pnt(-self.bend_radius, y2 + self.bend5_width / 2 + self.groove3_width, z2)  # 定义全部顶点
        e17 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p17, p18).Value()).Edge()
        e18 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p18, p19).Value()).Edge()
        e19 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p19, p20).Value()).Edge()
        e20 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p20, p21).Value()).Edge()
        e21 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p21, p22).Value()).Edge()
        e22 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p22, p23).Value()).Edge()
        e23 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p23, p24).Value()).Edge()
        e24 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p24, p17).Value()).Edge()  # 定义全部拓扑边
        w3 = BRepBuilderAPI_MakeWire(e17, e18, e19, e20)
        w3.Add(BRepBuilderAPI_MakeWire(e21, e22, e23, e24).Wire())
        f3 = BRepBuilderAPI_MakeFace(w3.Wire())  # 生成底面
        cut3 = BRepPrimAPI_MakePrism(f3.Face(), gp_Vec(self.flange_thickness, 0., 0.))  # 拉伸得到基体法兰
        cut_flange = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(cut1.Shape(), cut2.Shape()).Shape(), cut3.Shape())

        return cut_flange.Shape()

    def bend_part(self):
        x1 = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        y1 = self.flange_width / 2 - self.bend3_width / 2
        z1 = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        c1 = gp_Pnt(x1 - self.bend3_radius, y1, z1 + self.bend3_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        p1 = gp_Pnt(x1, y1, z1 + self.bend3_radius)
        p2 = gp_Pnt(x1 - self.flange_thickness, y1, z1 + self.bend3_radius)
        p3 = gp_Pnt(x1 - self.bend3_radius, y1, z1)
        p4 = gp_Pnt(x1 - self.bend3_radius, y1, z1 + self.flange_thickness)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc1 = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.bend3_width, 0.))  # 生成折弯弧

        x2 = self.flange_length / 2 - self.bend4_width / 2
        c2 = gp_Pnt(x2, self.bend4_radius, self.flange_thickness - self.bend4_radius)  # 圆心坐标
        circle3 = gp_Circ(gp_Ax2(c2, gp_Dir(1., 0., 0.)), self.bend4_radius)  # 外圆
        circle4 = gp_Circ(gp_Ax2(c2, gp_Dir(1., 0., 0.)), self.bend4_radius - self.flange_thickness)  # 内圆
        circle_arc3 = GC_MakeArcOfCircle(circle3, radians(0), radians(90), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(0), radians(90), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc3.Value())  # 外圆弧边
        circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value())  # 内圆弧边
        p5 = gp_Pnt(x2, 0., self.flange_thickness - self.bend4_radius)
        p6 = gp_Pnt(x2, self.flange_thickness, self.flange_thickness - self.bend4_radius)
        p7 = gp_Pnt(x2, self.bend4_radius, self.flange_thickness)
        p8 = gp_Pnt(x2, self.bend4_radius, 0.)
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w2 = BRepBuilderAPI_MakeWire(circle_arc_e3.Edge(), e3.Edge(), circle_arc_e4.Edge(), e4.Edge())
        circle_arc_f2 = BRepBuilderAPI_MakeFace(circle_arc_w2.Wire())  # 生成圆弧环面
        arc2 = BRepPrimAPI_MakePrism(circle_arc_f2.Face(), gp_Vec(self.bend4_width, 0., 0.))  # 生成折弯弧

        inter_radius = self.bend5_radius - self.flange_thickness
        y2 = self.flange_width / 2 - self.bend5_width / 2
        z2 = self.bend_radius + self.bend_height - self.bend5_radius
        c3 = gp_Pnt(self.bend5_radius - self.bend_radius, y2, z2)  # 圆心坐标
        circle5 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 1., 0.)), self.bend5_radius)  # 外圆
        circle6 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 1., 0.)), inter_radius)  # 内圆
        circle_arc5 = GC_MakeArcOfCircle(circle5, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc6 = GC_MakeArcOfCircle(circle6, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc_e5 = BRepBuilderAPI_MakeEdge(circle_arc5.Value())  # 外圆弧边
        circle_arc_e6 = BRepBuilderAPI_MakeEdge(circle_arc6.Value())  # 内圆弧边
        dx1 = self.bend5_radius - self.bend5_radius * cos(self.bend5_angle)
        dx2 = self.bend5_radius - inter_radius * cos(self.bend5_angle)  # y坐标
        dz1 = self.bend5_radius * sin(self.bend5_angle)
        dz2 = inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        p9 = gp_Pnt(dx1 - self.bend_radius, y2, z2 + dz1)
        p10 = gp_Pnt(dx2 - self.bend_radius, y2, z2 + dz2)
        p11 = gp_Pnt(-self.bend_radius, y2, z2)
        p12 = gp_Pnt(self.flange_thickness - self.bend_radius, y2, z2)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w3 = BRepBuilderAPI_MakeWire(circle_arc_e5.Edge(), e5.Edge(), circle_arc_e6.Edge(), e6.Edge())
        circle_arc_f3 = BRepBuilderAPI_MakeFace(circle_arc_w3.Wire())  # 生成圆弧环面
        arc3 = BRepPrimAPI_MakePrism(circle_arc_f3.Face(), gp_Vec(0., self.bend5_width, 0.))  # 生成折弯弧
        arc = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(arc1.Shape(), arc2.Shape()).Shape(), arc3.Shape())
        bend_arc = BRepAlgoAPI_Fuse(arc.Shape(), self.bend_part1())

        return bend_arc.Shape()

    def flange_part(self):
        x1 = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        y1 = self.flange_width / 2 - self.bend3_width / 2
        z1 = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        p1 = gp_Pnt(x1, y1, z1 + self.bend3_radius)
        p2 = gp_Pnt(x1 - self.flange_thickness, y1, z1 + self.bend3_radius)
        p3 = gp_Pnt(x1, y1 + self.bend3_width, z1 + self.bend3_radius)
        p4 = gp_Pnt(x1 - self.flange_thickness, y1 + self.bend3_width, z1 + self.bend3_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        edge_flange_f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e1, e2, e3, e4).Wire())  # 绘制边线法兰的底面
        flange1 = BRepPrimAPI_MakePrism(edge_flange_f1.Face(), gp_Vec(0., 0., self.bend3_height))  # 生成边线法兰

        x2 = self.flange_length / 2 - self.bend4_width / 2
        p5 = gp_Pnt(x2, 0., self.flange_thickness - self.bend4_radius)
        p6 = gp_Pnt(x2, self.flange_thickness, self.flange_thickness - self.bend4_radius)
        p7 = gp_Pnt(x2 + self.bend4_width, 0., self.flange_thickness - self.bend4_radius)
        p8 = gp_Pnt(x2 + self.bend4_width, self.flange_thickness, self.flange_thickness - self.bend4_radius)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p7).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p8).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        edge_flange_f2 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e5, e6, e7, e8).Wire())  # 绘制边线法兰的底面
        flange2 = BRepPrimAPI_MakePrism(edge_flange_f2.Face(), gp_Vec(0., 0., -self.bend4_height))  # 生成边线法兰

        inter_radius = self.bend5_radius - self.flange_thickness
        y2 = self.flange_width / 2 - self.bend5_width / 2
        z2 = self.bend_radius + self.bend_height - self.bend5_radius
        dx1 = self.bend5_radius - self.bend5_radius * cos(self.bend5_angle)
        dx2 = self.bend5_radius - inter_radius * cos(self.bend5_angle)  # y坐标
        dz1 = self.bend5_radius * sin(self.bend5_angle)
        dz2 = inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        p9 = gp_Pnt(dx1 - self.bend_radius, y2, z2 + dz1)
        p10 = gp_Pnt(dx2 - self.bend_radius, y2, z2 + dz2)
        p11 = gp_Pnt(dx1 - self.bend_radius, y2 + self.bend5_width, z2 + dz1)
        p12 = gp_Pnt(dx2 - self.bend_radius, y2 + self.bend5_width, z2 + dz2)
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value()).Edge()
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p11).Value()).Edge()
        e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p12).Value()).Edge()
        e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value()).Edge()
        edge_flange_f3 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e9, e10, e11, e12).Wire())  # 绘制边线法兰的底面
        n1 = gp_Vec(self.bend5_length * sin(self.bend5_angle), 0., self.bend5_length * cos(self.bend5_angle))
        flange3 = BRepPrimAPI_MakePrism(edge_flange_f3.Face(), n1)  # 生成边线法兰
        flange = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(flange1.Shape(), flange2.Shape()).Shape(), flange3.Shape())
        bend_flange = BRepAlgoAPI_Fuse(flange.Shape(), self.flange_part1())

        return bend_flange.Shape()

    def feature_local(self):
        bend1 = BRepAlgoAPI_Cut(self.flange_part(), self.cut_flange())
        bend = BRepAlgoAPI_Fuse(bend1.Shape(), self.bend_part())

        return bend.Shape()


class FlangHole(object):  # 翻边孔
    def __init__(self, flange_length, flange_width, flange_thickness, bend4_radius, bend4_height, hole_radius,
                 hole_depth, round_radius):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend4_radius = float(bend4_radius)  # 折弯半径（外）
        self.bend4_height = float(bend4_height)  # 折弯高度，这里指边线法兰的长度
        self.hole_x_position = self.flange_length/2  # 翻边孔圆心y坐标
        self.hole_z_position = self.flange_thickness - self.bend4_radius - self.bend4_height/2  # 翻边孔圆心z坐标
        self.hole_radius = float(hole_radius)  # 孔外圆半径
        self.hole_depth = float(hole_depth)  # 孔深，减去基体法兰厚度的部分
        self.round_radius = float(round_radius)  # 倒圆半径

    def cut_flange(self):
        origin = gp_Pnt(self.hole_x_position, 0., self.hole_z_position)  # 定义圆心
        circle = gp_Circ(gp_Ax2(origin, gp_Dir(0., 1., 0.)), self.hole_radius + self.round_radius)  # 外圆
        circle_circ = GC_MakeCircle(circle)
        circle_e = BRepBuilderAPI_MakeEdge(circle_circ.Value())
        circle_w = BRepBuilderAPI_MakeWire(circle_e.Edge())
        circle_f = BRepBuilderAPI_MakeFace(circle_w.Wire())
        flange = BRepPrimAPI_MakePrism(circle_f.Face(), gp_Vec(0., self.flange_thickness, 0.))  # 拉伸得到基体法兰

        return flange.Shape()

    def feature_local(self):
        y = self.flange_thickness
        c1 = gp_Pnt(self.hole_x_position, y + self.round_radius,
                    self.hole_z_position + self.hole_radius + self.round_radius)
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(1., 0., 0.)), self.round_radius)
        circle1_arc = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 画倒圆，四分之一圆
        circle1_e = BRepBuilderAPI_MakeEdge(circle1_arc.Value())
        p1 = gp_Pnt(self.hole_x_position, y + self.round_radius, self.hole_z_position + self.hole_radius)
        p2 = gp_Pnt(self.hole_x_position, y + self.hole_depth, self.hole_z_position + self.hole_radius)
        p3 = gp_Pnt(self.hole_x_position, y + self.hole_depth, self.hole_z_position)
        p4 = gp_Pnt(self.hole_x_position, y, self.hole_z_position)
        p5 = gp_Pnt(self.hole_x_position, y, self.hole_z_position + self.hole_radius + self.round_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value())
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value())
        w1 = BRepBuilderAPI_MakeWire(e1.Edge(), e2.Edge(), e3.Edge(), e4.Edge())
        w1.Add(circle1_e.Edge())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成回转截面
        flang_hole = BRepPrimAPI_MakeRevol(f1.Face(), gp_Ax1(p3, gp_Dir(0., 1., 0.)))  # 生成翻边孔外侧

        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(1., 0., 0.)), self.round_radius + self.flange_thickness)
        circle2_arc = GC_MakeArcOfCircle(circle2, radians(90), radians(180), True)  # 画倒圆，四分之一圆
        circle2_e = BRepBuilderAPI_MakeEdge(circle2_arc.Value())
        p6 = gp_Pnt(self.hole_x_position, y + self.round_radius,
                    self.hole_z_position + self.hole_radius - self.flange_thickness)
        p7 = gp_Pnt(self.hole_x_position, y + self.hole_depth,
                    self.hole_z_position + self.hole_radius - self.flange_thickness)
        p8 = gp_Pnt(self.hole_x_position, y + self.hole_depth, self.hole_z_position)
        p9 = gp_Pnt(self.hole_x_position, 0., self.hole_z_position)
        p10 = gp_Pnt(self.hole_x_position, 0., self.hole_z_position + self.hole_radius + self.round_radius)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p7).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value())
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p8, p9).Value())
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value())
        w2 = BRepBuilderAPI_MakeWire(e5.Edge(), e6.Edge(), e7.Edge(), e8.Edge())
        w2.Add(circle2_e.Edge())
        f2 = BRepBuilderAPI_MakeFace(w2.Wire())  # 生成回转截面
        inter_hole = BRepPrimAPI_MakeRevol(f2.Face(), gp_Ax1(p3, gp_Dir(0., 1., 0.)))  # 生成翻边孔的内孔
        compound_fuse = BRepAlgoAPI_Fuse(self.cut_flange(), flang_hole.Shape())
        compound = BRepAlgoAPI_Cut(compound_fuse.Shape(), inter_hole.Shape())

        return compound.Shape()


class Swelling(object):  # 凸包
    def __init__(self, flange_length, flange_width, flange_thickness, bend1_radius, bend1_height, bend2_radius,
                 bend2_length, bend3_radius, bend3_height, bend3_width, swelling_radius, swelling_height, round_radius):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend1_radius = float(bend1_radius)  # 一次折弯的半径
        self.bend1_height = float(bend1_height)  # 一次折弯延伸的长度
        self.bend2_radius = float(bend2_radius)  # 二次折弯的半径
        self.bend2_length = float(bend2_length)  # 二次折弯延伸的长度
        self.bend3_radius = float(bend3_radius)  # 三次折弯的半径
        self.bend3_height = float(bend3_height)  # 三次折弯的高度
        self.bend3_width = float(bend3_width)  # 三次折弯的宽度
        self.swelling_y_position = self.flange_width/2  # 凸包圆心y坐标
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness + self.bend3_radius
        self.swelling_z_position = z + self.bend3_height/2 + 1.0  # 凸包圆心z坐标
        self.swelling_radius = float(swelling_radius)  # 凸包外圆半径
        self.swelling_height = float(swelling_height)  # 凸包高度
        self.round_radius = float(round_radius)  # 倒圆半径

    def cut_flange(self):  # 生成基体法兰
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        origin = gp_Pnt(x, self.swelling_y_position, self.swelling_z_position)
        circle = gp_Circ(gp_Ax2(origin, gp_Dir(1., 0., 0.)), self.swelling_radius + self.round_radius)  # 外圆
        circle_circ = GC_MakeCircle(circle)
        circle_e = BRepBuilderAPI_MakeEdge(circle_circ.Value())
        circle_w = BRepBuilderAPI_MakeWire(circle_e.Edge())
        circle_f = BRepBuilderAPI_MakeFace(circle_w.Wire())
        flange = BRepPrimAPI_MakePrism(circle_f.Face(), gp_Vec(-self.flange_thickness, 0., 0.))  # 拉伸得到基体法兰

        return flange.Shape()

    def feature_local(self):
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        c1 = gp_Pnt(x + self.round_radius, self.swelling_y_position,
                    self.swelling_z_position + self.swelling_radius + self.round_radius)
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.round_radius)
        circle1_arc = GC_MakeArcOfCircle(circle1, radians(180), radians(270), True)  # 画倒圆，四分之一圆
        circle1_e = BRepBuilderAPI_MakeEdge(circle1_arc.Value())
        decrement = self.round_radius + self.flange_thickness
        p1 = gp_Pnt(x + self.round_radius, self.swelling_y_position, self.swelling_z_position + self.swelling_radius)
        p2 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position,
                    self.swelling_z_position + self.swelling_radius)
        p3 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position, self.swelling_z_position)
        p4 = gp_Pnt(x, self.swelling_y_position, self.swelling_z_position)
        p5 = gp_Pnt(x, self.swelling_y_position, self.swelling_z_position + self.swelling_radius + self.round_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value())
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value())
        w1 = BRepBuilderAPI_MakeWire(e1.Edge(), e2.Edge(), e3.Edge(), e4.Edge())
        w1.Add(circle1_e.Edge())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成回转截面
        bump_1 = BRepPrimAPI_MakeRevol(f1.Face(), gp_Ax1(p3, gp_Dir(-1., 0., 0.)))  # 凸台的圆柱部分

        p6 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position, self.swelling_z_position)
        p7 = gp_Pnt(x + self.swelling_height, self.swelling_y_position, self.swelling_z_position)
        p8 = gp_Pnt(x + self.swelling_height, self.swelling_y_position,
                    self.swelling_z_position + self.swelling_radius - decrement)
        p9 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position,
                    self.swelling_z_position + self.swelling_radius)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p7).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p9).Value())
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value())
        c2 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position,
                    self.swelling_z_position + self.swelling_radius - decrement)
        circle2 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 1., 0.)), decrement)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(0), radians(90), True)
        circle2_e = BRepBuilderAPI_MakeEdge(circle_arc2.Value())
        r_outline1_w = BRepBuilderAPI_MakeWire(e5.Edge(), e6.Edge(), e7.Edge(), circle2_e.Edge())  # 凸台倒圆的旋转截面轮廓
        r_outline1_f = BRepBuilderAPI_MakeFace(r_outline1_w.Wire())  # 凸台倒圆的旋转截面
        round_1 = BRepPrimAPI_MakeRevol(r_outline1_f.Face(), gp_Ax1(p3, gp_Dir(-1., 0., 0.)))  # 回转得到凸台倒圆
        bump = BRepAlgoAPI_Fuse(bump_1.Shape(), round_1.Shape())  # 外凸台，这里为了方便倒圆分成两部分

        circle3 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), decrement)
        circle3_arc = GC_MakeArcOfCircle(circle3, radians(180), radians(270), True)  # 画倒圆，四分之一圆
        circle3_e = BRepBuilderAPI_MakeEdge(circle3_arc.Value())
        p10 = gp_Pnt(x + self.round_radius, self.swelling_y_position,
                     self.swelling_z_position + self.swelling_radius - self.flange_thickness)
        p11 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position,
                     self.swelling_z_position + self.swelling_radius - self.flange_thickness)
        p12 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position, self.swelling_z_position)
        p13 = gp_Pnt(x - self.flange_thickness, self.swelling_y_position, self.swelling_z_position)
        p14 = gp_Pnt(x - self.flange_thickness, self.swelling_y_position,
                     self.swelling_z_position + self.swelling_radius + self.round_radius)
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p11).Value())
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value())
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p12, p13).Value())
        e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p13, p14).Value())
        w2 = BRepBuilderAPI_MakeWire(e8.Edge(), e9.Edge(), e10.Edge(), e11.Edge())
        w2.Add(circle3_e.Edge())
        f2 = BRepBuilderAPI_MakeFace(w2.Wire())  # 生成回转截面
        inter_hole_1 = BRepPrimAPI_MakeRevol(f2.Face(), gp_Ax1(p3, gp_Dir(-1., 0., 0.)))  # 内孔的圆柱部分

        p15 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position, self.swelling_z_position)
        p16 = gp_Pnt(x + self.swelling_height - self.flange_thickness, self.swelling_y_position,
                     self.swelling_z_position)
        p17 = gp_Pnt(x + self.swelling_height - self.flange_thickness, self.swelling_y_position,
                     self.swelling_z_position + self.swelling_radius - decrement)
        p18 = gp_Pnt(x + self.swelling_height - decrement, self.swelling_y_position,
                     self.swelling_z_position + self.swelling_radius - self.flange_thickness)
        e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p15, p16).Value())
        e13 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p15, p18).Value())
        e14 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p16, p17).Value())
        circle4 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 1., 0.)), self.round_radius)
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(0), radians(90), True)
        circle4_e = BRepBuilderAPI_MakeEdge(circle_arc4.Value())
        r_outline2_w = BRepBuilderAPI_MakeWire(e12.Edge(), e13.Edge(), e14.Edge(), circle4_e.Edge())  # 内孔倒圆的旋转截面轮廓
        r_outline2_f = BRepBuilderAPI_MakeFace(r_outline2_w.Wire())  # 内孔倒圆的旋转截面
        round_2 = BRepPrimAPI_MakeRevol(r_outline2_f.Face(), gp_Ax1(p3, gp_Dir(-1., 0., 0.)))  # 回转得到内孔倒圆
        inter_hole = BRepAlgoAPI_Fuse(inter_hole_1.Shape(), round_2.Shape())  # 内孔，这里为了方便倒圆分成两部分
        compound_fuse = BRepAlgoAPI_Fuse(self.cut_flange(), bump.Shape())
        compound = BRepAlgoAPI_Cut(compound_fuse.Shape(), inter_hole.Shape())

        return compound.Shape()


class BendGroove(object):  # 带止裂槽的折弯
    def __init__(self, flange_length, flange_width, flange_thickness, bend_radius, bend_height, bend1_angle,
                 bend1_radius, bend1_height, bend1_width, groove_length, groove_width):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend_radius = float(bend_radius)  # 基本折弯半径（外）
        self.bend_height = float(bend_height)  # 基本折弯高度，这里指边线法兰的长度
        self.bend1_angle = float(radians(bend1_angle))  # 折弯角（度转为弧度）
        self.bend1_radius = float(bend1_radius)  # 折弯半径（外）
        self.bend1_height = float(bend1_height)  # 折弯高度，这里指边线法兰的长度
        self.bend1_width = float(bend1_width)  # 折弯宽度
        self.groove_length = float(groove_length)  # 一个止裂口的长
        self.groove_width = float(groove_width)  # 一个止裂口的宽

    def cut_flange(self):
        f_p1 = self.bend_radius + self.bend_height/2 - self.bend1_width/2 - 1.0
        f_p2 = self.bend_radius + self.bend_height/2 + self.bend1_width/2 - 1.0
        p1 = gp_Pnt(-self.bend_radius, self.flange_width, f_p1 - self.groove_width)
        p2 = gp_Pnt(-self.bend_radius, self.flange_width - self.groove_length, f_p1 - self.groove_width)
        p3 = gp_Pnt(-self.bend_radius, self.flange_width - self.groove_length, f_p1)
        p4 = gp_Pnt(-self.bend_radius, self.flange_width - self.bend1_radius, f_p1)
        p5 = gp_Pnt(-self.bend_radius, self.flange_width - self.bend1_radius, f_p2)
        p6 = gp_Pnt(-self.bend_radius, self.flange_width - self.groove_length, f_p2)
        p7 = gp_Pnt(-self.bend_radius, self.flange_width - self.groove_length, f_p2 + self.groove_width)
        p8 = gp_Pnt(-self.bend_radius, self.flange_width, f_p2 + self.groove_width)  # 定义全部顶点
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p7).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p8, p1).Value()).Edge()  # 定义全部拓扑边
        w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)
        w2 = BRepBuilderAPI_MakeWire(e5, e6, e7, e8)
        w1.Add(w2.Wire())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成底面
        cut_flange = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(self.flange_thickness, 0., 0.))  # 拉伸得到基体法兰

        return cut_flange.Shape()

    def bend_part(self):
        f_p = self.bend_radius + self.bend_height / 2 - self.bend1_width / 2 - 1.0
        inter_radius = self.bend1_radius - self.flange_thickness
        c1 = gp_Pnt(self.bend1_radius - self.bend_radius, self.flange_width - self.bend1_radius, f_p)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), self.bend1_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(180) - self.bend1_angle, radians(180), True)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(180) - self.bend1_angle, radians(180), True)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        x1 = self.bend1_radius - self.bend1_radius * cos(self.bend1_angle)
        x2 = self.bend1_radius - inter_radius * cos(self.bend1_angle)  # x坐标
        y1 = self.bend1_radius * sin(self.bend1_angle)
        y2 = inter_radius * sin(self.bend1_angle)  # y坐标，注意是折弯半径减
        p1 = gp_Pnt(x1 - self.bend_radius, self.flange_width - self.bend1_radius + y1, f_p)
        p2 = gp_Pnt(x2 - self.bend_radius, self.flange_width - self.bend1_radius + y2, f_p)
        p3 = gp_Pnt(-self.bend_radius, self.flange_width - self.bend1_radius, f_p)
        p4 = gp_Pnt(self.flange_thickness - self.bend_radius, self.flange_width - self.bend1_radius, f_p)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        bend_arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., 0., self.bend1_width))  # 生成折弯弧

        return bend_arc.Shape()

    def flange_part(self):
        inter_radius = self.bend1_radius - self.flange_thickness
        f_p = self.bend_radius + self.bend_height / 2 - self.bend1_width / 2 - 1.0
        x1 = self.bend1_radius - self.bend1_radius * cos(self.bend1_angle)
        x2 = self.bend1_radius - inter_radius * cos(self.bend1_angle)  # x坐标
        y1 = self.bend1_radius * sin(self.bend1_angle)
        y2 = inter_radius * sin(self.bend1_angle)  # y坐标，注意是折弯半径减
        p1 = gp_Pnt(x1 - self.bend_radius, self.flange_width - self.bend1_radius + y1, f_p)
        p2 = gp_Pnt(x2 - self.bend_radius, self.flange_width - self.bend1_radius + y2, f_p)
        p3 = gp_Pnt(x1 - self.bend_radius, self.flange_width - self.bend1_radius + y1, f_p + self.bend1_width)
        p4 = gp_Pnt(x2 - self.bend_radius, self.flange_width - self.bend1_radius + y2, f_p + self.bend1_width)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value())
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        edge_flange_w = BRepBuilderAPI_MakeWire(e1.Edge(), e2.Edge(), e3.Edge(), e4.Edge())
        edge_flange_f = BRepBuilderAPI_MakeFace(edge_flange_w.Wire())  # 绘制边线法兰的底面
        n1 = gp_Vec(self.bend1_height * sin(self.bend1_angle), self.bend1_height * cos(self.bend1_angle), 0.)
        bend_flange = BRepPrimAPI_MakePrism(edge_flange_f.Face(), n1)  # 生成边线法兰

        return bend_flange.Shape()

    def feature_local(self):
        narrow_bend = BRepAlgoAPI_Fuse(self.bend_part(), self.flange_part())  # 布尔并

        return narrow_bend.Shape()


class Rib(object):  # 带肋骨的折弯
    def __init__(self, flange_length, flange_width, flange_thickness, bend1_radius, bend1_height, bend2_radius,
                 bend2_length, bend3_radius, bend3_height, bend3_width, rib_length, rib_width):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend1_radius = float(bend1_radius)  # 一次折弯的半径
        self.bend1_height = float(bend1_height)  # 一次折弯延伸的长度
        self.bend2_radius = float(bend2_radius)  # 二次折弯的半径
        self.bend2_length = float(bend2_length)  # 二次折弯延伸的长度
        self.bend3_radius = float(bend3_radius)  # 三次折弯的半径
        self.bend3_height = float(bend3_height)  # 三次折弯的高度
        self.bend3_width = float(bend3_width)  # 三次折弯的宽度
        self.rib_length = float(rib_length)  # 肋在法兰部分延伸的长度
        self.rib_width = float(rib_width)  # 肋的宽度
        self.rib_position = self.flange_width/2 - self.rib_width/2  # 肋的y坐标

    def fuse_feature(self):
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        c1 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.flange_thickness, z + self.bend3_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(90), radians(180), True)
        p1 = gp_Pnt(x - self.flange_thickness, self.rib_position + self.flange_thickness, z + self.bend3_radius)
        p2 = gp_Pnt(x, self.rib_position + self.flange_thickness, z + self.bend3_radius)
        p3 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.flange_thickness, z + self.flange_thickness)
        p4 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.flange_thickness, z)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        n1 = gp_Vec(0., self.rib_width - 2 * self.flange_thickness, 0.)
        bend_arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), n1)  # 生成折弯弧

        p5 = gp_Pnt(x - self.flange_thickness, self.rib_position + self.rib_width - self.flange_thickness,
                    z + self.bend3_radius)
        p6 = gp_Pnt(x, self.rib_position + self.rib_width - self.flange_thickness, z + self.bend3_radius)
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p5).Value())
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p6).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value())
        fuse1_w = BRepBuilderAPI_MakeWire(e3.Edge(), e4.Edge(), e5.Edge(), e6.Edge())
        fuse1_f = BRepBuilderAPI_MakeFace(fuse1_w.Wire())  # 绘制边线法兰的底面
        fuse1 = BRepPrimAPI_MakePrism(fuse1_f.Face(), gp_Vec(0., 0., self.rib_length))  # 生成边线法兰

        p7 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.rib_width - self.flange_thickness,
                    z + self.flange_thickness)
        p8 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.rib_width - self.flange_thickness, z)
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p7).Value())
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p8).Value())
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value())
        fuse2_w = BRepBuilderAPI_MakeWire(e7.Edge(), e8.Edge(), e9.Edge(), e10.Edge())
        fuse2_f = BRepBuilderAPI_MakeFace(fuse2_w.Wire())
        fuse2 = BRepPrimAPI_MakePrism(fuse2_f.Face(), gp_Vec(-self.rib_length, 0., 0.))
        fuse = BRepAlgoAPI_Fuse(bend_arc.Shape(), fuse1.Shape())
        fuse_feature = BRepAlgoAPI_Fuse(fuse.Shape(), fuse2.Shape())

        return fuse_feature.Shape()

    def cut_flange(self):
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        c1 = gp_Pnt(x - self.bend3_radius, self.rib_position, z + self.bend3_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        p1 = gp_Pnt(x - self.flange_thickness, self.rib_position, z + self.bend3_radius)
        p2 = gp_Pnt(x - self.flange_thickness, self.rib_position, z + self.bend3_radius + self.rib_length)
        p3 = gp_Pnt(x - self.bend3_radius, self.rib_position, z + self.flange_thickness)
        p4 = gp_Pnt(x - self.bend3_radius - self.rib_length, self.rib_position, z + self.flange_thickness)
        circle_arc1_e = BRepBuilderAPI_MakeEdge(circle_arc1.Value())
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value())
        w1 = BRepBuilderAPI_MakeWire(circle_arc1_e.Edge(), e1.Edge(), e2.Edge(), e3.Edge())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())
        rib_feature = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., self.rib_width, 0.))
        cut_flange = BRepAlgoAPI_Fuse(rib_feature.Shape(), self.fuse_feature())

        return cut_flange.Shape()

    def feature_local(self):
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        c1 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.flange_thickness, z + self.bend3_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius)  # 外圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        p1 = gp_Pnt(x, self.rib_position + self.flange_thickness, z + self.bend3_radius)
        p2 = gp_Pnt(x, self.rib_position + self.flange_thickness, z + self.bend3_radius + self.rib_length)
        p3 = gp_Pnt(x - self.bend3_radius, self.rib_position + self.flange_thickness, z)
        p4 = gp_Pnt(x - self.bend3_radius - self.rib_length, self.rib_position + self.flange_thickness, z)
        circle_arc1_e = BRepBuilderAPI_MakeEdge(circle_arc1.Value()).Edge()
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()
        f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_arc1_e, e1, e2, e3).Wire())
        rib = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., self.rib_width - 2 * self.flange_thickness, 0.)).Shape()
        cut_feature = BRepAlgoAPI_Cut(self.cut_flange(), rib)

        return cut_feature.Shape()

    def bend_part(self):
        x = self.flange_length + self.bend1_radius + self.bend2_radius - self.flange_thickness + self.bend2_length
        y = self.flange_width / 2 - self.bend3_width / 2
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness
        c1 = gp_Pnt(x - self.bend3_radius, y, z + self.bend3_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend3_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(90), radians(180), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        segment1 = GC_MakeSegment(gp_Pnt(x, y, z + self.bend3_radius),
                                  gp_Pnt(x - self.flange_thickness, y, z + self.bend3_radius))
        segment2 = GC_MakeSegment(gp_Pnt(x - self.bend3_radius, y, z),
                                  gp_Pnt(x - self.bend3_radius, y, z + self.flange_thickness))
        e1 = BRepBuilderAPI_MakeEdge(segment1.Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(segment2.Value()).Edge()  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1, circle_arc_e2.Edge(), e2)
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.bend3_width, 0.))  # 生成折弯弧
        bend_arc = BRepAlgoAPI_Fuse(BRepAlgoAPI_Cut(arc.Shape(), self.fuse_feature()).Shape(), self.feature_local())

        return bend_arc.Shape()


class Rip(object):  # 切口
    def __init__(self, flange_length, flange_width, flange_thickness, rip_width, rip_depth):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.rip_width = float(rip_width)  # 切口宽
        self.rip_depth = float(rip_depth)  # 切口深
        self.rip_position = self.flange_length/2 - self.rip_width/2 - 1.0  # 切口位置

    def feature_local(self):  # 生成切口特征
        p1 = gp_Pnt(self.rip_position, self.flange_width, 0.)
        p2 = gp_Pnt(self.rip_position, self.flange_width - self.rip_depth, 0.)
        p3 = gp_Pnt(self.rip_position + self.rip_width, self.flange_width - self.rip_depth, 0.)
        p4 = gp_Pnt(self.rip_position + self.rip_width, self.flange_width, 0.)  # 切口的四个顶点
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p4).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p3).Value()).Edge()  # 切口的四条拓扑边
        w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)  # 生成网格
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成底面
        rip = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到切口法兰

        return rip.Shape()


class CommonHole(object):  # 普通孔
    def __init__(self, flange_length, flange_width, flange_thickness, bend4_radius, bend4_height, bend4_width,
                 hole_spacing, small_hole_radius):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend4_radius = float(bend4_radius)  # 三次折弯的半径
        self.bend4_height = float(bend4_height)  # 三次折弯的高度
        self.bend4_width = float(bend4_width)  # 三次折弯的宽度
        self.hole_spacing = float(hole_spacing)  # 小孔圆心到折弯边界的距离
        self.small_hole_radius = float(small_hole_radius)  # 小孔半径

    def feature_local(self):  # 生成孔特征
        f_p1 = self.flange_length/2 - self.bend4_width/2 + self.hole_spacing
        f_p2 = self.flange_length/2 + self.bend4_width/2 - self.hole_spacing
        z = self.flange_thickness - self.bend4_radius
        c1 = gp_Pnt(f_p1, 0., z - self.bend4_height + self.hole_spacing)
        c2 = gp_Pnt(f_p1, 0., z - self.hole_spacing)
        c3 = gp_Pnt(f_p2, 0., z - self.bend4_height + self.hole_spacing)
        c4 = gp_Pnt(f_p2, 0., z - self.hole_spacing)
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.small_hole_radius)
        circle2 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 1., 0.)), self.small_hole_radius)
        circle3 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 1., 0.)), self.small_hole_radius)
        circle4 = gp_Circ(gp_Ax2(c4, gp_Dir(0., 1., 0.)), self.small_hole_radius)  # 孔圆
        circle_w1 = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(GC_MakeCircle(circle1).Value()).Edge())
        circle_w2 = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(GC_MakeCircle(circle2).Value()).Edge())
        circle_w3 = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(GC_MakeCircle(circle3).Value()).Edge())
        circle_w4 = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(GC_MakeCircle(circle4).Value()).Edge())
        n1 = gp_Vec(0., self.flange_thickness, 0.)  # 定义拉伸向量
        common_hole1 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(circle_w1.Wire()).Face(), n1).Shape()  # 小
        common_hole2 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(circle_w2.Wire()).Face(), n1).Shape()  # 小
        common_hole3 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(circle_w3.Wire()).Face(), n1).Shape()  # 小
        common_hole4 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(circle_w4.Wire()).Face(), n1).Shape()  # 小
        common_hole = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(common_hole1, common_hole2).Shape(),
                                       BRepAlgoAPI_Fuse(common_hole3, common_hole4).Shape())  # 合并小

        return common_hole.Shape()


class CommonGroove(object):  # 普通槽
    def __init__(self, flange_length, flange_width, flange_thickness, groove_spacing, groove_angle, groove_length,
                 groove_width):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.groove_spacing = float(groove_spacing)  # 槽的间距的一半
        self.groove_angle = float(radians(groove_angle))  # 折弯角（度转为弧度）
        self.groove_length = float(groove_length)  # 槽的长
        self.groove_width = float(groove_width)  # 槽的宽

    def feature_local(self):  # 生成槽特征
        delta_y_1 = self.groove_length/2 * cos(self.groove_angle)
        delta_y_2 = self.groove_width/2 * sin(self.groove_angle)
        delta_x_1 = self.groove_length/2 * sin(self.groove_angle)
        delta_x_2 = self.groove_width/2 * cos(self.groove_angle)
        y1 = self.flange_width/2 + self.groove_spacing
        y2 = self.flange_width / 2 - self.groove_spacing
        x1 = self.flange_length/2 + self.groove_spacing/2
        x2 = self.flange_length/2 - self.groove_spacing/2
        p1 = gp_Pnt(x1 + delta_x_1 + delta_x_2, y1 - delta_y_1 + delta_y_2, 0.)
        p2 = gp_Pnt(x1 + delta_x_1 - delta_x_2, y1 - delta_y_1 - delta_y_2, 0.)
        p3 = gp_Pnt(x1 - delta_x_1 + delta_x_2, y1 + delta_y_1 + delta_y_2, 0.)
        p4 = gp_Pnt(x1 - delta_x_1 - delta_x_2, y1 + delta_y_1 - delta_y_2, 0.)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()  # 槽的两条直角边
        c1 = gp_Pnt(x1 + delta_x_1, y1 - delta_y_1, 0.)
        c2 = gp_Pnt(x1 - delta_x_1, y1 + delta_y_1, 0.)  # 圆心坐标
        circle_1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), self.groove_width/2)
        circle_2 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 0., 1.)), self.groove_width/2)
        circle_are_1 = GC_MakeArcOfCircle(circle_1, self.groove_angle + radians(180), self.groove_angle, True)
        circle_arc_2 = GC_MakeArcOfCircle(circle_2, self.groove_angle, self.groove_angle + radians(180), True)  # 槽半圆
        circle_e_1 = BRepBuilderAPI_MakeEdge(circle_are_1.Value()).Edge()
        circle_e_2 = BRepBuilderAPI_MakeEdge(circle_arc_2.Value()).Edge()  # 槽的半圆边
        groove_f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_e_1, e1, circle_e_2, e2).Wire())
        groove1 = BRepPrimAPI_MakePrism(groove_f1.Face(), gp_Vec(0., 0., self.flange_thickness))

        p5 = gp_Pnt(x1 + delta_x_1 + delta_x_2, y2 + delta_y_1 - delta_y_2, 0.)
        p6 = gp_Pnt(x1 + delta_x_1 - delta_x_2, y2 + delta_y_1 + delta_y_2, 0.)
        p7 = gp_Pnt(x1 - delta_x_1 + delta_x_2, y2 - delta_y_1 - delta_y_2, 0.)
        p8 = gp_Pnt(x1 - delta_x_1 - delta_x_2, y2 - delta_y_1 + delta_y_2, 0.)
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p7).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p8).Value()).Edge()  # 槽的两条直角边
        c3 = gp_Pnt(x1 + delta_x_1, y2 + delta_y_1, 0.)
        c4 = gp_Pnt(x1 - delta_x_1, y2 - delta_y_1, 0.)  # 圆心坐标
        circle_3 = gp_Circ(gp_Ax2(c3, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_4 = gp_Circ(gp_Ax2(c4, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_are_3 = GC_MakeArcOfCircle(circle_3, -self.groove_angle, -self.groove_angle + radians(180), True)
        circle_arc_4 = GC_MakeArcOfCircle(circle_4, -self.groove_angle + radians(180), -self.groove_angle, True)
        circle_e_3 = BRepBuilderAPI_MakeEdge(circle_are_3.Value()).Edge()
        circle_e_4 = BRepBuilderAPI_MakeEdge(circle_arc_4.Value()).Edge()  # 槽的半圆边
        groove_f2 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_e_3, e3, circle_e_4, e4).Wire())
        groove2 = BRepPrimAPI_MakePrism(groove_f2.Face(), gp_Vec(0., 0., self.flange_thickness))

        p9 = gp_Pnt(x2 - delta_x_1 - delta_x_2, y1 - delta_y_1 + delta_y_2, 0.)
        p10 = gp_Pnt(x2 - delta_x_1 + delta_x_2, y1 - delta_y_1 - delta_y_2, 0.)
        p11 = gp_Pnt(x2 + delta_x_1 - delta_x_2, y1 + delta_y_1 + delta_y_2, 0.)
        p12 = gp_Pnt(x2 + delta_x_1 + delta_x_2, y1 + delta_y_1 - delta_y_2, 0.)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p11).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p12).Value()).Edge()  # 槽的两条直角边
        c5 = gp_Pnt(x2 - delta_x_1, y1 - delta_y_1, 0.)
        c6 = gp_Pnt(x2 + delta_x_1, y1 + delta_y_1, 0.)  # 圆心坐标
        circle_5 = gp_Circ(gp_Ax2(c5, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_6 = gp_Circ(gp_Ax2(c6, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_are_5 = GC_MakeArcOfCircle(circle_5, -self.groove_angle + radians(180), -self.groove_angle, True)
        circle_arc_6 = GC_MakeArcOfCircle(circle_6, -self.groove_angle, -self.groove_angle + radians(180), True)
        circle_e_5 = BRepBuilderAPI_MakeEdge(circle_are_5.Value()).Edge()
        circle_e_6 = BRepBuilderAPI_MakeEdge(circle_arc_6.Value()).Edge()  # 槽的半圆边
        groove_f3 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_e_5, e5, circle_e_6, e6).Wire())
        groove3 = BRepPrimAPI_MakePrism(groove_f3.Face(), gp_Vec(0., 0., self.flange_thickness))

        p13 = gp_Pnt(x2 - delta_x_1 - delta_x_2, y2 + delta_y_1 - delta_y_2, 0.)
        p14 = gp_Pnt(x2 - delta_x_1 + delta_x_2, y2 + delta_y_1 + delta_y_2, 0.)
        p15 = gp_Pnt(x2 + delta_x_1 - delta_x_2, y2 - delta_y_1 - delta_y_2, 0.)
        p16 = gp_Pnt(x2 + delta_x_1 + delta_x_2, y2 - delta_y_1 + delta_y_2, 0.)
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p13, p15).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p14, p16).Value()).Edge()  # 槽的两条直角边
        c7 = gp_Pnt(x2 - delta_x_1, y2 + delta_y_1, 0.)
        c8 = gp_Pnt(x2 + delta_x_1, y2 - delta_y_1, 0.)  # 圆心坐标
        circle_7 = gp_Circ(gp_Ax2(c7, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_8 = gp_Circ(gp_Ax2(c8, gp_Dir(0., 0., 1.)), self.groove_width / 2)
        circle_are_7 = GC_MakeArcOfCircle(circle_7, self.groove_angle, self.groove_angle + radians(180), True)
        circle_arc_8 = GC_MakeArcOfCircle(circle_8, self.groove_angle + radians(180), self.groove_angle, True)  # 槽半圆
        circle_e_7 = BRepBuilderAPI_MakeEdge(circle_are_7.Value()).Edge()
        circle_e_8 = BRepBuilderAPI_MakeEdge(circle_arc_8.Value()).Edge()  # 槽的半圆边
        groove_f4 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_e_7, e7, circle_e_8, e8).Wire())
        groove4 = BRepPrimAPI_MakePrism(groove_f4.Face(), gp_Vec(0., 0., self.flange_thickness))
        groove = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(groove1.Shape(), groove2.Shape()).Shape(),
                                  BRepAlgoAPI_Fuse(groove3.Shape(), groove4.Shape()).Shape())

        return groove.Shape()


class Vent(object):  # 通风孔
    def __init__(self, flange_length, flange_width, flange_thickness, vent_x_position, vent_y_position, vent_spacing,
                 first_radius, hole_width=()):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.vent_x_position = float(vent_x_position)  # 孔的x位置
        self.vent_y_position = float(vent_y_position)  # 孔的y位置
        self.vent_spacing = float(vent_spacing)  # 孔的间距
        self.first_radius = float(first_radius)  # 最内孔的半径
        self.hole_width = hole_width  # 每个孔的宽度

    def feature_local(self):
        # 第一个通风孔
        c = gp_Pnt(self.vent_x_position - self.vent_spacing/2, self.vent_y_position + self.vent_spacing/2, 0.)  # 圆心坐标
        axis = gp_Dir(0., 0., 1.)
        circle_axis = gp_Ax2(c, axis)  # 圆的法向量
        circle = gp_Circ(circle_axis, self.first_radius)
        circle_arc = GC_MakeArcOfCircle(circle, radians(90), radians(180), True)
        p1 = gp_Pnt(self.vent_x_position - self.vent_spacing/2 - self.first_radius,
                    self.vent_y_position + self.vent_spacing/2, 0.)
        p2 = gp_Pnt(self.vent_x_position - self.vent_spacing/2,
                    self.vent_y_position + self.vent_spacing/2 + self.first_radius, 0.)
        circle_arc_e = BRepBuilderAPI_MakeEdge(circle_arc.Value())
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c, p1).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c, p2).Value())
        w1 = BRepBuilderAPI_MakeWire(circle_arc_e.Edge(), e1.Edge(), e2.Edge())
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())
        n1 = gp_Vec(0., 0., self.flange_thickness)
        vent = BRepPrimAPI_MakePrism(f1.Face(), n1)
        vent_radius = self.first_radius + self.vent_spacing
        for i in self.hole_width:
            i = float(i)
            circle1 = gp_Circ(circle_axis, vent_radius)
            circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(180), True)
            p3 = gp_Pnt(self.vent_x_position - self.vent_spacing/2 - vent_radius,
                        self.vent_y_position + self.vent_spacing/2, 0.)
            p4 = gp_Pnt(self.vent_x_position - self.vent_spacing/2,
                        self.vent_y_position + self.vent_spacing/2 + vent_radius, 0.)
            vent_radius += i
            circle2 = gp_Circ(circle_axis, vent_radius)
            circle_arc2 = GC_MakeArcOfCircle(circle2, radians(90), radians(180), True)
            p5 = gp_Pnt(self.vent_x_position - self.vent_spacing/2 - vent_radius,
                        self.vent_y_position + self.vent_spacing/2, 0.)
            p6 = gp_Pnt(self.vent_x_position - self.vent_spacing/2,
                        self.vent_y_position + self.vent_spacing/2 + vent_radius, 0.)
            circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())
            circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())
            e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p5).Value())
            e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p6).Value())
            w2 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e3.Edge(), e4.Edge())
            w2.Add(circle_arc_e2.Edge())
            f2 = BRepBuilderAPI_MakeFace(w2.Wire())
            hole = BRepPrimAPI_MakePrism(f2.Face(), n1)
            vent = BRepAlgoAPI_Fuse(vent.Shape(), hole.Shape())
            vent_radius = vent_radius + self.vent_spacing

        # 第二个通风孔
        c1 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2, self.vent_y_position + self.vent_spacing / 2,
                    0.)  # 圆心坐标
        circle_axis_1 = gp_Ax2(c1, axis)  # 圆的法向量
        circle_3 = gp_Circ(circle_axis_1, self.first_radius)
        circle_arc_3 = GC_MakeArcOfCircle(circle_3, radians(0), radians(90), True)
        p7 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + self.first_radius,
                    self.vent_y_position + self.vent_spacing / 2, 0.)
        p8 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                    self.vent_y_position + self.vent_spacing / 2 + self.first_radius, 0.)
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc_3.Value())
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c1, p7).Value())
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c1, p8).Value())
        w3 = BRepBuilderAPI_MakeWire(circle_arc_e3.Edge(), e5.Edge(), e6.Edge())
        f3 = BRepBuilderAPI_MakeFace(w3.Wire())
        vent1 = BRepPrimAPI_MakePrism(f3.Face(), n1)
        vent_radius = self.first_radius + self.vent_spacing
        for i in self.hole_width:
            i = float(i)
            circle4 = gp_Circ(circle_axis_1, vent_radius)
            circle_arc4 = GC_MakeArcOfCircle(circle4, radians(0), radians(90), True)
            p9 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + vent_radius,
                        self.vent_y_position + self.vent_spacing / 2, 0.)
            p10 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                         self.vent_y_position + self.vent_spacing / 2 + vent_radius, 0.)
            vent_radius += i
            circle5 = gp_Circ(circle_axis_1, vent_radius)
            circle_arc5 = GC_MakeArcOfCircle(circle5, radians(0), radians(90), True)
            p11 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + vent_radius,
                         self.vent_y_position + self.vent_spacing / 2, 0.)
            p12 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                         self.vent_y_position + self.vent_spacing / 2 + vent_radius, 0.)
            circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value())
            circle_arc_e5 = BRepBuilderAPI_MakeEdge(circle_arc5.Value())
            e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p11).Value())
            e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p12).Value())
            w4 = BRepBuilderAPI_MakeWire(circle_arc_e4.Edge(), e7.Edge(), e8.Edge())
            w4.Add(circle_arc_e5.Edge())
            f4 = BRepBuilderAPI_MakeFace(w4.Wire())
            hole1 = BRepPrimAPI_MakePrism(f4.Face(), n1)
            vent1 = BRepAlgoAPI_Fuse(vent1.Shape(), hole1.Shape())
            vent_radius = vent_radius + self.vent_spacing

        # 第三个通风孔
        c2 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2, self.vent_y_position - self.vent_spacing / 2,
                    0.)  # 圆心坐标
        circle_axis_2 = gp_Ax2(c2, axis)  # 圆的法向量
        circle_6 = gp_Circ(circle_axis_2, self.first_radius)
        circle_arc_6 = GC_MakeArcOfCircle(circle_6, -radians(90), radians(0), True)
        p13 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + self.first_radius,
                     self.vent_y_position - self.vent_spacing / 2, 0.)
        p14 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                     self.vent_y_position - self.vent_spacing / 2 - self.first_radius, 0.)
        circle_arc_e6 = BRepBuilderAPI_MakeEdge(circle_arc_6.Value())
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c2, p13).Value())
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c2, p14).Value())
        w5 = BRepBuilderAPI_MakeWire(circle_arc_e6.Edge(), e9.Edge(), e10.Edge())
        f5 = BRepBuilderAPI_MakeFace(w5.Wire())
        vent2 = BRepPrimAPI_MakePrism(f5.Face(), n1)
        vent_radius = self.first_radius + self.vent_spacing
        for i in self.hole_width:
            i = float(i)
            circle7 = gp_Circ(circle_axis_2, vent_radius)
            circle_arc7 = GC_MakeArcOfCircle(circle7, -radians(90), radians(0), True)
            p15 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + vent_radius,
                         self.vent_y_position - self.vent_spacing / 2, 0.)
            p16 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                         self.vent_y_position - self.vent_spacing / 2 - vent_radius, 0.)
            vent_radius += i
            circle8 = gp_Circ(circle_axis_2, vent_radius)
            circle_arc8 = GC_MakeArcOfCircle(circle8, -radians(90), radians(0), True)
            p17 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2 + vent_radius,
                         self.vent_y_position - self.vent_spacing / 2, 0.)
            p18 = gp_Pnt(self.vent_x_position + self.vent_spacing / 2,
                         self.vent_y_position - self.vent_spacing / 2 - vent_radius, 0.)
            circle_arc_e7 = BRepBuilderAPI_MakeEdge(circle_arc7.Value())
            circle_arc_e8 = BRepBuilderAPI_MakeEdge(circle_arc8.Value())
            e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p15, p17).Value())
            e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p16, p18).Value())
            w6 = BRepBuilderAPI_MakeWire(circle_arc_e7.Edge(), e11.Edge(), e12.Edge())
            w6.Add(circle_arc_e8.Edge())
            f6 = BRepBuilderAPI_MakeFace(w6.Wire())
            hole2 = BRepPrimAPI_MakePrism(f6.Face(), n1)
            vent2 = BRepAlgoAPI_Fuse(vent2.Shape(), hole2.Shape())
            vent_radius = vent_radius + self.vent_spacing

        # 第四个通风孔
        c3 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2, self.vent_y_position - self.vent_spacing / 2,
                    0.)  # 圆心坐标
        circle_axis_3 = gp_Ax2(c3, axis)  # 圆的法向量
        circle_9 = gp_Circ(circle_axis_3, self.first_radius)
        circle_arc_9 = GC_MakeArcOfCircle(circle_9, -radians(180), -radians(90), True)
        p19 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2 - self.first_radius,
                     self.vent_y_position - self.vent_spacing / 2, 0.)
        p20 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2,
                     self.vent_y_position - self.vent_spacing / 2 - self.first_radius, 0.)
        circle_arc_e9 = BRepBuilderAPI_MakeEdge(circle_arc_9.Value())
        e13 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c3, p19).Value())
        e14 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(c3, p20).Value())
        w7 = BRepBuilderAPI_MakeWire(circle_arc_e9.Edge(), e13.Edge(), e14.Edge())
        f7 = BRepBuilderAPI_MakeFace(w7.Wire())
        vent3 = BRepPrimAPI_MakePrism(f7.Face(), n1)
        vent_radius = self.first_radius + self.vent_spacing
        for i in self.hole_width:
            i = float(i)
            circle10 = gp_Circ(circle_axis_3, vent_radius)
            circle_arc10 = GC_MakeArcOfCircle(circle10, -radians(180), -radians(90), True)
            p21 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2 - vent_radius,
                         self.vent_y_position - self.vent_spacing / 2, 0.)
            p22 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2,
                         self.vent_y_position - self.vent_spacing / 2 - vent_radius, 0.)
            vent_radius += i
            circle11 = gp_Circ(circle_axis_3, vent_radius)
            circle_arc11 = GC_MakeArcOfCircle(circle11, -radians(180), -radians(90), True)
            p23 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2 - vent_radius,
                         self.vent_y_position - self.vent_spacing / 2, 0.)
            p24 = gp_Pnt(self.vent_x_position - self.vent_spacing / 2,
                         self.vent_y_position - self.vent_spacing / 2 - vent_radius, 0.)
            circle_arc_e10 = BRepBuilderAPI_MakeEdge(circle_arc10.Value())
            circle_arc_e11 = BRepBuilderAPI_MakeEdge(circle_arc11.Value())
            e15 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p21, p23).Value())
            e16 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p22, p24).Value())
            w8 = BRepBuilderAPI_MakeWire(circle_arc_e10.Edge(), e15.Edge(), e16.Edge())
            w8.Add(circle_arc_e11.Edge())
            f8 = BRepBuilderAPI_MakeFace(w8.Wire())
            hole3 = BRepPrimAPI_MakePrism(f8.Face(), n1)
            vent3 = BRepAlgoAPI_Fuse(vent3.Shape(), hole3.Shape())
            vent_radius = vent_radius + self.vent_spacing

        vent4 = BRepAlgoAPI_Fuse(vent.Shape(), vent1.Shape())
        vent5 = BRepAlgoAPI_Fuse(vent2.Shape(), vent3.Shape())
        vent_feature = BRepAlgoAPI_Fuse(vent4.Shape(), vent5.Shape())

        return vent_feature.Shape()


class Array(object):  # 阵列
    def __init__(self, flange_length, flange_width, flange_thickness, array_length, array_width,
                 array_x_position, array_y_position, array_spacing, array_num=()):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.array_length = float(array_length)  # 单个矩形长
        self.array_width = float(array_width)  # 单个矩形宽
        self.array_x_position = float(array_x_position)  # 阵列起始x位置
        self.array_y_position = float(array_y_position)  # 阵列起始y位置
        self.array_spacing = float(array_spacing)  # 阵列间距
        self.array_num = array_num  # 阵列数目（n×m）

    def feature_local(self):  # 生成切口特征
        p1 = gp_Pnt(self.array_x_position, self.array_y_position, 0.)
        p2 = gp_Pnt(self.array_x_position + self.array_length, self.array_y_position, 0.)
        p3 = gp_Pnt(self.array_x_position, self.array_y_position + self.array_width, 0.)
        p4 = gp_Pnt(self.array_x_position + self.array_length,
                    self.array_y_position + self.array_width, 0.)  # 单个矩形的四个顶点
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p4).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()  # 切口的四条拓扑边
        w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, e4)  # 生成网格
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成底面
        array = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到切口法兰

        for j in range(0, self.array_num[1], 1):
            j = float(j)
            y = self.array_width * j + self.array_spacing * j
            for i in range(0, self.array_num[0], 1):
                i = float(i)
                x = self.array_length * i + self.array_spacing * i
                p5 = gp_Pnt(self.array_x_position + x, self.array_y_position + y, 0.)
                p6 = gp_Pnt(self.array_x_position + self.array_length + x, self.array_y_position + y, 0.)
                p7 = gp_Pnt(self.array_x_position + x, self.array_y_position + self.array_width + y, 0.)
                p8 = gp_Pnt(self.array_x_position + self.array_length + x,
                            self.array_y_position + self.array_width + y, 0.)  # 单个矩形的四个顶点
                e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
                e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p7).Value()).Edge()
                e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p8).Value()).Edge()
                e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()  # 切口的四条拓扑边
                w2 = BRepBuilderAPI_MakeWire(e5, e6, e7, e8)  # 生成网格
                f2 = BRepBuilderAPI_MakeFace(w2.Wire())  # 生成底面
                rip_flange = BRepPrimAPI_MakePrism(f2.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到切口法兰

                array = BRepAlgoAPI_Fuse(array.Shape(), rip_flange.Shape())  # 布尔减

        return array.Shape()


class ProfiledGroove(object):  # 折弯槽
    def __init__(self, flange_length, flange_width, flange_thickness, bend_radius, bend_height, bend5_radius,
                 bend5_width, groove_position, groove_w_in_bend, groove_l_in_bend, groove_l_in_flange, groove_num):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend_radius = float(bend_radius)  # 基本折弯半径（外）
        self.bend_height = float(bend_height)  # 基本折弯高度，这里指边线法兰的长度
        self.bend5_angle = float(radians(70))  # 四次折弯的角度
        self.bend5_radius = float(bend5_radius)  # 四次折弯的半径
        self.bend5_width = float(bend5_width)  # 四次折弯的宽度
        self.groove_position = float(groove_position)  # 槽的位置
        self.groove_w_in_bend = float(groove_w_in_bend)  # 折弯槽的宽
        self.groove_l_in_bend = float(groove_l_in_bend)  # 槽在第二个折弯上的长度
        self.groove_l_in_flange = float(groove_l_in_flange)  # 槽在第一个折弯上的长度
        self.groove_num = int(groove_num)  # 槽的数目

    def single_flange(self, position):
        z = self.bend_radius + self.bend_height - self.bend5_radius
        inter_radius = self.bend5_radius - self.flange_thickness
        c1 = gp_Pnt(self.bend5_radius - self.bend_radius, position, z)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend5_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        x1 = -self.bend_radius + self.bend5_radius - self.bend5_radius * cos(self.bend5_angle)
        x2 = -self.bend_radius + self.bend5_radius - inter_radius * cos(self.bend5_angle)  # x坐标
        z1 = z + self.bend5_radius * sin(self.bend5_angle)
        z2 = z + inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        p1 = gp_Pnt(-self.bend_radius, position, z)
        p2 = gp_Pnt(self.flange_thickness - self.bend_radius, position, z)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, position, z1), gp_Pnt(x2, position, z2)).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        bend_arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.groove_w_in_bend, 0.))  # 生成折弯弧

        c2 = gp_Pnt(x1 + self.groove_l_in_bend * sin(self.bend5_angle), position + self.groove_w_in_bend/2,
                    z1 + self.groove_l_in_bend * cos(self.bend5_angle))
        axis_1 = gp_Dir(cos(self.bend5_angle), 0., -sin(self.bend5_angle))
        circle3 = gp_Circ(gp_Ax2(c2, axis_1), self.groove_w_in_bend / 2)
        circle_arc3 = GC_MakeArcOfCircle(circle3, radians(90), -radians(90), True)
        p3 = gp_Pnt(x1, position + self.groove_w_in_bend, z1)
        p4 = gp_Pnt(x1 + self.groove_l_in_bend * sin(self.bend5_angle), position,
                    z1 + self.groove_l_in_bend * cos(self.bend5_angle))
        p5 = gp_Pnt(x1 + self.groove_l_in_bend * sin(self.bend5_angle), position + self.groove_w_in_bend,
                    z1 + self.groove_l_in_bend * cos(self.bend5_angle))
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc3.Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, position, z1), p3).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, position, z1), p4).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p5).Value()).Edge()
        groove1_f = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e3, e4, e5, circle_arc_e3).Wire())
        n1 = gp_Vec(self.flange_thickness * cos(self.bend5_angle), 0., -self.flange_thickness * sin(self.bend5_angle))
        groove1 = BRepPrimAPI_MakePrism(groove1_f.Face(), n1)  # 生成边线法兰

        c3 = gp_Pnt(-self.bend_radius, position + self.groove_w_in_bend/2, z - self.groove_l_in_flange)
        circle4 = gp_Circ(gp_Ax2(c3, gp_Dir(1., 0., 0.)), self.groove_w_in_bend / 2)  # 外圆
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(90), -radians(90), True)  # 外圆弧一定要注意起始角度和终止角度
        p6 = gp_Pnt(-self.bend_radius, position, z - self.groove_l_in_flange)
        p7 = gp_Pnt(-self.bend_radius, position + self.groove_w_in_bend, z)
        p8 = gp_Pnt(-self.bend_radius, position + self.groove_w_in_bend, z - self.groove_l_in_flange)
        circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(-self.bend_radius, position, z), p6).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(-self.bend_radius, position, z), p7).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        groove2_f = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(circle_arc_e4, e6, e7, e8).Wire())
        groove2 = BRepPrimAPI_MakePrism(groove2_f.Face(), gp_Vec(self.flange_thickness, 0., 0.))
        groove = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(bend_arc.Shape(), groove1.Shape()).Shape(), groove2.Shape())

        return groove

    def feature_local(self):
        cut_feature = self.single_flange(self.groove_position)
        p = self.groove_position
        for i in range(self.groove_num):
            p_increment = p + (self.groove_w_in_bend + 2.0) * i
            single = self.single_flange(p_increment)
            cut_feature = BRepAlgoAPI_Fuse(cut_feature.Shape(), single.Shape())

        return cut_feature.Shape()

    def bend_part(self):
        inter_radius = self.bend5_radius - self.flange_thickness
        y1 = self.flange_width / 2 - self.bend5_width / 2
        z1 = self.bend_radius + self.bend_height - self.bend5_radius
        c1 = gp_Pnt(self.bend5_radius - self.bend_radius, y1, z1)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend5_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(270), radians(270) + self.bend5_angle, True)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        dx1 = self.bend5_radius - self.bend5_radius * cos(self.bend5_angle)
        dx2 = self.bend5_radius - inter_radius * cos(self.bend5_angle)  # y坐标
        dz1 = self.bend5_radius * sin(self.bend5_angle)
        dz2 = inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        p1 = gp_Pnt(dx1 - self.bend_radius, y1, z1 + dz1)
        p2 = gp_Pnt(dx2 - self.bend_radius, y1, z1 + dz2)
        p3 = gp_Pnt(-self.bend_radius, y1, z1)
        p4 = gp_Pnt(self.flange_thickness - self.bend_radius, y1, z1)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value())  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.bend5_width, 0.))  # 生成折弯弧
        bend_arc = BRepAlgoAPI_Cut(arc.Shape(), self.feature_local())

        return bend_arc.Shape()


class ProfiledArray(object):  # 折弯槽
    def __init__(self, flange_length, flange_width, flange_thickness, bend_radius, bend_height, array_position,
                 array_w_in_bend, array_l_in_bend, array_l_in_flange, array_num):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend_radius = float(bend_radius)  # 基本折弯半径（外）
        self.bend_height = float(bend_height)  # 基本折弯高度，这里指边线法兰的长度
        self.array_position = float(array_position)  # 方孔的位置
        self.array_w_in_bend = float(array_w_in_bend)  # 折弯方孔的宽
        self.array_l_in_bend = float(array_l_in_bend)  # 方孔在第二个折弯上的长度
        self.array_l_in_flange = float(array_l_in_flange)  # 方孔第一个折弯上的长度
        self.array_num = int(array_num)  # 方孔的数目

    def single_flange(self, position):
        inter_radius = self.bend_radius - self.flange_thickness
        circle1 = gp_Circ(gp_Ax2(gp_Pnt(0., position, self.bend_radius), gp_Dir(0., 1., 0.)), self.bend_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(gp_Pnt(0., position, self.bend_radius), gp_Dir(0., 1., 0.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(180), radians(270), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(180), radians(270), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        p1 = gp_Pnt(-self.bend_radius, position, self.bend_radius)
        p2 = gp_Pnt(-inter_radius, position, self.bend_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(0., position, 0.),
                                                    gp_Pnt(0., position, self.flange_thickness)).Value())
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        bend_arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.array_w_in_bend, 0.))  # 生成折弯弧

        p3 = gp_Pnt(-self.bend_radius, position + self.array_w_in_bend, self.bend_radius)
        p4 = gp_Pnt(-self.bend_radius, position, self.bend_radius + self.array_l_in_bend)
        p5 = gp_Pnt(-self.bend_radius, position + self.array_w_in_bend, self.bend_radius + self.array_l_in_bend)
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p4).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p5).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value()).Edge()
        array1_f = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e3, e4, e5, e6).Wire())  # 绘制边线法兰的底面
        array1 = BRepPrimAPI_MakePrism(array1_f.Face(), gp_Vec(self.flange_thickness, 0., 0.))  # 生成边线法兰

        p6 = gp_Pnt(0., position + self.array_w_in_bend, 0.)
        p7 = gp_Pnt(self.array_l_in_flange, position, 0.)
        p8 = gp_Pnt(self.array_l_in_flange, position + self.array_w_in_bend, 0.)
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(0., position, 0.), p6).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(0., position, 0.), p7).Value()).Edge()
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p8).Value()).Edge()
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p8).Value()).Edge()
        array2_f = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e7, e8, e9, e10).Wire())
        array2 = BRepPrimAPI_MakePrism(array2_f.Face(), gp_Vec(0., 0., self.flange_thickness))
        array = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(bend_arc.Shape(), array1.Shape()).Shape(), array2.Shape())

        return array

    def feature_local(self):
        cut_feature = self.single_flange(self.array_position)
        p = self.array_position
        for i in range(self.array_num):
            p_increment = p + (self.array_w_in_bend + 5.0) * i
            single = self.single_flange(p_increment)
            cut_feature = BRepAlgoAPI_Fuse(cut_feature.Shape(), single.Shape())

        return cut_feature.Shape()

    def bend_part(self):
        c1 = gp_Pnt(0., 0., self.bend_radius)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 1., 0.)), self.bend_radius - self.flange_thickness)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(180), radians(270), True)  # 外圆弧一定要注意起始角度和终止角度
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(180), radians(270), True)  # 内圆弧一定要注意起始角度和终止角度
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        p1 = gp_Pnt(-self.bend_radius, 0., self.bend_radius)
        p2 = gp_Pnt(self.flange_thickness - self.bend_radius, 0., self.bend_radius)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(0., 0., 0.), gp_Pnt(0., 0., self.flange_thickness)).Value())
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., self.flange_width, 0.))  # 生成折弯弧
        bend_arc = BRepAlgoAPI_Cut(arc.Shape(), self.feature_local())

        return bend_arc.Shape()


class Bend(object):  # 二次折弯
    def __init__(self, flange_length, flange_width, flange_thickness, bend4_radius, bend4_height, bend4_width,
                 bend5_radius, bend5_angle, bend5_length):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend4_radius = float(bend4_radius)  # 四次折弯的半径
        self.bend4_height = float(bend4_height)  # 四次折弯的高度
        self.bend4_width = float(bend4_width)  # 四次折弯的宽度
        self.bend5_radius = float(bend5_radius)  # 五次折弯半径
        self.bend5_angle = float(radians(bend5_angle))  # 五次折弯角（度转为弧度)
        self.bend5_length = float(bend5_length)  # 五次折弯延伸的长度

    def bend_part(self):
        inter_radius = self.bend5_radius - self.flange_thickness
        x = self.flange_length / 2 - self.bend4_width / 2
        y = self.flange_thickness
        z = self.flange_thickness - self.bend4_radius
        c1 = gp_Pnt(x, y - self.bend5_radius, z)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), self.bend5_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(90), radians(90) + self.bend5_angle, True)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(90), radians(90) + self.bend5_angle, True)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value()).Edge()  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value()).Edge()  # 内圆弧边
        x1 = x - self.bend5_radius * sin(self.bend5_angle)
        x2 = x - inter_radius * sin(self.bend5_angle)  # x坐标
        y1 = y - self.bend5_radius + self.bend5_radius * cos(self.bend5_angle)
        y2 = y - self.bend5_radius + inter_radius * cos(self.bend5_angle)  # y坐标
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, y1, z), gp_Pnt(x2, y2, z)).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x, y, z), gp_Pnt(x, 0., z)).Value()).Edge()  # 生成圆弧环的另外两条直边
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1, e1, circle_arc_e2, e2)
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        arc1 = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., 0., -self.bend4_height))  # 生成折弯弧

        c2 = gp_Pnt(x + self.bend4_width, y - self.bend5_radius, z)  # 圆心坐标
        circle3 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 0., 1.)), self.bend5_radius)  # 外圆
        circle4 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 0., 1.)), inter_radius)  # 内圆
        circle_arc3 = GC_MakeArcOfCircle(circle3, radians(90) - self.bend5_angle, radians(90), True)
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(90) - self.bend5_angle, radians(90), True)
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc3.Value()).Edge()  # 外圆弧边
        circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value()).Edge()  # 内圆弧边
        x3 = x + self.bend4_width + self.bend5_radius * sin(self.bend5_angle)
        x4 = x + self.bend4_width + inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x3, y1, z), gp_Pnt(x4, y2, z)).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x + self.bend4_width, y, z),
                                                    gp_Pnt(x + self.bend4_width, 0., z)).Value()).Edge()
        circle_arc_w2 = BRepBuilderAPI_MakeWire(circle_arc_e3, e3, circle_arc_e4, e4)
        circle_arc_f2 = BRepBuilderAPI_MakeFace(circle_arc_w2.Wire())  # 生成圆弧环面
        arc2 = BRepPrimAPI_MakePrism(circle_arc_f2.Face(), gp_Vec(0., 0., -self.bend4_height))  # 生成折弯弧
        bend_arc = BRepAlgoAPI_Fuse(arc1.Shape(), arc2.Shape())

        return bend_arc.Shape()

    def flange_part(self):
        inter_radius = self.bend5_radius - self.flange_thickness
        x = self.flange_length / 2 - self.bend4_width / 2
        z = self.flange_thickness - self.bend4_radius
        x1 = x - self.bend5_radius * sin(self.bend5_angle)
        x2 = x - inter_radius * sin(self.bend5_angle)  # x坐标
        y1 = self.flange_thickness - self.bend5_radius + self.bend5_radius * cos(self.bend5_angle)
        y2 = self.flange_thickness - self.bend5_radius + inter_radius * cos(self.bend5_angle)  # y坐标
        p1 = gp_Pnt(x1, y1, z - self.bend4_height)
        p2 = gp_Pnt(x2, y2, z - self.bend4_height)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, y1, z), gp_Pnt(x2, y2, z)).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, y1, z), p1).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x2, y2, z), p2).Value()).Edge()
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        edge_flange_f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e1, e2, e3, e4).Wire())  # 绘制边线法兰的底面
        n1 = gp_Vec(-self.bend5_length * cos(self.bend5_angle), -self.bend5_length * sin(self.bend5_angle), 0.)
        flange1 = BRepPrimAPI_MakePrism(edge_flange_f1.Face(), n1)  # 生成边线法兰

        x3 = x + self.bend4_width + self.bend5_radius * sin(self.bend5_angle)
        x4 = x + self.bend4_width + inter_radius * sin(self.bend5_angle)  # z坐标，注意是折弯半径减
        p3 = gp_Pnt(x3, y1, z - self.bend4_height)
        p4 = gp_Pnt(x4, y2, z - self.bend4_height)
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x3, y1, z), gp_Pnt(x4, y2, z)).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x3, y1, z), p3).Value()).Edge()
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x4, y2, z), p4).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
        edge_flange_f2 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e5, e6, e7, e8).Wire())  # 绘制边线法兰的底面
        n2 = gp_Vec(self.bend5_length * cos(self.bend5_angle), -self.bend5_length * sin(self.bend5_angle), 0.)
        flange2 = BRepPrimAPI_MakePrism(edge_flange_f2.Face(), n2)  # 生成边线法兰
        bend_flange = BRepAlgoAPI_Fuse(flange1.Shape(), flange2.Shape())  # 布尔并

        return bend_flange.Shape()

    def feature_local(self):
        bend = BRepAlgoAPI_Fuse(self.bend_part(), self.flange_part())

        return bend.Shape()


class Roll (object):  # 卷圆
    def __init__(self, flange_length, flange_width, flange_thickness, bend1_radius, bend1_height, bend2_radius,
                 bend2_length, bend3_radius, bend3_height, bend3_width, roll_angle, roll_radius, groove_length,
                 groove_width):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.bend1_radius = float(bend1_radius)  # 一次折弯的半径
        self.bend1_height = float(bend1_height)  # 一次折弯延伸的长度
        self.bend2_radius = float(bend2_radius)  # 二次折弯的半径
        self.bend2_length = float(bend2_length)  # 二次折弯延伸的长度
        self.bend3_radius = float(bend3_radius)  # 三次折弯的半径
        self.bend3_height = float(bend3_height)  # 三次折弯的高度
        self.bend3_width = float(bend3_width)  # 三次折弯的宽度
        self.roll_angle = float(radians(roll_angle))  # 卷圆角（度转为弧度）
        self.roll_radius = float(roll_radius)  # 卷圆半径（外）
        self.groove_length = float(groove_length)  # 槽的长
        self.groove_width = float(groove_width)  # 槽的宽

    def roll_part(self):  # 生成卷圆特征
        x = self.flange_length + self.bend1_radius + self.bend2_radius - 2 * self.flange_thickness + self.bend2_length
        y = self.flange_width / 2 - self.bend3_width / 2
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness + self.bend3_radius
        inter_radius = self.roll_radius - self.flange_thickness
        circle1 = gp_Circ(gp_Ax2(gp_Pnt(x + self.roll_radius, y, z), gp_Dir(0., 0., 1.)), self.roll_radius)  # 外圆
        circle2 = gp_Circ(gp_Ax2(gp_Pnt(x + self.roll_radius, y, z), gp_Dir(0., 0., 1.)), inter_radius)  # 内圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(180), radians(180) + self.roll_angle, True)
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(180), radians(180) + self.roll_angle, True)
        circle_arc_e1 = BRepBuilderAPI_MakeEdge(circle_arc1.Value())  # 外圆弧边
        circle_arc_e2 = BRepBuilderAPI_MakeEdge(circle_arc2.Value())  # 内圆弧边
        x1 = x + self.roll_radius - self.roll_radius * cos(self.roll_angle)
        x2 = x + self.roll_radius - inter_radius * cos(self.roll_angle)  # x坐标
        y1 = y - self.roll_radius * sin(self.roll_angle)
        y2 = y - inter_radius * sin(self.roll_angle)  # z坐标，注意是折弯半径减
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x1, y1, z), gp_Pnt(x2, y2, z)).Value())
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x, y, z), gp_Pnt(x + self.flange_thickness, y, z)).Value())
        circle_arc_w1 = BRepBuilderAPI_MakeWire(circle_arc_e1.Edge(), e1.Edge(), circle_arc_e2.Edge(), e2.Edge())
        circle_arc_f1 = BRepBuilderAPI_MakeFace(circle_arc_w1.Wire())  # 生成圆弧环面
        roll1 = BRepPrimAPI_MakePrism(circle_arc_f1.Face(), gp_Vec(0., 0., self.bend3_height))  # 生成卷圆

        p = y + self.bend3_width
        circle3 = gp_Circ(gp_Ax2(gp_Pnt(x + self.roll_radius, p, z), gp_Dir(0., 0., 1.)), self.roll_radius)  # 外圆
        circle4 = gp_Circ(gp_Ax2(gp_Pnt(x + self.roll_radius, p, z), gp_Dir(0., 0., 1.)), inter_radius)  # 内圆
        circle_arc3 = GC_MakeArcOfCircle(circle3, radians(180) - self.roll_angle, radians(180), True)
        circle_arc4 = GC_MakeArcOfCircle(circle4, radians(180) - self.roll_angle, radians(180), True)
        circle_arc_e3 = BRepBuilderAPI_MakeEdge(circle_arc3.Value())  # 外圆弧边
        circle_arc_e4 = BRepBuilderAPI_MakeEdge(circle_arc4.Value())  # 内圆弧边
        x3 = x + self.roll_radius - self.roll_radius * cos(self.roll_angle)
        x4 = x + self.roll_radius - inter_radius * cos(self.roll_angle)  # x坐标
        y3 = p + self.roll_radius * sin(self.roll_angle)
        y4 = p + inter_radius * sin(self.roll_angle)  # z坐标，注意是折弯半径减
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x3, y3, z), gp_Pnt(x4, y4, z)).Value())
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(gp_Pnt(x, p, z), gp_Pnt(x + self.flange_thickness, p, z)).Value())
        circle_arc_w2 = BRepBuilderAPI_MakeWire(circle_arc_e3.Edge(), e3.Edge(), circle_arc_e4.Edge(), e4.Edge())
        circle_arc_f2 = BRepBuilderAPI_MakeFace(circle_arc_w2.Wire())  # 生成圆弧环面
        roll2 = BRepPrimAPI_MakePrism(circle_arc_f2.Face(), gp_Vec(0., 0., self.bend3_height))  # 生成卷圆
        roll = BRepAlgoAPI_Fuse(roll1.Shape(), roll2.Shape())

        return roll.Shape()

    def groove_part(self):  # 生成槽特征
        x = self.flange_length + self.bend1_radius + self.bend2_radius - 2 * self.flange_thickness + self.bend2_length
        x = x + self.roll_radius
        y = self.flange_width / 2 - self.bend3_width / 2
        z = self.bend1_radius + self.bend1_height + self.bend2_radius - self.flange_thickness + self.bend3_radius
        z = z + self.bend3_height / 2
        p1 = gp_Pnt(x, y, z - self.groove_length / 2)
        p2 = gp_Pnt(x, y - self.roll_radius - 1.0, z - self.groove_length / 2)
        p3 = gp_Pnt(x - self.groove_width / 2, y - self.roll_radius - 1.0, z - self.groove_length / 2)
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p1).Value()).Edge()
        f1 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e1, e2, e3).Wire())
        cone1 = BRepPrimAPI_MakeRevol(f1.Face(), gp_Ax1(p2, gp_Dir(0., 1., 0.)))
        p4 = gp_Pnt(x, y, z + self.groove_length / 2)
        p5 = gp_Pnt(x, y - self.roll_radius - 1.0, z + self.groove_length / 2)
        p6 = gp_Pnt(x - self.groove_width / 2, y - self.roll_radius - 1.0, z + self.groove_length / 2)
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p5).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p4).Value()).Edge()
        f2 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e4, e5, e6).Wire())
        cone2 = BRepPrimAPI_MakeRevol(f2.Face(), gp_Ax1(p5, gp_Dir(0., 1., 0.)))
        p7 = gp_Pnt(x + self.groove_width / 2, y - self.roll_radius - 1.0, z - self.groove_length / 2)
        e7 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p3).Value()).Edge()
        e8 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p7).Value()).Edge()
        e9 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p7, p1).Value()).Edge()
        f3 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e7, e8, e9).Wire())
        column1 = BRepPrimAPI_MakePrism(f3.Face(), gp_Vec(0., 0., self.groove_length))

        p = y + self.bend3_width
        p8 = gp_Pnt(x, p, z - self.groove_length / 2)
        p9 = gp_Pnt(x, p + self.roll_radius + 1.0, z - self.groove_length / 2)
        p10 = gp_Pnt(x - self.groove_width / 2, p + self.roll_radius + 1.0, z - self.groove_length / 2)
        e10 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p8, p9).Value()).Edge()
        e11 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p9, p10).Value()).Edge()
        e12 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p8).Value()).Edge()
        f4 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e10, e11, e12).Wire())
        cone3 = BRepPrimAPI_MakeRevol(f4.Face(), gp_Ax1(p9, gp_Dir(0., -1., 0.)))
        p11 = gp_Pnt(x, p, z + self.groove_length / 2)
        p12 = gp_Pnt(x, p + self.roll_radius + 1.0, z + self.groove_length / 2)
        p13 = gp_Pnt(x - self.groove_width / 2, p + self.roll_radius + 1.0, z + self.groove_length / 2)
        e13 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p11, p12).Value()).Edge()
        e14 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p12, p13).Value()).Edge()
        e15 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p13, p11).Value()).Edge()
        f5 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e13, e14, e15).Wire())
        cone4 = BRepPrimAPI_MakeRevol(f5.Face(), gp_Ax1(p5, gp_Dir(0., -1., 0.)))
        p14 = gp_Pnt(x + self.groove_width / 2, p + self.roll_radius + 1.0, z - self.groove_length / 2)
        e16 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p8, p10).Value()).Edge()
        e17 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p10, p14).Value()).Edge()
        e18 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p14, p8).Value()).Edge()
        f6 = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(e16, e17, e18).Wire())
        column2 = BRepPrimAPI_MakePrism(f6.Face(), gp_Vec(0., 0., self.groove_length))
        cut1 = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(cone1.Shape(), cone2.Shape()).Shape(), column1.Shape())
        cut2 = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(cone3.Shape(), cone4.Shape()).Shape(), column2.Shape())
        groove = BRepAlgoAPI_Common(BRepAlgoAPI_Fuse(cut1.Shape(), cut2.Shape()).Shape(), self.roll_part())

        return groove.Shape()

    def feature_local(self):  # 生成带孔的卷圆
        feature_local = BRepAlgoAPI_Cut(self.roll_part(), self.groove_part())

        return feature_local.Shape()


class EarPlate(object):  # 耳板类
    def __init__(self, flange_length, flange_width, flange_thickness, ear_length, ear_width, ear_position, ear_radius):

        self.flange_length = float(flange_length)  # 基体法兰的长
        self.flange_width = float(flange_width)  # 基体法兰的宽
        self.flange_thickness = float(flange_thickness)  # 基体法兰的厚度
        self.ear_length = float(ear_length)  # 耳板长，指直边部分长度
        self.ear_width = float(ear_width)  # 耳板宽
        self.ear_position = float(ear_position)  # 耳板位置
        self.ear_radius = float(ear_radius)  # 耳板孔径

    def hole_part(self):
        external_radius = self.ear_width / 2  # 耳板的外半径
        c1 = gp_Pnt(self.ear_position + external_radius, self.flange_width + self.ear_length, 0.)  # 圆心坐标
        circle_arc1 = GC_MakeCircle(gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), self.ear_radius))
        circle_arc1_e = BRepBuilderAPI_MakeEdge(circle_arc1.Value())
        circle_arc1_w = BRepBuilderAPI_MakeWire(circle_arc1_e.Edge())
        circle_arc1_f = BRepBuilderAPI_MakeFace(circle_arc1_w.Wire())
        hole1 = BRepPrimAPI_MakePrism(circle_arc1_f.Face(), gp_Vec(0., 0., self.flange_thickness))  # 生成耳板的孔

        c2 = gp_Pnt(self.flange_length - self.ear_position - external_radius, self.flange_width + self.ear_length, 0.)
        circle_arc2 = GC_MakeCircle(gp_Circ(gp_Ax2(c2, gp_Dir(0., 0., 1.)), self.ear_radius))
        circle_arc2_e = BRepBuilderAPI_MakeEdge(circle_arc2.Value())
        circle_arc2_w = BRepBuilderAPI_MakeWire(circle_arc2_e.Edge())
        circle_arc2_f = BRepBuilderAPI_MakeFace(circle_arc2_w.Wire())
        hole2 = BRepPrimAPI_MakePrism(circle_arc2_f.Face(), gp_Vec(0., 0., self.flange_thickness))  # 生成耳板的孔
        ear_hole = BRepAlgoAPI_Fuse(hole1.Shape(), hole2.Shape())

        return ear_hole.Shape()

    def feature_local(self):  # 生成耳板特征
        external_radius = self.ear_width / 2  # 耳板的外半径
        p1 = gp_Pnt(self.ear_position, self.flange_width, 0.)
        p2 = gp_Pnt(self.ear_position + self.ear_width, self.flange_width, 0.)
        p3 = gp_Pnt(self.ear_position + self.ear_width, self.flange_width + self.ear_length, 0.)
        p4 = gp_Pnt(self.ear_position, self.flange_width + self.ear_length, 0.)  # 耳板的四个顶点
        c1 = gp_Pnt(self.ear_position + external_radius, self.flange_width + self.ear_length, 0.)  # 圆心坐标
        circle1 = gp_Circ(gp_Ax2(c1, gp_Dir(0., 0., 1.)), external_radius)  # 外圆
        circle_arc1 = GC_MakeArcOfCircle(circle1, radians(0), radians(180), True)  # 外圆弧
        e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
        e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
        e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p4).Value()).Edge()
        circle_arc1_e = BRepBuilderAPI_MakeEdge(circle_arc1.Value()).Edge()  # 耳板的四条拓扑边
        w1 = BRepBuilderAPI_MakeWire(e1, e2, e3, circle_arc1_e)  # 生成网格
        f1 = BRepBuilderAPI_MakeFace(w1.Wire())  # 生成底面
        ear_flange1 = BRepPrimAPI_MakePrism(f1.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到耳板法兰

        p5 = gp_Pnt(self.flange_length - self.ear_position, self.flange_width, 0.)
        p6 = gp_Pnt(self.flange_length - self.ear_position - self.ear_width, self.flange_width, 0.)
        p7 = gp_Pnt(self.flange_length - self.ear_position - self.ear_width, self.flange_width + self.ear_length, 0.)
        p8 = gp_Pnt(self.flange_length - self.ear_position, self.flange_width + self.ear_length, 0.)  # 耳板的四个顶点
        c2 = gp_Pnt(self.flange_length - self.ear_position - external_radius, self.flange_width + self.ear_length, 0.)
        circle2 = gp_Circ(gp_Ax2(c2, gp_Dir(0., 0., 1.)), external_radius)  # 外圆
        circle_arc2 = GC_MakeArcOfCircle(circle2, radians(0), radians(180), True)  # 外圆弧
        e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p6).Value()).Edge()
        e5 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p6, p7).Value()).Edge()
        e6 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p5, p8).Value()).Edge()
        circle_arc2_e = BRepBuilderAPI_MakeEdge(circle_arc2.Value()).Edge()  # 耳板的四条拓扑边
        w2 = BRepBuilderAPI_MakeWire(e4, e5, e6, circle_arc2_e)  # 生成网格
        f2 = BRepBuilderAPI_MakeFace(w2.Wire())  # 生成底面
        ear_flange2 = BRepPrimAPI_MakePrism(f2.Face(), gp_Vec(0., 0., self.flange_thickness))  # 拉伸得到耳板法兰
        ear_flange = BRepAlgoAPI_Fuse(ear_flange1.Shape(), ear_flange2.Shape())
        ear_plate = BRepAlgoAPI_Cut(ear_flange.Shape(), self.hole_part())  # 布尔减

        return ear_plate.Shape()


#展示模型代码
#new_compound = ProfiledArray(50, 90, 1, 3, 44, 20, 3, 3, 3, 5).feature_local()
#display, start_display, add_menu, add_function_to_menu = init_display()  # 初始化
#display.DisplayShape(new_compound, update=True)

#display.FitAll()
#start_display()
