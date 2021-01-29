
def ansform_points(pointlist):
    a = 0
    trans_points = []
    for li in pointlist:
        a = a + 1
        li.insert(0, "K")
        li.insert(1, a)

    for i in pointlist:
        trans_points.append(i)

    return trans_points


def ansform_line(line_list):
    trans_line = []
    for li in line_list:
        li.insert(0, "L")

    for i in line_list:
        trans_line.append(i)

    return trans_line


def ansform_lsel_st(start):

    lsel = []
    lsel.insert(0, "LSEL")
    lsel.insert(1, "S")
    lsel.insert(2, "LINE")
    lsel.insert(3, " ")
    lsel.insert(4, start)

    return lsel


def ansform_lsel_st_end(start, end):

    lsel = []
    lsel.insert(0, "LSEL")
    lsel.insert(1, "S")
    lsel.insert(2, "LINE")
    lsel.insert(3, " ")
    lsel.insert(4, start)
    lsel.insert(5, end)

    return lsel


def ansform_area(area_list):
    trans_area = []
    for li in area_list:
        li.insert(0, "A")

    for i in area_list:
        trans_area.append(i)

    return trans_area


def ansform_asel_st(start):

    asel = []
    asel.insert(0, "ASEL")
    asel.insert(1, "S")
    asel.insert(2, "AREA")
    asel.insert(3, " ")
    asel.insert(4, start)

    return asel


def ansform_asel_st_end(start, end):

    asel = []
    asel.insert(0, "ASEL")
    asel.insert(1, "S")
    asel.insert(2, "AREA")
    asel.insert(3, " ")
    asel.insert(4, start)
    asel.insert(5, end)

    return asel


def ansform_vsel_st(start):

    vsel = []
    vsel.insert(0, "VSEL")
    vsel.insert(1, "S")
    vsel.insert(2, "VOLU")
    vsel.insert(3, " ")
    vsel.insert(4, start)

    return vsel

def ansform_vsel_add_st(start):

    vsel = []
    vsel.insert(0, "VSEL")
    vsel.insert(1, "A")
    vsel.insert(2, "VOLU")
    vsel.insert(3, " ")
    vsel.insert(4, start)

    return vsel


def ansform_vsel_st_end(start, end):

    vsel = []
    vsel.insert(0, "VSEL")
    vsel.insert(1, "S")
    vsel.insert(2, "VOLU")
    vsel.insert(3, " ")
    vsel.insert(4, start)
    vsel.insert(5, end)

    return vsel


def ansform_vsel_add_st_end(start, end):

    vsel = []
    vsel.insert(0, "VSEL")
    vsel.insert(1, "A")
    vsel.insert(2, "VOLU")
    vsel.insert(3, " ")
    vsel.insert(4, start)
    vsel.insert(5, end)

    return vsel


def ansform_cm(name, key):

    cm = []
    cm.insert(0, "CM")
    cm.insert(1, name)

    if key == "A":
        cm.insert(2, "AREA")
    elif key == "L":
        cm.insert(2, "LINE")
    elif key == "V":
        cm.insert(2, "VOLU")
    else:
        pass

    return cm


def ansform_sub(key, cm_1, cm_2):

    sub = []
    if key == "AA":
        sub.insert(0, "ASBA")
    elif key == "AL":
        sub.insert(0, "ASBL")
    else:
        pass

    sub.insert(1, cm_1)
    sub.insert(2, cm_2)
    sub.insert(3, " ")
    sub.insert(4, "DELETE")
    sub.insert(5, "KEEP")

    return sub