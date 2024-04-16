import h5py
import random
import numpy as np


EPSILON = 1e-6


def get_sparse_tensor(adj_matrix, default_value=0.):
    # 把稠密矩阵变成稀疏矩阵，即把邻接矩阵变成（面，面）对
    idx = np.where(np.not_equal(adj_matrix, default_value))
    values = adj_matrix[idx]
    shape = np.shape(adj_matrix)

    idx = np.transpose(idx).astype(np.int32)
    values = values.astype(np.float32)
    shape = np.array(shape).astype(np.int32)

    return idx, values, shape


def normalize_data(data):
    # 数据归一化，避免太大的数引发数值问题
    data_max = np.max(data, axis=0)
    data_min = np.min(data, axis=0)

    data_norm = (data - data_min) / (data_max - data_min + EPSILON)
    return data_norm


def zero_centered_data(data):
    # 中心化
    return (data - np.mean(data)) / np.std(data)


def normalize_surface_labels(data, num_surface_types=11):
    # 面类型归一化
    data_norm = data / (num_surface_types + EPSILON)
    return data_norm


def normalize_curve_labels(data, num_curve_types=9):
    # 边类型归一化
    data_norm = data / (num_curve_types + EPSILON)
    return data_norm


def normalize_edge_convexity(data, num_edge_convex=3):
    # 边凸度归一化
    data_norm = data / (num_edge_convex + EPSILON)
    return data_norm


def disjoint_adj_sparse(m1_idx, m1_values, m1_shape, m2_idx, m2_values, m2_shape):
    # 把稀疏矩阵变成稠密矩阵，即把（面，面）对变成邻接矩阵
    m3_shape = [m1_shape[0] + m2_shape[0], m1_shape[1] + m2_shape[1]]
    m3_values = np.concatenate((m1_values, m2_values))

    m2_idx[:, 0] = m2_idx[:, 0] + m1_shape[0]
    m2_idx[:, 1] = m2_idx[:, 1] + m1_shape[1]
    m3_idx = np.concatenate((m1_idx, m2_idx), axis=0)

    return m3_idx, m3_values, m3_shape


def extract_data_from_h5_group(h5_group, normalize=True):
    # 从h5文件的组中提取数据
    v_1 = np.array(h5_group.get("V_1"))
    surface_types = v_1[:, -1].reshape(-1, 1)
    v_1 = v_1[:, :-1]
    v_2 = np.array(h5_group.get("V_2"))
    curve_types = v_2[:, -1].reshape(-1, 1)
    edge_convexity = v_2[:, 0].reshape(-1, 1)
    curve_length = v_2[:, 2].reshape(-1, 1)
    labels = np.array(h5_group.get("labels"))

    if normalize:
        v_1 = normalize_data(v_1)
        curve_length = normalize_data(curve_length)
        surface_types = normalize_surface_labels(surface_types)
        curve_types = normalize_curve_labels(curve_types)
        edge_convexity = normalize_edge_convexity(edge_convexity)

    v_1 = np.concatenate((v_1, surface_types), axis=1)
    v_2 = np.concatenate((edge_convexity, curve_length, curve_types), axis=1)

    a_1_idx = np.array(h5_group.get("A_1_idx"))
    a_1_values = np.array(h5_group.get("A_1_values"))
    a_1_shape = np.array(h5_group.get("A_1_shape"))

    return v_1, v_2, a_1_idx, a_1_values, a_1_shape, labels


