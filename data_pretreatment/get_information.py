import numpy as np
from math import pi
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.gp import gp_Pnt
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface, shapeanalysis_GetFaceUVBounds
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Cone, GeomAbs_Sphere, \
    GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, \
    GeomAbs_OffsetSurface, GeomAbs_OtherSurface, GeomAbs_Line, GeomAbs_Circle, GeomAbs_Ellipse, GeomAbs_Hyperbola,\
    GeomAbs_Parabola, GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_OffsetCurve, GeomAbs_OtherCurve
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.TopAbs import TopAbs_FORWARD, TopAbs_REVERSED
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import topods_Face
from OCC.Core.gp import gp_Vec
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.BRepLProp import BRepLProp_SLProps


EPSILON = 1e-6


class WorkFace:
    def __init__(self, index, face):
        self.index = index
        self.hash = hash(face)
        self.face = face
        self.surface_area = None
        self.normal = None
        self.curvature1 = None
        self.curvature2 = None
        self.face_type = None
        self.label = None


class WorkEdge:
    def __init__(self, index, edge):
        self.index = index
        self.hash = hash(edge)
        self.edge = edge
        self.faces = []
        self.hash_faces = []
        self.face_tags = []
        self.convexity = None
        self.dihedral = None
        self.curve_length = None
        self.edge_type = None


def ask_point_uv2(xyz, face):
    # 从xyz坐标给出uv坐标的通用函数，uv值未标准化
    gp_pnt = gp_Pnt(float(xyz[0]), float(xyz[1]), float(xyz[2]))
    surface = BRep_Tool().Surface(face)

    sas = ShapeAnalysis_Surface(surface)
    gp_pnt2d = sas.ValueOfUV(gp_pnt, 0.01)
    uv = list(gp_pnt2d.Coord())

    return uv


def ask_point_normal_face(uv, face):
    # 给定一个点在面上的uv坐标，求该点的法向量
    face_ds = topods_Face(face)
    surface = BRep_Tool().Surface(face_ds)
    props = GeomLProp_SLProps(surface, uv[0], uv[1], 1, 1e-6)

    gp_dir = props.Normal()
    if face.Orientation() == TopAbs_REVERSED:
        gp_dir.Reverse()

    return gp_dir.Coord()


def ask_edge_mid_pnt_tangent(edge):
    # 求边的中点和中点处的切线
    result = BRep_Tool.Curve(edge)  # result[0] is the handle of curve;result[1] is the u_min; result[2] is u_max
    t_mid = (result[1] + result[2]) / 2
    p = gp_Pnt(0, 0, 0)
    v1 = gp_Vec(0, 0, 0)
    result[0].D1(t_mid, p, v1)  # handle.GetObject() gives Geom_Curve type, p:gp_Pnt, v1:gp_Vec

    return [p.Coord(), v1.Coord()]


def edge_concavity(edge, faces):
    # 计算边的凹凸性
    [mid_pnt, tangent] = ask_edge_mid_pnt_tangent(edge)
    uv0 = ask_point_uv2(mid_pnt, faces[0])
    uv1 = ask_point_uv2(mid_pnt, faces[1])
    n0 = ask_point_normal_face(uv0, faces[0])
    n1 = ask_point_normal_face(uv1, faces[1])

    if edge.Orientation() == TopAbs_FORWARD:
        cp = np.cross(n0, n1)
        r = np.dot(cp, tangent)
        s = np.sign(r)

    else:
        cp = np.cross(n1, n0)
        r = np.dot(cp, tangent)
        s = np.sign(r)

    return s


def edge_dihedral(edge, faces):
    # 计算边的二面角
    [mid_pnt, _] = ask_edge_mid_pnt_tangent(edge)
    uv0 = ask_point_uv2(mid_pnt, faces[0])
    uv1 = ask_point_uv2(mid_pnt, faces[1])
    n0 = ask_point_normal_face(uv0, faces[0])
    n1 = ask_point_normal_face(uv1, faces[1])
    n0_norm = np.linalg.norm(n0)
    n1_norm = np.linalg.norm(n1)
    x = n0_norm * n1_norm + EPSILON
    y = np.dot(n0, n1) / x
    z = pi - np.arccos(y)

    return z


def ask_curve_length(edge):
    props = GProp_GProps()

    brepgprop_LinearProperties(edge, props)
    length = props.Mass()
    return length


def recognise_edge_type(edge):
    # 判断B-rep边的曲线种类
    # BRepAdaptor to get the edge curve, GetType() to get the type of geometrical curve type
    cur = BRepAdaptor_Curve(edge)
    cur_type = cur.GetType()
    e = 0
    if cur_type == GeomAbs_Line:
        e = 1
    elif cur_type == GeomAbs_Circle:
        e = 2
    elif cur_type == GeomAbs_Ellipse:
        e = 3
    elif cur_type == GeomAbs_Hyperbola:
        e = 4
    elif cur_type == GeomAbs_Parabola:
        e = 5
    elif cur_type == GeomAbs_BezierCurve:
        e = 6
    elif cur_type == GeomAbs_BSplineCurve:
        e = 7
    elif cur_type == GeomAbs_OffsetCurve:
        e = 8
    elif cur_type == GeomAbs_OtherCurve:
        e = 9

    return e


