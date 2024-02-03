def validate_and_get_file(data):
    if 'file' not in data.files:
        raise ValueError("No file part")
    file = data.files['file']
    if file.filename == '':
        raise ValueError("No selected file")
    return file


def write_to_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)
