from qtpy import QtWidgets
from flt_geom_ui_v2.mainwindow import Ui_MainWindow
from matplotlib.pyplot import *

from ansys_trans import *
from functions import *
from outwrite import *

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # stacked windows
        self.ui.pb_innerlense.clicked.connect(lambda: self.ui.sw_innerlense.setCurrentIndex(1))
        self.ui.pb_numerical.clicked.connect(lambda: self.ui.sw_numerical.setCurrentIndex(1))

        # Push Bottums
        self.ui.pb_select.clicked.connect(self.create_geometry)

    def create_geometry(self):

        # Input values

        # Projectname
        project_name = str(self.ui.project_name.text())

        # Geometrical input values
        # fault
        fault_length = int(self.ui.fc_length.value())
        fault_width = self.ui.fc_width.value()
        fault_dip = self.ui.fc_dip.value()
        distance_bands = self.ui.fc_dist_bands.value()

        # numb_bands = int(self.ui.numb_bands.currentText())

        # Input for lense
        # outer lense
        lense_length = int(self.ui.fc_lense_length.value())
        lense_width = self.ui.fc_lense_width.value()

        dist_lense = int(self.ui.fc_lense_dist.value())

        # inner lense
        if self.ui.box_ilense.isChecked():
            inner_lense_length = self.ui.inlense_l.value()  # lense length
            inner_lense_width = self.ui.inlense_w.value()   # lense width
        else:
            inner_lense_length = (4*lense_length)/5    # lense length
            inner_lense_width = lense_width / 3         # lense width

        # damage zone
        dz_width = self.ui.dz_width.value()

        # Input for reservoir & model dimensions
        # upper reservoir
        res_up_left_top_h = self.ui.res_up_left_top.value()
        res_up_left_bottom_h = self.ui.res_up_left_bottom.value()
        res_up_right_top_h = self.ui.res_low_left_top.value()
        res_up_right_bottom_h = self.ui.res_low_left_bottom.value()

        # lower reservoir
        res_low_left_top_h = self.ui.res_up_right_top.value()
        res_low_left_bottom_h = self.ui.res_up_right_bottom.value()
        res_low_right_top_h = self.ui.res_low_right_top.value()
        res_low_right_bottom_h = self.ui.res_low_right_bottom.value()

        # model dimensions
        mx_extend = self.ui.mx_extend.value()
        my_extend = self.ui.my_extend.value()

        thickness = self.ui.m_thickness.value()

        # Numerical inputs on inner lense
        # numerical setup
        if self.ui.cbox_numsetup1.isChecked():
            circle_points = int(self.ui.circle_points1.value())
            dz_tip_points = int(self.ui.dz_tip_points1.value())
        else:
            circle_points = 8  # 8 is the max number recommended for Ansys (Area-command)
            dz_tip_points = 4  # 4 is the max number recommended for Ansys (Area-command)

        # Defining & Calculating constants
        origin = [0, 0]
        right_angle = 90  # right angle in degree

        opp_angle = right_angle - fault_dip  # third angle in fault triangle
        kp_lense = 2 * circle_points

        n_lenses = int((fault_length / (lense_length + dist_lense)) / 2)

        # lense (around midpoint)
        # Calculation of lense - triangle for length
        x_lense_length = cong_asa(0.5 * lense_length, opp_angle, right_angle)
        y_lense_length = cong_asa(0.5 * lense_length, fault_dip, right_angle)

        # Calculation of lense tips
        lense_tip2 = point_calculation(*origin, x1=-x_lense_length, y1=y_lense_length)
        lense_tip1 = point_calculation(*origin, x1=x_lense_length, y1=-y_lense_length)

        # Calculation of lense triangle for width
        x_lense_width = cong_asa(0.5 * lense_width, fault_dip, right_angle)
        y_lense_width = cong_asa(0.5 * lense_width, opp_angle, right_angle)

        # Calculation of lense width
        lense_width1 = point_calculation(*origin, x1=-x_lense_width, y1=-y_lense_width)
        lense_width2 = point_calculation(*origin, x1=x_lense_width, y1=y_lense_width)

        # lenticular shape (circle through lense points)
        c1_lense = circle_through_points(*lense_tip1, *lense_tip2, *lense_width1)
        c2_lense = circle_through_points(*lense_tip1, *lense_tip2, *lense_width2)

        # angle between lense tips
        ang_lense = angle_on_circle(c1_lense[2], lense_length)

        # angle for point calculation on circle
        ang_bet_lense = ang_lense / circle_points

        # calculate list with angles from lense tip to (standart) deviated points on circle
        li_ang_lense = []
        ang_li_lense = ang_xpoints(li_ang_lense, ang_bet_lense, circle_points)

        # coordinates of points on circle
        points_circle_lense1 = []
        points_lense1 = coord_circlepoints(points_circle_lense1, ang_li_lense, c1_lense[0], c1_lense[1], *lense_tip1)

        points_circle_lense2 = []
        points_lense2 = coord_circlepoints(points_circle_lense2, ang_li_lense, c2_lense[0], c2_lense[1], *lense_tip2)

        # Displacement to create a line at the lense tips (not only point contact!)
        # define each side of lense individually
        lense_point = [lense_tip1]
        lense_point = app_list(points_lense1, lense_point)
        lense_point.append(lense_tip2)
        lense_point = app_list(points_lense2, lense_point)

        len_lense_points = len(lense_point)

        # list of distance to midpoint
        list_distance = lense_points(lense_length + dist_lense, n_lenses)
        len_list_distance = len(list_distance)

        # direction vector to multiply the lenses
        m_vector1 = norm_vector(*direction_vector(*origin, *lense_tip2))
        m_vector2 = norm_vector(*direction_vector(*origin, *lense_tip1))

        up = []
        for j in range(0, len_list_distance):
            for i in range(0, len_lense_points):
                up.append(transform_vector(*lense_point[i], *m_vector1, list_distance[j]))

        # Calculating all downward lenses
        down = []
        for j in range(0, len_list_distance):
            for i in range(0, len_lense_points):
                down.append(transform_vector(*lense_point[i], *m_vector2, list_distance[j]))

        # Complete fault
        inner_fault_model = []
        inner_fault_model = app_list(lense_point, inner_fault_model)
        inner_fault_model = app_list(up, inner_fault_model)
        inner_fault_model = app_list(down, inner_fault_model)

        fault_model = app_list(up, lense_point)
        fault_model = app_list(down, lense_point)

        inner_fc_intems = len(fault_model)
        # print(inner_fc_intems, 'inner_fc_items')

        # multiple rows
        trans_tip2 = norm_vector(*direction_vector(*lense_tip2, *origin))

        # left additional row
        trans_left_width = norm_vector(*direction_vector(*origin, *lense_width1))

        left_widht = []
        for i in range(0, len(fault_model)):
            left_widht.append(transform_vector(*fault_model[i], *trans_left_width, distance_bands))

        left_fault = []
        for i in range(0, len(left_widht)):
            left_fault.append(transform_vector(*left_widht[i], *trans_tip2, 0.5 * (lense_length + dist_lense)))

        add_left_fault = left_fault[0:((len(left_fault)) - kp_lense)]

        left_fc_intems = len(add_left_fault)

        # right additional row
        trans_right_width = norm_vector(*direction_vector(*origin, *lense_width2))

        right_widht = []
        for i in range(0, len(fault_model)):
            right_widht.append(transform_vector(*fault_model[i], *trans_right_width, distance_bands))

        right_fault = []
        for i in range(0, len(right_widht)):
            right_fault.append(transform_vector(*right_widht[i], *trans_tip2, 0.5 * (lense_length + dist_lense)))

        add_right_fault = right_fault[0:(len(
            right_fault) - kp_lense)]  # circlepoints are 8 which need to be multiplied by 2 since there are two half-circles and added 2 for the additional point at the tip

        right_fc_intems = len(add_right_fault)

        fault_model = app_list(add_left_fault, fault_model)
        fault_model = app_list(add_right_fault, fault_model)

        complete_fc_items = len(fault_model)

        # ---------------------------------------------------------------------------------------
        # Calculation of inner lense triangle for length

        x_inner_lense_length = cong_asa(0.5 * inner_lense_length, opp_angle, right_angle)
        y_inner_lense_length = cong_asa(0.5 * inner_lense_length, fault_dip, right_angle)

        # Calculation of lense tips
        inner_lense_tip2 = point_calculation(*origin, x1=-x_inner_lense_length, y1=y_inner_lense_length)
        inner_lense_tip1 = point_calculation(*origin, x1=x_inner_lense_length, y1=-y_inner_lense_length)

        # Calculation of lense triangle for width
        x_inner_lense_width = cong_asa(0.5 * inner_lense_width, fault_dip, right_angle)
        y_inner_lense_width = cong_asa(0.5 * inner_lense_width, opp_angle, right_angle)

        # Calculation of lense width
        inner_lense_width1 = point_calculation(*origin, x1=-x_inner_lense_width, y1=-y_inner_lense_width)
        inner_lense_width2 = point_calculation(*origin, x1=x_inner_lense_width, y1=y_inner_lense_width)

        # lenticular shape (circle through lense points)
        c1_inner_lense = circle_through_points(*inner_lense_tip1, *inner_lense_tip2, *inner_lense_width1)
        c2_inner_lense = circle_through_points(*inner_lense_tip1, *inner_lense_tip2, *inner_lense_width2)

        # angle between lense tips
        ang_inner_lense = angle_on_circle(c1_inner_lense[2], inner_lense_length)

        # angle for point calculation on circle
        ang_bet_inner_lense = ang_inner_lense / circle_points

        # calculate list with angles from lense tip to (standart) deviated points on circle
        li_ang_inner_lense = []
        ang_li_inner_lense = ang_xpoints(li_ang_inner_lense, ang_bet_inner_lense, circle_points)

        # coordinates of points on circle
        points_circle_inner_lense1 = []
        points_inner_lense1 = coord_circlepoints(points_circle_inner_lense1, ang_li_inner_lense, c1_inner_lense[0],
                                                 c1_inner_lense[1], *inner_lense_tip1)

        points_circle_inner_lense2 = []
        points_inner_lense2 = coord_circlepoints(points_circle_inner_lense2, ang_li_inner_lense, c2_inner_lense[0],
                                                 c2_inner_lense[1], *inner_lense_tip2)

        # list of lense
        inner_lense_model = [inner_lense_tip1]
        inner_lense_model = app_list(points_inner_lense1, inner_lense_model)
        inner_lense_model.append(inner_lense_tip2)
        inner_lense_model = app_list(points_inner_lense2, inner_lense_model)

        len_inner_lense_model = len(inner_lense_model)

        inner_lense_up = []
        for j in range(0, len_list_distance):
            for i in range(0, len_inner_lense_model):
                inner_lense_up.append(transform_vector(*inner_lense_model[i], *m_vector1, list_distance[j]))

        inner_lense_down = []
        for j in range(0, len_list_distance):
            for i in range(0, len_inner_lense_model):
                inner_lense_down.append(transform_vector(*inner_lense_model[i], *m_vector2, list_distance[j]))

        inner_faultlense_model = []
        inner_faultlense_model = app_list(inner_lense_model, inner_faultlense_model)
        inner_faultlense_model = app_list(inner_lense_up, inner_faultlense_model)
        inner_faultlense_model = app_list(inner_lense_down, inner_faultlense_model)

        # left additional row
        inner_left_widht = []
        for i in range(0, len(inner_faultlense_model)):
            inner_left_widht.append(transform_vector(*inner_faultlense_model[i], *trans_left_width, distance_bands))

        inner_left_fault = []
        for i in range(0, len(inner_left_widht)):
            inner_left_fault.append(
                transform_vector(*inner_left_widht[i], *trans_tip2, 0.5 * (lense_length + dist_lense)))

        add_innerleft_fault = inner_left_fault[0:((len(inner_left_fault)) - kp_lense)]

        # right additional row
        inner_right_widht = []
        for i in range(0, len(inner_faultlense_model)):
            inner_right_widht.append(
                transform_vector(*inner_faultlense_model[i], *trans_right_width, distance_bands))

        inner_right_fault = []
        for i in range(0, len(inner_right_widht)):
            inner_right_fault.append(
                transform_vector(*inner_right_widht[i], *trans_tip2, 0.5 * (lense_length + dist_lense)))

        add_innerright_fault = inner_right_fault[0:(len(inner_right_fault) - kp_lense)]

        inner_faultlense_model = app_list(add_innerleft_fault, inner_faultlense_model)
        inner_faultlense_model = app_list(add_innerright_fault, inner_faultlense_model)

        fault_model = app_list(inner_faultlense_model, fault_model)

        complete_innerfc_items = len(fault_model)

        # -------------------------------------------------------------------------------------------------------------
        # Fault
        # Calculation of fault tips
        fault_tip_1 = up[-circle_points]
        fault_tip_2 = down[-2 * circle_points]

        real_fc_length = distance_points(*fault_tip_1, *fault_tip_2)

        # Calculation of fault triangle for length
        x_fault = cong_asa(0.5 * real_fc_length, opp_angle, right_angle)
        y_fault = cong_asa(0.5 * real_fc_length, fault_dip, right_angle)

        fault_tip1 = point_calculation(*origin, x1=x_fault, y1=-y_fault)
        fault_tip2 = point_calculation(*origin, x1=-x_fault, y1=y_fault)

        # damage zone
        # Calculation of damagezone triangle for width
        x_dz_width = cong_asa(0.5 * (dz_width * 2 + fault_width), fault_dip, right_angle)
        y_dz_width = cong_asa(0.5 * (dz_width * 2 + fault_width), opp_angle, right_angle)

        # Calculation of damage zone width
        dz_width1_1 = point_calculation(*fault_tip1, x1=-x_dz_width, y1=-y_dz_width)
        dz_width1_2 = point_calculation(*fault_tip1, x1=x_dz_width, y1=y_dz_width)

        dz_width2_1 = point_calculation(*fault_tip2, x1=-x_dz_width, y1=-y_dz_width)
        dz_width2_2 = point_calculation(*fault_tip2, x1=x_dz_width, y1=y_dz_width)

        # lenticular shape (circle through damage zonne points)
        c1_dz = [fault_tip1[0], fault_tip1[1], dz_width]
        c2_dz = [fault_tip2[0], fault_tip2[1], dz_width]

        # angle between damage zone tips
        ang_dz = angle_on_circle(c1_dz[2], 2 * dz_width)

        # angle for point calculation on circle
        ang_bet_dz = ang_dz / dz_tip_points

        # calculate list with angles from damage zone tip to (standart) deviated points on circle
        li_ang_dz = []
        ang_li_dz = ang_xpoints(li_ang_dz, ang_bet_dz, dz_tip_points)

        # coordinates of points on circle
        points_circle_dz1 = []
        points_dz1 = coord_circlepoints(points_circle_dz1, ang_li_dz, c1_dz[0], c1_dz[1], *dz_width1_2)

        points_circle_dz2 = []
        points_dz2 = coord_circlepoints(points_circle_dz2, ang_li_dz, c2_dz[0], c2_dz[1], *dz_width2_1)

        # model_geometry
        model_point1 = point_calculation(*origin, x1=-0.5 * mx_extend, y1=-0.5 * my_extend)
        model_point2 = point_calculation(*origin, x1=-0.5 * mx_extend, y1=dz_width1_2[1])
        model_point3 = point_calculation(*origin, x1=-0.5 * mx_extend, y1=dz_width2_1[1])
        model_point4 = point_calculation(*origin, x1=-0.5 * mx_extend, y1=0.5 * my_extend)
        model_point5 = point_calculation(*origin, x1=fault_tip2[0], y1=0.5 * my_extend)
        model_point6 = point_calculation(*origin, x1=dz_width2_2[0], y1=0.5 * my_extend)
        model_point7 = point_calculation(*origin, x1=0.5 * mx_extend, y1=0.5 * my_extend)
        model_point8 = point_calculation(*origin, x1=0.5 * mx_extend, y1=dz_width2_2[1])
        model_point9 = point_calculation(*origin, x1=0.5 * mx_extend, y1=dz_width1_1[1])
        model_point10 = point_calculation(*origin, x1=0.5 * mx_extend, y1=-0.5 * my_extend)
        model_point11 = point_calculation(*origin, x1=fault_tip1[0], y1=-0.5 * my_extend)
        model_point12 = point_calculation(*origin, x1=dz_width1_1[0], y1=-0.5 * my_extend)

        # Reservoir
        # intersects with model boundaries (not all in final model)
        res_up_left_top = point_calculation(*origin, x1=-0.5 * mx_extend, y1=res_up_left_top_h)
        res_up_left_bottom = point_calculation(*origin, x1=-0.5 * mx_extend, y1=res_up_left_bottom_h)
        res_up_right_top = point_calculation(*origin, x1=0.5 * mx_extend, y1=res_up_right_top_h)
        res_up_right_bottom = point_calculation(*origin, x1=0.5 * mx_extend, y1=res_up_right_bottom_h)

        res_low_left_top = point_calculation(*origin, x1=-0.5 * mx_extend, y1=res_low_left_top_h)
        res_low_left_bottom = point_calculation(*origin, x1=-0.5 * mx_extend, y1=res_low_left_bottom_h)
        res_low_right_top = point_calculation(*origin, x1=0.5 * mx_extend, y1=res_low_right_top_h)
        res_low_right_bottom = point_calculation(*origin, x1=0.5 * mx_extend, y1=res_low_right_bottom_h)

        # intersections with damagezone
        res_up_intersection_top = intersection_sline(*res_up_left_top, *res_up_right_top, *dz_width1_1,
                                                     *dz_width2_1)
        res_up_intersection_bottom = intersection_sline(*res_up_left_bottom, *res_up_right_bottom, *dz_width1_1,
                                                        *dz_width2_1)

        res_low_intersection_top = intersection_sline(*res_low_left_top, *res_low_right_top, *dz_width1_2,
                                                      *dz_width2_2)
        res_low_intersection_bottom = intersection_sline(*res_low_left_bottom, *res_low_right_bottom, *dz_width1_2,
                                                         *dz_width2_2)

        # Hint points for smear in
        # direction vector between top and bottom
        norm_res_smear1 = norm_vector(*direction_vector(*res_up_intersection_top, *res_low_intersection_top))
        norm_res_smear2 = norm_vector(*direction_vector(*res_up_intersection_bottom, *res_low_intersection_bottom))

        # hintpoints for smear in
        hint_smear_tle = transform_vector(*res_up_intersection_top, *norm_res_smear1, -100)
        hint_smear_tri = transform_vector(*res_low_intersection_top, *norm_res_smear1, 100)

        hint_smear_ble = transform_vector(*res_up_intersection_bottom, *norm_res_smear2, -100)
        hint_smear_bri = transform_vector(*res_low_intersection_bottom, *norm_res_smear2, 100)

        # Multiple DZ
        fault_core_width = fault_width / 2
        number_dz = 3

        # DZ top
        dz_up = []

        dz_up.append(dz_width1_2)
        dz_up = app_list(points_dz1, dz_up)
        dz_up.append(dz_width1_1)

        len_dz_up = len(dz_up)

        # DZ bottum

        dz_down = []
        dz_down.append(dz_width2_1)
        dz_down = app_list(points_dz2, dz_down)
        dz_down.append(dz_width2_2)

        len_dz_down = len(dz_down)

        # Calculations for multiple DZ

        # straightline between endpoint fc and dz

        norm_up = []
        for j in range(0, len_dz_up):
            norm_up.append(norm_vector(*direction_vector(*fault_tip1, *dz_up[j])))
        len_norm_up = len(norm_up)

        norm_bot = []
        for j in range(0, len_dz_down):
            norm_bot.append(norm_vector(*direction_vector(*fault_tip2, *dz_down[j])))
        len_norm_bot = len(norm_bot)

        # transform fcbc upper
        bcfc_uft = []
        for j in range(0, len_norm_up):
            bcfc_uft.append(transform_vector(*fault_tip1, *norm_up[j], fault_core_width))
        len_bcfc_uft = len(bcfc_uft)

        # transform fcbc lower
        bcfc_bft = []
        for j in range(0, len_norm_bot):
            bcfc_bft.append(transform_vector(*fault_tip2, *norm_bot[j], fault_core_width))
        len_bcfc_bft = len(bcfc_bft)

        # distance between end fc and end dz
        dist_upfcdz = []
        for i in range(0, len_bcfc_uft):
            dist_upfcdz.append(distance_points(*bcfc_uft[i], *dz_up[i]) / number_dz)

        dist_botfcdz = []
        for i in range(0, len_bcfc_bft):
            dist_botfcdz.append(distance_points(*bcfc_bft[i], *dz_down[i]) / number_dz)

        # rounded distances for all dz sections

        def dists_round_point(list_dist, number_points):
            output = []
            for i in range(1, number_points):
                output.append((round(list_dist * i, 2)))
            return output

        dist_top1 = dists_round_point(dist_upfcdz[0], number_dz)
        dist_top2 = dists_round_point(dist_upfcdz[1], number_dz)
        dist_top3 = dists_round_point(dist_upfcdz[2], number_dz)
        dist_top4 = dists_round_point(dist_upfcdz[3], number_dz)
        dist_top5 = dists_round_point(dist_upfcdz[4], number_dz)

        dist_bot1 = dists_round_point(dist_botfcdz[0], number_dz)
        dist_bot2 = dists_round_point(dist_botfcdz[1], number_dz)
        dist_bot3 = dists_round_point(dist_botfcdz[2], number_dz)
        dist_bot4 = dists_round_point(dist_botfcdz[3], number_dz)
        dist_bot5 = dists_round_point(dist_botfcdz[4], number_dz)

        # get points from distances

        points_top1 = []
        for j in range(0, len(dist_top1)):
            points_top1.append(transform_vector(*bcfc_uft[0], *norm_up[0], dist_top1[j]))

        points_top2 = []
        for j in range(0, len(dist_top2)):
            points_top2.append(transform_vector(*bcfc_uft[1], *norm_up[1], dist_top2[j]))

        points_top3 = []
        for j in range(0, len(dist_top3)):
            points_top3.append(transform_vector(*bcfc_uft[2], *norm_up[2], dist_top3[j]))

        points_top4 = []
        for j in range(0, len(dist_top4)):
            points_top4.append(transform_vector(*bcfc_uft[3], *norm_up[3], dist_top4[j]))

        points_top5 = []
        for j in range(0, len(dist_top5)):
            points_top5.append(transform_vector(*bcfc_uft[4], *norm_up[4], dist_top5[j]))

        points_bot1 = []
        for j in range(0, len(dist_bot1)):
            points_bot1.append(transform_vector(*bcfc_bft[0], *norm_bot[0], dist_bot1[j]))

        points_bot2 = []
        for j in range(0, len(dist_bot2)):
            points_bot2.append(transform_vector(*bcfc_bft[1], *norm_bot[1], dist_bot2[j]))

        points_bot3 = []
        for j in range(0, len(dist_bot3)):
            points_bot3.append(transform_vector(*bcfc_bft[2], *norm_bot[2], dist_bot3[j]))

        points_bot4 = []
        for j in range(0, len(dist_bot4)):
            points_bot4.append(transform_vector(*bcfc_bft[3], *norm_bot[3], dist_bot4[j]))

        points_bot5 = []
        for j in range(0, len(dist_bot5)):
            points_bot5.append(transform_vector(*bcfc_bft[4], *norm_bot[4], dist_bot5[j]))

        # Hier alle Punkte in Ansys-form bringen?

        points = [points_top1[0], points_top2[0], points_top3[0], points_top4[0], points_top5[0],
                  points_bot1[0], points_bot2[0], points_bot3[0], points_bot4[0], points_bot5[0],
                  points_top1[1], points_top2[1], points_top3[1], points_top4[1], points_top5[1],
                  points_bot1[1], points_bot2[1], points_bot3[1], points_bot4[1], points_bot5[1]]

        more_dz = app_list(bcfc_bft, bcfc_uft)
        more_dz = app_list(points, more_dz)

        len_more_dz = len(more_dz)

        # add to list fault_model
        faultcore_items = len(fault_model)

        fault_model.append(dz_width1_2)
        fault_model = app_list(points_dz1, fault_model)
        fault_model.append(dz_width1_1)

        dz_res_items_1 = len(fault_model)

        fault_model.append(res_up_intersection_bottom)
        fault_model.append(res_up_intersection_top)

        fault_model.append(dz_width2_1)
        fault_model = app_list(points_dz2, fault_model)
        fault_model.append(dz_width2_2)

        dz_res_items_2 = len(fault_model)

        fault_model.append(res_low_intersection_top)
        fault_model.append(res_low_intersection_bottom)

        fc_dz_items = len(fault_model)
        dz_items = fc_dz_items - faultcore_items

        res_up_int_b_index = dz_res_items_1 + 1
        res_up_int_t_index = dz_res_items_1 + 2

        res_low_int_b_index = dz_res_items_2 + 1
        res_low_int_t_index = dz_res_items_2 + 2

        # -----------------------------------------------------------------------------------
        # Fault-tip

        # fault core
        fc_upper_tip = inner_fault_model[int((0.5 * inner_fc_intems))]

        fc_lower_tip = inner_fault_model[int((inner_fc_intems) - (2 * circle_points))]

        # fault left
        fleft_upper_tip = add_left_fault[int((0.5 * left_fc_intems) + circle_points)]

        fleft_lower_tip = add_left_fault[int((left_fc_intems) - (2 * circle_points))]

        # fault right
        fright_upper_tip = add_right_fault[int((0.5 * right_fc_intems + circle_points))]

        fright_lower_tip = add_right_fault[int((right_fc_intems) - (2 * circle_points))]

        # Intersections fault_tips and model_boundaries

        hint_int_top_fmid = intersection_sline(*model_point4, *model_point7, *fc_upper_tip, *fc_lower_tip)
        hint_int_bottom_fmid = intersection_sline(*model_point1, *model_point10, *fc_upper_tip, *fc_lower_tip)

        hint_int_top_fleft = intersection_sline(*model_point4, *model_point7, *fleft_upper_tip, *fleft_lower_tip)
        hint_int_bottom_fleft = intersection_sline(*model_point1, *model_point10, *fleft_upper_tip,
                                                   *fleft_lower_tip)

        hint_int_top_fright = intersection_sline(*model_point4, *model_point7, *fright_upper_tip, *fright_lower_tip)
        hint_int_bottom_fright = intersection_sline(*model_point1, *model_point10, *fright_upper_tip,
                                                    *fright_lower_tip)

        hint_int = [hint_int_top_fmid, hint_int_bottom_fmid, hint_int_top_fleft, hint_int_bottom_fleft,
                    hint_int_top_fright, hint_int_bottom_fright]

        # ---------------------------------------------------------------------------------------------------------------------
        # Areas
        # FC

        kp_fc = list(range(1, complete_fc_items + 1))

        area_kp_fc = list(chunks(kp_fc, 2 * circle_points))

        # ---------------------------------------------------------------------------------------------------------------------
        # inner lense

        kp_inner_lense = list(range(complete_fc_items + 1, complete_innerfc_items + 1))

        area_kp_inner_lense = list(chunks(kp_inner_lense, 2 * circle_points))

        # -----------------------------------------------------------------------------------------------------------------
        # Areas
        # Damagezone - complete

        dz_area = [list(range(faultcore_items + 1, fc_dz_items + 1))]

        # -----------------------------------------------------------------------------------------------------------
        # lines for dividing the dz_area

        fault_model = app_list(hint_int, fault_model)
        fm_with_hints = len(fault_model)

        hint_lines_numbers = list(range(fm_with_hints - 5, fm_with_hints + 1))
        hint_lines = list(chunks(hint_lines_numbers, 2))

        # ----------------------------------------------------------------------------------------------------------
        # combine areas

        area_model = []
        area_model = app_list(area_kp_fc, area_model)

        faultcore_areas = len(area_model)

        area_model = app_list(area_kp_inner_lense, area_model)

        fc_innerlense_areas = len(area_model)

        area_model = app_list(dz_area, area_model)

        fc_dz_areas = len(area_model)

        # ------------------------------------------------------------------------------------------------------------
        # Surrounding rock

        # KP
        sur_areas = [model_point1, model_point2, res_up_left_bottom, res_up_left_top, model_point3, model_point4,
                     model_point5,
                     model_point6, model_point7, model_point8, res_low_right_top, res_low_right_bottom,
                     model_point9,
                     model_point10, model_point11, model_point12]

        fault_model = app_list(sur_areas, fault_model)

        fm_with_surareas = len(fault_model)

        # --------------------------------------------------------------------------------------------------------------
        # dz_areas_sections
        fault_model = app_list(more_dz, fault_model)
        fm_with_mDz = len(fault_model)

        # smear in points
        smear_points = [hint_smear_tle, hint_smear_tri, hint_smear_ble, hint_smear_bri]
        len_smear_points = len(smear_points)

        fault_model = app_list(smear_points, fault_model)
        fm_complete = len(fault_model)

        hint_lines_smear = list(range(fm_complete - 3, fm_complete + 1))
        hint_lines_smear = list(chunks(hint_lines_smear, 2))
        hint_lines = app_list(hint_lines_smear, hint_lines)

        dz_areas_add = list(range(fm_with_surareas + 1, fm_with_mDz + 1))
        dz_areas_add = list(chunks(dz_areas_add, 10))

        # Areas

        res_up = [fm_with_surareas - 13, fm_with_surareas - 12, dz_res_items_1 + 2, dz_res_items_1 + 1]
        res_down = [fm_with_surareas - 5, fm_with_surareas - 4, dz_res_items_2 + 2, dz_res_items_2 + 1]

        sur_1 = [fm_with_surareas - 15, fm_with_surareas - 14, dz_res_items_1, fm_with_surareas]
        sur_2 = [fm_with_surareas - 14, fm_with_surareas - 13, dz_res_items_1 + 1, dz_res_items_1]
        sur_3 = [fm_with_surareas - 12, fm_with_surareas - 11, dz_res_items_1 + 3, dz_res_items_1 + 2]

        sur_4 = list(range(dz_res_items_1 + 3, dz_res_items_1 + 3 + int((0.5 * dz_tip_points)) + 1))
        sur_4.reverse()

        sur_4.insert(0, fm_with_surareas - 11)
        sur_4.insert(1, fm_with_surareas - 10)
        sur_4.insert(2, fm_with_surareas - 9)

        sur_5 = list(range(dz_res_items_1 + 3 + int((0.5 * dz_tip_points)), dz_res_items_2 + 1))
        sur_5.reverse()

        sur_5.insert(0, fm_with_surareas - 9)
        sur_5.insert(1, fm_with_surareas - 8)

        sur_6 = [fm_with_surareas - 8, fm_with_surareas - 7, fm_with_surareas - 6, dz_res_items_2]
        sur_7 = [fm_with_surareas - 6, fm_with_surareas - 5, dz_res_items_2 + 1, dz_res_items_2]
        sur_8 = [fm_with_surareas - 4, fm_with_surareas - 3, faultcore_items + 1, dz_res_items_2 + 2]

        sur_9 = list(range(faultcore_items + 1, faultcore_items + int((0.5 * dz_tip_points)) + 2))
        sur_9.reverse()

        sur_9.insert(0, fm_with_surareas - 3)
        sur_9.insert(1, fm_with_surareas - 2)
        sur_9.insert(2, fm_with_surareas - 1)

        sur_10 = list(range(faultcore_items + int((0.5 * dz_tip_points)) + 1, dz_res_items_1 + 1))
        sur_10.reverse()

        sur_10.insert(0, fm_with_surareas - 1)
        sur_10.insert(1, fm_with_surareas)

        res_rock = [res_up, res_down]
        sur_rock = [sur_1, sur_2, sur_3, sur_4, sur_5, sur_6, sur_7, sur_8, sur_9, sur_10]

        area_model = app_list(res_rock, area_model)
        area_model = app_list(sur_rock, area_model)

        all_area_befor_bool = len(area_model)

        area_model = app_list(dz_areas_add, area_model)
        all_area_befor_bool2 = len(area_model)

        # ------------------------------------------------------------------------------------------------------------
        # Define Boolean Operations in Ansys

        asel_fc = [ansform_asel_st_end(1, faultcore_areas)]
        asel_innerfc = [ansform_asel_st_end(faultcore_areas + 1, fc_innerlense_areas)]
        asel_dz1 = [ansform_asel_st(fc_dz_areas)]
        asel_dz2 = [ansform_asel_st(all_area_befor_bool + 3)]
        asel_dz3 = [ansform_asel_st(all_area_befor_bool + 2)]
        asel_dz4 = [ansform_asel_st(all_area_befor_bool + 1)]

        lsel_hints1 = [ansform_lsel_st_end(1, 3)]
        lsel_hints2 = [ansform_lsel_st_end(4, 5)]

        asel_dz1_2 = [ansform_asel_st(all_area_befor_bool2 + 1)]
        asel_dz2_2 = [ansform_asel_st(fc_dz_areas)]
        asel_dz3_2 = [ansform_asel_st(all_area_befor_bool2)]
        asel_dz4_2 = [ansform_asel_st(all_area_befor_bool2 - 1)]

        cm_fc = [ansform_cm("faultcore_area", "A")]
        cm_innerfc = [ansform_cm("innerfc_area", "A")]
        cm_dz1 = [ansform_cm("dz_area1", "A")]
        cm_dz2 = [ansform_cm("dz_area2", "A")]
        cm_dz3 = [ansform_cm("dz_area3", "A")]
        cm_dz4 = [ansform_cm("dz_area4", "A")]
        cm_hints1 = [ansform_cm("hint_list1", "L")]
        cm_hints2 = [ansform_cm("hint_list2", "L")]

        sub_dz1_dz2 = [ansform_sub("AL", "dz_area1", "dz_area2")]
        sub_dz2_dz3 = [ansform_sub("AL", "dz_area2", "dz_area3")]
        sub_dz3_dz4 = [ansform_sub("AL", "dz_area3", "dz_area4")]

        sub_dz_fc = [ansform_sub("AL", "dz_area4", "faultcore_area")]

        cm_dz1_2 = [ansform_cm("dz_area1", "A")]
        cm_dz2_2 = [ansform_cm("dz_area2", "A")]
        cm_dz3_2 = [ansform_cm("dz_area3", "A")]
        cm_dz4_2 = [ansform_cm("dz_area4", "A")]

        sub_dz4_hints = [ansform_sub("AL", "dz_area4", "hint_list1")]
        sub_dz1_hints = [ansform_sub("AL", "dz_area1", "hint_list2")]
        sub_dz2_hints = [ansform_sub("AL", "dz_area2", "hint_list2")]
        sub_dz3_hints = [ansform_sub("AL", "dz_area3", "hint_list2")]

        sub_fc_lense = [ansform_sub("AL", "faultcore_area", "innerfc_area")]

        # ---------------------------------------------------------------------------------------------------------------
        # Define Volumes for meshing

        vsel_ifc = [ansform_vsel_st_end(1, faultcore_areas)]
        cm_volu_ifc = [ansform_cm("innerfc_lense", "V")]

        vsel_fclense1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas)]
        vsel_fclense2 = [
            ansform_vsel_add_st_end(all_area_befor_bool2 - faultcore_areas + 14, all_area_befor_bool2 + 12)]
        cm_volu_fclense = [ansform_cm("faultcore_lense", "V")]

        vsel_fcvolu1 = [ansform_vsel_st(all_area_befor_bool - faultcore_areas + 1)]
        vsel_fcvolu2 = [ansform_vsel_add_st_end(all_area_befor_bool2 - faultcore_areas + 2,
                                                all_area_befor_bool2 - faultcore_areas + 4)]
        cm_volu_fcvolu = [ansform_cm("faultcore_volu", "V")]

        vsel_dz_res1_1 = [ansform_vsel_st(faultcore_areas + 1)]
        vsel_dz_res1_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 11)]
        cm_volu_dz_res1 = [ansform_cm("dz_res_volu1", "V")]

        vsel_dz_res2_1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas + 1)]
        vsel_dz_res2_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 8)]
        cm_volu_dz_res2 = [ansform_cm("dz_res_volu2", "V")]

        vsel_dz_res3_1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas - 1)]
        vsel_dz_res3_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 5)]
        cm_volu_dz_res3 = [ansform_cm("dz_res_volu3", "V")]

        vsel_dz1_1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas + 12)]
        vsel_dz1_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 13)]
        cm_volu_dz1 = [ansform_cm("dz_volu1", "V")]

        vsel_dz2_1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas + 9)]
        vsel_dz2_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 10)]
        cm_volu_dz2 = [ansform_cm("dz_volu2", "V")]

        vsel_dz3_1 = [ansform_vsel_st(all_area_befor_bool2 - faultcore_areas + 6)]
        vsel_dz3_2 = [ansform_vsel_add_st(all_area_befor_bool2 - faultcore_areas + 7)]
        cm_volu_dz3 = [ansform_cm("dz_volu3", "V")]

        vsel_res = [ansform_vsel_st_end(faultcore_areas + 2, faultcore_areas + 3)]
        cm_volu_res = [ansform_cm("res_volu", "V")]

        vsel_sur = [ansform_vsel_st_end(faultcore_areas + 4, faultcore_areas + 13)]
        cm_volu_sur = [ansform_cm("sur_volu", "V")]

        ansys_out = 1

        if ansys_out == 1:
            outwrite = writeout_ansys(thickness, fault_model, hint_lines, area_model, asel_fc, cm_fc, asel_innerfc,
                                      cm_innerfc, asel_dz1, asel_dz2, asel_dz3, asel_dz4, cm_dz1, cm_dz2, cm_dz3,
                                      cm_dz4,
                                      lsel_hints1, lsel_hints2, cm_hints1, cm_hints2, sub_dz1_dz2, sub_dz2_dz3,
                                      sub_dz3_dz4, sub_dz_fc, asel_dz1_2, asel_dz2_2, asel_dz3_2, asel_dz4_2, cm_dz1_2,
                                      cm_dz2_2, cm_dz3_2, cm_dz4_2, sub_dz4_hints, sub_dz1_hints, sub_dz2_hints,
                                      sub_dz3_hints, sub_fc_lense, vsel_fclense1, vsel_fclense2,
                                      vsel_fcvolu1, vsel_fcvolu2, cm_volu_fclense, cm_volu_fcvolu, vsel_ifc,
                                      cm_volu_ifc, vsel_dz_res1_1, vsel_dz_res1_2, vsel_dz_res2_1, vsel_dz_res2_2,
                                      vsel_dz_res3_1, vsel_dz_res3_2, cm_volu_dz_res1, cm_volu_dz_res2, cm_volu_dz_res3,
                                      vsel_dz1_1, vsel_dz1_2, vsel_dz2_1, vsel_dz2_2, vsel_dz3_1, vsel_dz3_2,
                                      cm_volu_dz1, cm_volu_dz2, cm_volu_dz3, vsel_res, cm_volu_res, vsel_sur,
                                      cm_volu_sur)
        else:
            outwrite = writeout_kp(fault_model)

        write_row(project_name, outwrite)


window = MainWindow()

window.show()

sys.exit(app.exec_())