def get_edges(topo, occ_faces):
    work_edges = {}

    edges = topo.edges()
    for edge in edges:
        faces = list(topo.faces_from_edge(edge))

        we = WorkEdge(len(work_edges), edge)

        if len(faces) > 1:
            s = edge_concavity(edge, faces)
            we.dihedral = edge_dihedral(edge, faces)
        else:
            s = 0
            we.dihedral = pi

        if s == 1:
            # Convex
            edge_convexity = 1
        elif s == -1:
            # Concave
            edge_convexity = 2
        else:
            # Smooth (s==0) or other
            edge_convexity = 3

        we.convexity = edge_convexity
        we.faces = faces
        we.curve_length = ask_curve_length(edge)
        we.edge_type = recognise_edge_type(edge)

        for face in faces:
            we.hash_faces.append(hash(face))
            we.face_tags.append(occ_faces.index(face))

        if len(faces) == 1:
            we.hash_faces.append(hash(faces[0]))
            we.face_tags.append(occ_faces.index(faces[0]))

        work_edges[we.hash] = we

    return work_edges


def ask_surface_area(f):
    props = GProp_GProps()

    brepgprop_SurfaceProperties(f, props)
    area = props.Mass()
    return area


def sample_point_curvature(face):
    # 计算采样点的高斯曲率和平均曲率，用于变曲率曲面
    # get face uv bounds
    u_min, u_max, v_min, v_max = shapeanalysis_GetFaceUVBounds(face)

    # points = []
    # sas = ShapeAnalysis_Surface(face)
    point_num = 0
    g_cur_sum = 0
    m_cur_sum = 0
    u = u_min
    while u < u_max:
        v = v_min
        while v < v_max:
            # p = sas.Value(u, v)
            # print("u=", u, " v=", v, "->X=", p.X(), " Y=", p.Y(), " Z=", p.Z())
            # points.append(p)
            face1 = BRepAdaptor_Surface(face, True)
            sl_props = BRepLProp_SLProps(face1, u, v, 2, 0.001)
            gaussian = sl_props.GaussianCurvature()
            mean = sl_props.MeanCurvature()
            point_num += 1
            g_cur_sum = g_cur_sum + gaussian
            m_cur_sum = m_cur_sum + mean
            v += 0.1
        u += 0.1

    g_curvature = g_cur_sum / point_num
    m_curvature = m_cur_sum / point_num

    return g_curvature, m_curvature


def single_point_curvature(face):
    # 计算单个点的高斯曲率和平均曲率，用于恒曲率曲面
    # get face uv bounds
    u_min, u_max, v_min, v_max = shapeanalysis_GetFaceUVBounds(face)

    # points = []
    # sas = ShapeAnalysis_Surface(face)
    u = (u_min + u_max) / 2
    v = (v_min + v_max) / 2
    face1 = BRepAdaptor_Surface(face, True)
    sl_props = BRepLProp_SLProps(face1, u, v, 2, 0.001)
    gaussian = sl_props.GaussianCurvature()
    mean = sl_props.MeanCurvature()

    return gaussian, mean


def ask_centroid_normal(face):
    """Get centroid normal vector of B-Rep face."""
    mass_props = GProp_GProps()
    brepgprop.SurfaceProperties(face, mass_props)
    g_pt = mass_props.CentreOfMass()
    uv = ask_point_uv2(g_pt.Coord(), face)
    n = ask_point_normal_face(uv, face)

    return n


def recognise_face_type(face):
    # 识别面的种类，并根据种类返回高斯曲率和平均曲率，a：种类；b：高斯曲率；c：平均曲率
    # BRepAdaptor to get the face surface, GetType() to get the type of geometrical surface type
    surf = BRepAdaptor_Surface(face, True)
    surf_type = surf.GetType()
    a = 0
    b = 0
    c = 0
    if surf_type == GeomAbs_Plane:
        a = 1
        b = float(0)
        c = float(0)
    elif surf_type == GeomAbs_Cylinder:
        a = 2
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_Torus:
        a = 3
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_Sphere:
        a = 4
        b, c = single_point_curvature(face)
    elif surf_type == GeomAbs_Cone:
        a = 5
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_BezierSurface:
        a = 6
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_BSplineSurface:
        a = 7
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_SurfaceOfRevolution:
        a = 8
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_OffsetSurface:
        a = 9
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_SurfaceOfExtrusion:
        a = 10
        b, c = sample_point_curvature(face)
    elif surf_type == GeomAbs_OtherSurface:
        a = 11
        b, c = sample_point_curvature(face)

    return b, c, a,


def get_faces(topo, label_map):
    work_faces = {}
    faces = list(topo.faces())

    for face in faces:
        wf = WorkFace(len(work_faces), face)
        wf.surface_area = ask_surface_area(face)
        wf.normal = ask_centroid_normal(face)
        wf.curvature1, wf.curvature2, wf.face_type = recognise_face_type(face)
        wf.label = label_map[face]
        work_faces[wf.hash] = wf

    return work_faces, faces


def get_brep_information(shape, label_map):
    # 在B-rep上执行拓扑遍历，得到面和边
    topo = TopologyExplorer(shape)
    work_faces, faces = get_faces(topo, label_map)
    work_edges = get_edges(topo, faces)

    return work_faces, work_edges, faces
