def validate_vendor_data(data):

    required_data = ['name', 'phone', 'address', 'code']
    missing_data = list()
    for require in required_data:
        if require not in data:
            missing_data.append(require)
    if len(missing_data):
        raise ValueError('{} {} required'.format(', '.join(missing_data), ('are', 'is')[len(missing_data) == 1]))
    return True
