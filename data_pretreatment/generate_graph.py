from OCC.Extend.DataExchange import STEPControl_Reader
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.StepRepr import StepRepr_RepresentationItem
from get_information import get_brep_information
from write_h5_file import write_h5_file


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

    id_map = {}
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
            id_map[face] = name_id

    return shape, topo, id_map


def create_graphs(h5_path, step_path, shape_name):
    try:
        shape, topo, label_map = read_step_with_labels(step_path)
        failure_test = check_face_in_map(topo, label_map)

        if failure_test:
            print("Issue with face map")
        else:
            work_faces, work_edges, faces = get_brep_information(shape, label_map)
            write_h5_file(h5_path, shape_name, work_faces, work_edges)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    import glob
    import os

    h5_file = "C:\\Users\\10564\\Desktop\\cad_model\\mix_train_inc.h5"
    step_files = glob.glob("D:\\Users Files\\Data\\mixed_train\\*.step")  # 两个路径需要改
    for i, step_file in enumerate(step_files):
        if i % 500 == 0:
            print(f"Count: {i}")
        step_id = os.path.basename(step_file)[:-len(".step")]
        create_graphs(h5_file, step_file, step_id)
