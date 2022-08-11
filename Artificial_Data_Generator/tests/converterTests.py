import shapes
import converters.degree as deg_con


def degree_converter():
    degrees = list(range(0, 360))
    circle = shapes.Circle()

    for degree in degrees:
        print(degree)
        print(deg_con.degree_to_xy(degree, circle))


degree_converter()
