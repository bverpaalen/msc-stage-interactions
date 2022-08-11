import shapes
from circle_point_selection import edge_point_selection as eps
from circle_point_selection import inner_point_selection as ips
from converters import coordinates, degree
import simulator
import matplotlib.pyplot as plt
import os

# 52.173701, 4.462163
# 52.174073, 4.463023
# 937

# https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
# 111.32 km = 1 degree lat
# 40075 km * cos(lat) / 360 = 1 degree long
# 40075 km * cos(4.46) / 360 = 27.57 km

n_trips = 1000

path = "./fake_experiments_v2/"

# 100 m
#lat_in_meter = round(1.0 / (150 / 0.1), 6)
lat_in_meter = 0.00092163008

# 100 m
#long_in_meter = round(1.0 / (120 / 0.1), 6)
long_in_meter = 0.00146985054


def main(start_lat=0, start_long=0, width=1, n_trips=100):
    source = (52.173701, 4.462163)
    x_to_lat = lat_in_meter * 0.1
    y_to_long = long_in_meter * 0.1

    circle = shapes.Circle(start_lat, start_long, width)
    for i in range(n_trips):
        create_trip(circle, i, source, x_to_lat, y_to_long)


def create_trip(circle, experiment_id, source_coordinates, x_to_lat, y_to_long):
    points = eps.x_potential_points(circle.degrees, 25)

    cor_points = []
    for point in points:
        cor_point = degree.degree_to_xy(point, circle)
        cor_points.append(cor_point)
    changing_point = ips.best_n_point_selection(circle, cor_points[0], cor_points[1])
    walks = simulator.simulate_walks(cor_points[0], cor_points[1], changing_point, 29)

    index = 0
    for walk in walks:
        trip = coordinates.list_of_x_y_to_coordinates(walk, source_coordinates, x_to_lat, y_to_long)
        write_trip(trip, experiment_id, False, index, path)
        index += 1

    simulator.simulate_meeting(walks, 5)

    index = 0
    for walk in walks:
        trip = coordinates.list_of_x_y_to_coordinates(walk, source_coordinates, x_to_lat, y_to_long)
        write_trip(trip,experiment_id, True, index, path)
        #xs = []
        #ys = []

        #for item in walk:
        #    xs.append(item[0])
        #    ys.append(item[1])
        index += 1
        #plt.plot(xs, ys)
    #plt.show()


def write_trip(trip, id, will_meet, index, path):
    header = "Date, Time, Latitude, Longitude, Altitude, Speed, Course, Type, Distance, Essential\n"
    data = "2020/1/1"
    time = 0

    if will_meet:
        meet = "True"
    else:
        meet = "False"

    if not os.path.exists(path):
        os.mkdir(path)

    f = open(path + "trip_" + meet + "_" + str(id) + "_" + str(index) + ".csv","w+")
    f.write(header)
    for data_point in trip:
        lat = str(data_point[0])
        long= str(data_point[1])

        line = data + "," + "00:00:"+str(time) + "," + lat + "," + long +",0,-1,0,fake,-1,1\n"

        f.write(line)
        time += 1
    f.close()


main(0, 0, 1, n_trips=n_trips)
# main(52.173701,4.462163,0.000937)
