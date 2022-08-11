def list_of_x_y_to_coordinates(array, coordinates_source, x_to_lat, y_to_long):
    new_array = []
    for item in array:
        new_item = x_y_to_coordinates(item, coordinates_source, x_to_lat, y_to_long)
        new_array.append(new_item)
    return new_array


def x_y_to_coordinates(point, coordinates_source, x_to_lat, y_to_long):
    x = point[0]
    y = point[1]

    lat_diff = x_to_lat * float(x)
    long_diff = y_to_long * float(y)

    lat = coordinates_source[0] + lat_diff
    long = coordinates_source[1] + long_diff
    return lat, long
