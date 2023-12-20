def validate_purchase_order_data(data):
    status_options = ['pending', 'completed', 'canceled']
    required_data = ['vendor_id', 'order_date', 'delivery_date', 'items', 'quantity', 'status',
                     'quality_rating', 'issue_date', 'acknowledgment_date']
    if data.get('status') not in status_options:
        raise ValueError('select valid status from {}'.format(status_options))
    missing_data = list()
    for require in required_data:
        if require not in data:
            missing_data.append(require)
    if len(missing_data):
        raise ValueError('{} {} required'.format(', '.join(missing_data), ('are', 'is')[len(missing_data) == 1]))
    return True
