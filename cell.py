from config import *


class Cell(object):
    """
    docstring for Cell
    string or int : id
    list: inflow_list : adjacency matrix for inflow
    list: outflow_list : adjacenct list but reverse, will give how much handover this cell will take (might be a dict later)
    list: cat_list = category list belong cell i
    load: calculated from categories' total loads.
    list : cat_percentage [class Category]

    """

    def __init__(self, id, cat_list, pe_list):
        self.id = id
        self.cat_list = cat_list
        self.pe_list = pe_list
        self.load = PRB
        self.cell_radius = CELL_RADIUS
        self.cell_barring = 0
        self.load_list = []

    def calculate_load(self, pe_list_load):
        self.load += sum(pe_list_load)
        # print(self.load)
        # return sum(loads)

    def assign_flow_lists(self, inflow_list, outflow_list):
        self.inflow_list = inflow_list
        self.outflow_list = outflow_list

    def assign_handover_setting(self, handover_setting):
        self.handover_setting = handover_setting
        self.modify_cats_handover(handover_setting)

    def modify_cats_handover(self, handover_setting):
        for cat in self.cat_list:
            cat.assign_handover_setting(handover_setting)

    def update_load(self, load):
        # load = [x.load for x in self.cat_list]
        # print(load)
        # print('hi')
        self.load = load

    # def decrease_load_list(self, pe_id, load):
    #     self.load_list.append(load)
    #     # print(pe_id)
    #     self.pe_list.remove(pe_id)
    #
    # def decrease_load(self):
    #     self.load -= sum(self.load_list)
    #
    # def increase_load_list(self, pe_id, load):
    #     self.load_list.append(load)
    #     self.pe_list.append(pe_id)
    #
    # def increase_load(self):
    #     self.load += sum(self.load_list)

    def update_barring(self, cell_barring):
        # load = [x.load for x in self.cat_list]
        # print(load)
        # print('hi')
        self.cell_barring = cell_barring

    def update_radius(self):
        cell_radius = self.cell_radius
        if self.load > BARRING_THRE and self.cell_radius > MIN_CELL_RADIUS:
            cell_radius -= BARRING_DISTANCE
        elif self.load <= BARRING_THRE and MIN_CELL_RADIUS <= self.cell_radius < CELL_RADIUS:
            cell_radius += BARRING_DISTANCE
        self.cell_radius = cell_radius
        return cell_radius
