import numpy as np

def convert_to_obj(input_filename, output_filename):
    data_raw = np.loadtxt(input_filename)

    points = data_raw[:, 2:5]  # columns 2, 3, 4 are X, Y, Z
    connection = data_raw[:, 6].astype(int)  # parent IDs, converted to int

    #create a mapping from swc ID to vertex index
    id_to_index = {int(data_raw[i, 0]): i + 1 for i in range(len(data_raw))}  # +1 for 1-based index in OBJ

    with open(output_filename, 'w') as f:
        for point in points:
            txt_str = 'v ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
            f.write(txt_str)


        for index, parent_id in enumerate(connection):
            if parent_id == -1 or parent_id == 0:
                continue
            if parent_id in id_to_index:
                parent_index = id_to_index[parent_id]
                txt_str = f'l {index + 1} {parent_index}\n'
                f.write(txt_str)

    asdf = 1
