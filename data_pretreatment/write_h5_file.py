import h5py
import numpy as np
from collections import Counter


def get_sparse_tensor(adj_matrix, default_value=0.):
    idx = np.where(np.not_equal(adj_matrix, default_value))
    values = adj_matrix[idx]
    shape = np.shape(adj_matrix)

    idx = np.transpose(idx).astype(np.int32)
    values = values.astype(np.float32)
    shape = np.array(shape).astype(np.int32)

    return idx, values, shape


def get_face_features(faces):
    faces_list = []
    label_list = []

    for face_tag, face in faces.items():
        face_list = [face.surface_area, face.normal[0], face.normal[1], face.normal[2],
                     face.curvature1, face.curvature2, face.face_type]
        faces_list.append(face_list)
        label_list.append(face.label)

    return np.array(faces_list, dtype=np.float), np.array(label_list, dtype=np.float)


def adj_and_edge_features(edges, faces):
    brep_adj = np.zeros((len(faces), len(faces)))
    edges_list = []

    for edge in edges.values():
        a = edge.face_tags[0]
        b = edge.face_tags[1]
        edge_list = [edge.convexity, edge.curve_length, edge.edge_type, a, b]
        edges_list.append(edge_list)

        brep_adj[a, b] = 1
        brep_adj[b, a] = 1

    return np.array(edges_list, dtype=np.float), brep_adj


def edge_feature_treatment(edge_vector, adj_pair):
    vector = [[]] * adj_pair.shape[0]

    for index, j in enumerate(adj_pair):
        y = Counter([j[0], j[1]])
        for i in edge_vector:
            x = Counter([int(i[3]), int(i[4])])
            if dict(x) == dict(y):
                i = list(i)
                vector[index] = i
            else:
                pass

    a = np.array(vector, dtype=float)
    edge_feature_vector = np.array([a[:, 0], a[:, 1], a[:, 2]]).T

    return edge_feature_vector


def write_h5_file(h5_path, graph_name, work_faces, work_face_edges, save_sparse=True):
    hf = h5py.File(h5_path, 'a')
    group = hf.create_group(str(graph_name))

    v_1, labels = get_face_features(work_faces)
    e_v, a_1 = adj_and_edge_features(work_face_edges, work_faces)
    edge_pair, _, _ = get_sparse_tensor(a_1)
    v_2 = edge_feature_treatment(e_v, edge_pair)

    group.create_dataset("V_1", data=v_1, compression="lzf")
    group.create_dataset("V_2", data=v_2, compression="lzf")
    group.create_dataset("labels", data=labels, compression="lzf")

    if not save_sparse:
        group.create_dataset("A_1", data=a_1, compression="lzf")

    else:
        a_1_idx, a_1_values, a_1_shape = get_sparse_tensor(a_1)

        group.create_dataset("A_1_idx", data=a_1_idx, compression="lzf")
        group.create_dataset("A_1_values", data=a_1_values, compression="lzf")
        group.create_dataset("A_1_shape", data=a_1_shape, compression="lzf")

    #print(a_1_idx)
    #print(np.around(v_1, decimals=1))
    #print(np.around(v_2, decimals=1))
    #print(labels)
    hf.close()
