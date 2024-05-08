def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    return data_str