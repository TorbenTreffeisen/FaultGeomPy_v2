import math
import csv



def point_calculation(x, y, x1=0, y1=0):
    p = [x + x1, y + y1]
    return p


def midpoint(p1x, p1y, p2x, p2y):
    mx = 0.5 * (p1x + p2x)
    my = 0.5 * (p1y + p2y)
    mid = [mx, my]

    return mid


def cong_asa(s, w1, w2):
    f = (s * math.sin(math.radians(w1))) / math.sin(math.radians(w2))
    return f


def circle_through_points(x1, y1, x2, y2, x3, y3):
    a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
    b = (x1 ** 2 + y1 ** 2) * (y3 - y2) + (x2 ** 2 + y2 ** 2) * (y1 - y3) + (x3 ** 2 + y3 ** 2) * (y2 - y1)
    c = (x1 ** 2 + y1 ** 2) * (x2 - x3) + (x2 ** 2 + y2 ** 2) * (x3 - x1) + (x3 ** 2 + y3 ** 2) * (x1 - x2)

    x_center = -b / (2 * a)
    y_center = -c / (2 * a)
    radius = math.sqrt(((x_center - x1) ** 2) + ((y_center - y1) ** 2))
    circle = [x_center, y_center, radius]
    return circle


def angle_on_circle(radius, distance):
    angle = math.acos((2 * radius**2 - distance**2)/(2 * radius ** 2))
    return angle


def ang_xpoints(li_ang, ang_bet, number):
    for i in range(1, number):
        li_ang.append(ang_bet * i)
    return li_ang


def points_on_circle(origin_x, origin_y, start_x, start_y, angle):
    xp = origin_x + math.cos(angle) * (start_x - origin_x) + math.sin(angle) * (start_y - origin_y)
    yp = origin_y - math.sin(angle) * (start_x - origin_x) + math.cos(angle) * (start_y - origin_y)
    point = [xp, yp]
    return point


def coord_circlepoints(points_circle, li_ang, mx, my, endp1, endp2):
    for j in li_ang:
        points_circle.append(points_on_circle(mx, my, endp1, endp2, j))
    return points_circle


def direction_vector(point_a_x, point_a_y, point_b_x, point_b_y):
    vector = [point_b_x - point_a_x, point_b_y - point_a_y]
    return vector


def norm_vector(x_vect, y_vect):
    magnitude = math.sqrt(x_vect**2 + y_vect**2)
    norm_x = (1/magnitude) * x_vect
    norm_y = (1/magnitude) * y_vect
    norm_vector = [norm_x, norm_y]

    return norm_vector


def transform_vector(x_old_point, y_old_point, x_dir_vector, y_dir_vector,  distance):
    x_new_point = x_old_point + distance * x_dir_vector
    y_new_point = y_old_point + distance * y_dir_vector
    new_point = [x_new_point, y_new_point]

    return new_point




def intersection_sline(g1_p1_x, g1_p1_y, g1_p2_x, g1_p2_y, g2_p1_x, g2_p1_y, g2_p2_x, g2_p2_y):
    xschnitt = (-g1_p1_x * g2_p1_x * g1_p2_y + g1_p1_x * g2_p2_x * g1_p2_y + g1_p2_x * g2_p1_x * g1_p1_y - g1_p2_x *
                g2_p2_x * g1_p1_y + g1_p2_x * g2_p2_x * g2_p1_y - g1_p1_x * g2_p2_x * g2_p1_y - g1_p2_x * g2_p1_x *
                g2_p2_y + g1_p1_x * g2_p1_x * g2_p2_y) / \
               (-g2_p1_x * g1_p2_y + g2_p2_x * g1_p2_y + g2_p1_x * g1_p1_y - g2_p2_x * g1_p1_y + g1_p2_x *
                g2_p1_y - g1_p1_x * g2_p1_y - g1_p2_x * g2_p2_y + g1_p1_x * g2_p2_y)
    yschnitt = ((g2_p2_y - g2_p1_y) / (g2_p2_x - g2_p1_x)) * (xschnitt - g2_p1_x) + g2_p1_y
    schnittpunkt = [xschnitt, yschnitt]
    return schnittpunkt


def app_list(list1, app_li):
    for j in list1:
        app_li.append(j)

    return app_li

def points_3d(pointlist):
    a = 0
    trans_points = []
    for li in pointlist:
        li.append(0)

    for i in pointlist:
        trans_points.append(i)

    return trans_points


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def lense_points(lenght_lense, number):
    list_lense = []
    for i in range(1, number):
        list_lense.append(lenght_lense * i)
    return list_lense


def insert_points_area(area_list, startlist, endlist, number, insert1, insert2):
    trans_area = []

    i = 0
    for li in area_list:
        li.insert(insert1, startlist[i])
        li.insert(insert2, endlist[i])
        i = i + 1

    for j in area_list:
        trans_area.append(j)

    return trans_area

#  CSV schreiben
def write_row(file_name, list):
    csv_filename = str(file_name + ".csv")

    with open(csv_filename, "w", newline='') as file_to_write:
        writer = csv.writer(file_to_write)
        writer.writerows(list)

    del list[:]

# new for moreDZ

def distance_points(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