def generate_h5_batch_file(file_path, batch_path, vertices_per_batch=10000):
    """Generate hdf5 file for batches of subset of dataset.

    param file_path: Path of hdf5 file storing the hierarchical B-Rep graphs of subset.
    param batch_path: Path of hdf5 file for batches.
    param vertices_per_batch: Max number of vertices in batch for all hierarchical B-Rep graphs.
    return: None
    """
    hf = h5py.File(file_path, 'r')
    batch_counter = 0
    batch_num = 0
    vertex_count = 0

    v_1_batch = v_2_batch = unit_tensor_batch = names = labels_batch = None
    a_1_batch_idx = a_1_batch_values = a_1_batch_shape = None

    keys = list(hf.keys())
    random.shuffle(keys)

    # Loop over groups in h5 file
    for key in keys:
        group = hf.get(key)
        v_1, v_2, a_1_idx, a_1_values, a_1_shape, labels = extract_data_from_h5_group(group, normalize=True)

        vertex_count += v_1.shape[0]  # 这里有问题，回头记得改！

        # Check if adding the new graph will make the batch graph too. If so add the batch graph to the file.
        if vertex_count >= vertices_per_batch:
            print(f"Generated batch num {batch_num}")
            batch = [names, v_1_batch, v_2_batch, a_1_batch_idx, a_1_batch_values, a_1_batch_shape,
                     unit_tensor_batch, labels_batch]
            write_batch_to_file(batch_num, batch, batch_path)

            # Reset batch
            vertex_count = 0
            batch_counter = 0
            batch_num += 1
            v_1_batch = v_2_batch = unit_tensor_batch = names = labels_batch = None
            a_1_batch_idx = a_1_batch_values = a_1_batch_shape = None

        # If limit is not reached add new graph to batch.
        else:
            # If there is no graphs in current batch
            if batch_counter == 0:
                v_1_batch = v_1
                v_2_batch = v_2
                unit_tensor_batch = np.zeros(v_1.shape[0])
                names = np.array([[key]], dtype='S')
                labels_batch = labels

                a_1_batch_idx, a_1_batch_values, a_1_batch_shape = a_1_idx, a_1_values, a_1_shape

                batch_counter += 1

            # If there are graphs in current batch
            else:
                v_1_batch = np.append(v_1_batch, v_1, axis=0)
                v_2_batch = np.append(v_2_batch, v_2, axis=0)
                unit_tensor = np.full(v_1.shape[0], batch_counter)
                unit_tensor_batch = np.append(unit_tensor_batch, unit_tensor, axis=0)
                names = np.append(names, np.array([[key]], dtype='S'), axis=0)
                labels_batch = np.append(labels_batch, labels, axis=0)

                a_1_batch_idx, a_1_batch_values, a_1_batch_shape = \
                    disjoint_adj_sparse(a_1_batch_idx, a_1_batch_values, a_1_batch_shape,
                                        a_1_idx, a_1_values, a_1_shape)
                batch_counter += 1

    batch = [names, v_1_batch, v_2_batch, a_1_batch_idx, a_1_batch_values, a_1_batch_shape, unit_tensor_batch,
             labels_batch]
    write_batch_to_file(batch_num, batch, batch_path)

    hf.close()


def write_batch_to_file(batch_num, batch, file_path):
    """Writes batch graph to h5 file.

    param batch_num: Index of batch.
    param batch: List containing batch graph information.
    param file_path: File path of h5 file.
    return: None
    """
    hf = h5py.File(file_path, 'a')
    batch_group = hf.create_group(str(batch_num))

    if not batch:
        batch_group.create_dataset("names", 'str', data=batch[0], compression="gzip", compression_opts=9)
        batch_group.create_dataset("V_1", 'f', data=batch[1])
        batch_group.create_dataset("V_2", 'f', data=batch[2])
        batch_group.create_dataset("A_1_idx", 'f', data=batch[3])
        batch_group.create_dataset("A_1_values", 'f', data=batch[4])
        batch_group.create_dataset("A_1_shape", 'f', data=batch[5])
        batch_group.create_dataset("I_1", 'f', data=batch[6])
        batch_group.create_dataset("labels", 'f', data=batch[7])
    else:
        batch_group.create_dataset("names", data=batch[0], compression="gzip", compression_opts=9)
        batch_group.create_dataset("V_1", data=batch[1])
        batch_group.create_dataset("V_2", data=batch[2])
        batch_group.create_dataset("A_1_idx", data=batch[3])
        batch_group.create_dataset("A_1_values", data=batch[4])
        batch_group.create_dataset("A_1_shape", data=batch[5])
        batch_group.create_dataset("I_1", data=batch[6])
        batch_group.create_dataset("labels", data=batch[7])

    hf.close()


if __name__ == "__main__":

    read_file_path = "C:\\Users\\10564\\Desktop\\cad_model\\mix_train_inc.h5"
    batch_h5_path = "C:\\Users\\10564\\Desktop\\cad_model\\mix_train_inc_batch.h5"
    generate_h5_batch_file(read_file_path, batch_h5_path, vertices_per_batch=10000)
