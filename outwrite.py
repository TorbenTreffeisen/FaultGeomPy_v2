from ansys_trans import *
from functions import *


def writeout_ansys(thickness, fault_model, hint_lines, area_model, asel_fc, cm_fc, asel_innerfc, cm_innerfc, asel_dz1, asel_dz2, asel_dz3, asel_dz4, cm_dz1, cm_dz2, cm_dz3, cm_dz4,
                   lsel_hints1, lsel_hints2, cm_hints1, cm_hints2, sub_dz1_dz2, sub_dz2_dz3, sub_dz3_dz4, sub_dz_fc, asel_dz1_2, asel_dz2_2, asel_dz3_2, asel_dz4_2, cm_dz1_2, cm_dz2_2, cm_dz3_2, cm_dz4_2, sub_dz4_hints, sub_dz1_hints, sub_dz2_hints, sub_dz3_hints, sub_fc_lense, vsel_fclense1, vsel_fclense2,
                   vsel_fcvolu1, vsel_fcvolu2, cm_volu_fclense, cm_volu_fcvolu, vsel_ifc, cm_volu_ifc, vsel_dz_res1_1, vsel_dz_res1_2, vsel_dz_res2_1, vsel_dz_res2_2, vsel_dz_res3_1, vsel_dz_res3_2, cm_volu_dz_res1, cm_volu_dz_res2, cm_volu_dz_res3,
                              vsel_dz1_1, vsel_dz1_2, vsel_dz2_1, vsel_dz2_2, vsel_dz3_1, vsel_dz3_2, cm_volu_dz1, cm_volu_dz2, cm_volu_dz3, vsel_res, cm_volu_res, vsel_sur, cm_volu_sur):

    ## Writeout
    lz = [[]]
    allsel = [["allsel"]]
    vext = [["VEXT", "ALL", " ", " ", 0, 0, thickness]]
    outwrite = []

    # in Ansys commands
    outwrite = app_list(lz, outwrite)
    point = ansform_points(fault_model)
    outwrite = app_list(point, outwrite)

    outwrite = app_list(lz, outwrite)
    lines = ansform_line(hint_lines)
    outwrite = app_list(lines, outwrite)

    outwrite = app_list(lz, outwrite)
    area_dz = ansform_area(area_model)
    outwrite = app_list(area_dz, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_fc, outwrite)
    outwrite = app_list(cm_fc, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_innerfc, outwrite)
    outwrite = app_list(cm_innerfc, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz1, outwrite)
    outwrite = app_list(cm_dz1, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz2, outwrite)
    outwrite = app_list(cm_dz2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz3, outwrite)
    outwrite = app_list(cm_dz3, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz4, outwrite)
    outwrite = app_list(cm_dz4, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(lsel_hints1, outwrite)
    outwrite = app_list(cm_hints1, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(lsel_hints2, outwrite)
    outwrite = app_list(cm_hints2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz1_dz2, outwrite)
    outwrite = app_list(sub_dz2_dz3, outwrite)
    outwrite = app_list(sub_dz3_dz4, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz_fc, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz1_2, outwrite)
    outwrite = app_list(cm_dz1_2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz2_2, outwrite)
    outwrite = app_list(cm_dz2_2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz3_2, outwrite)
    outwrite = app_list(cm_dz3_2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(asel_dz4_2, outwrite)
    outwrite = app_list(cm_dz4_2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz4_hints, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz1_hints, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz2_hints, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_dz3_hints, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(sub_fc_lense, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vext, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_ifc, outwrite)
    outwrite = app_list(cm_volu_ifc, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_fclense1, outwrite)
    outwrite = app_list(vsel_fclense2, outwrite)
    outwrite = app_list(cm_volu_fclense, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_fcvolu1, outwrite)
    outwrite = app_list(vsel_fcvolu2, outwrite)
    outwrite = app_list(cm_volu_fcvolu, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz_res1_1, outwrite)
    outwrite = app_list(vsel_dz_res1_2, outwrite)
    outwrite = app_list(cm_volu_dz_res1, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz_res2_1, outwrite)
    outwrite = app_list(vsel_dz_res2_2, outwrite)
    outwrite = app_list(cm_volu_dz_res2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz_res3_1, outwrite)
    outwrite = app_list(vsel_dz_res3_2, outwrite)
    outwrite = app_list(cm_volu_dz_res3, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz1_1, outwrite)
    outwrite = app_list(vsel_dz1_2, outwrite)
    outwrite = app_list(cm_volu_dz1, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz2_1, outwrite)
    outwrite = app_list(vsel_dz2_2, outwrite)
    outwrite = app_list(cm_volu_dz2, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_dz3_1, outwrite)
    outwrite = app_list(vsel_dz3_2, outwrite)
    outwrite = app_list(cm_volu_dz3, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_res, outwrite)
    outwrite = app_list(cm_volu_res, outwrite)
    outwrite = app_list(allsel, outwrite)

    outwrite = app_list(lz, outwrite)
    outwrite = app_list(vsel_sur, outwrite)
    outwrite = app_list(cm_volu_sur, outwrite)
    outwrite = app_list(allsel, outwrite)

    return outwrite


def writeout_kp(fault_model):
    ## Writeout
    lz = [[]]
    outwrite = []

    # in Ansys commands
    outwrite = app_list(lz, outwrite)
    point = points_3d(fault_model)
    outwrite = app_list(point, outwrite)

    return outwrite