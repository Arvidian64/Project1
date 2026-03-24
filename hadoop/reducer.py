def run_reducer(mapped_data):
    """
    Expects a list of tuples: [(sensor, value), ...]
    The list MUST be sorted by sensor name first.
    """
    results = []
    current_sensor = None
    count = 0
    total = 0
    min_val = None
    max_val = None

    for sensor, value in mapped_data:
        # Core logic from original reducer
        if current_sensor == sensor:
            count += 1
            total += value
            min_val = min(min_val, value)
            max_val = max(max_val, value)
        else:
            if current_sensor is not None:
                results.append((current_sensor, min_val, max_val, total / count))

            current_sensor = sensor
            count = 1
            total = value
            min_val = value
            max_val = value

    if current_sensor is not None:
        results.append((current_sensor, min_val, max_val, total / count))

    return results

    
