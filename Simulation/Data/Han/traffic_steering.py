from config import *


def traffic_steering(cells, pes):
    removed_pes = []
    for cell in cells:
        if cell.cell_barring_flag == 1:
            for cat in cell.cat_list:
                for pe in cat.pe_list:
                    distance = (pow(cell.coordinate_x - pe.x_coordinate, 2) + pow(cell.coordinate_y - pe.y_coordinate,
                                                                                  2))

                    if pe.load > 1 and distance > pow(cell.radius / 30, 2):
                        cat.pe_list.remove(pe)
                        for cell_j_id in OUTFLOW_SETTING[cell.id]:
                            distance = (pow(cells[cell_j_id].coordinate_x - pe.x_coordinate, 2) + pow(
                                cells[cell_j_id].coordinate_y - pe.y_coordinate, 2))
                            #if cells[cell_j_id].cell_barring_flag == 0 and distance <= pow(cells[cell_j_id].radius / 30, 2):
                            if distance <= pow(cells[cell_j_id].radius / 30, 2):
                                cells[cell_j_id].cat_list[0].pe_list.append(pe)
                                pe.assign_cell(cells[cell_j_id].id)
                                break
                            else:
                                pe.assign_cell(99)
                                for ue in pes:
                                    if ue.pe_id == pe.pe_id:
                                        ue.assign_cell(99)

        # if cell.cell_barring_flag == 1:

        #    distance = {}
        #    remove_pe_list = []
        #    handover_num = int(cell.load - 45)
        #    for i in range(len(pes_x_coordinates[cell.id])):
        #        x = pes_x_coordinates[cell.id][i]
        #        y = pes_y_coordinates[cell.id][i]
        #        distance.update({i: (pow(cells_x_coordinates[cell.id] - x, 2) + pow(cells_y_coordinates[cell.id] - y, 2))})

        #    j = 1
        #    if j <= handover_num:
        #        max_key = max(distance, key=lambda x: distance[x])
        #        remove_pe_list.append(max_key)
        #        distance.pop(max_key)

        #    for k in range(len(remove_pe_list)):
        #        pe_id = remove_pe_list[k]
        #        for cell_id in OUTFLOW_SETTING[cell.id]:
        #            if (pow(pes_x_coordinates[cell.id][pe_id],cells_x_coordinates[cell_id])
        #                    + pow(pes_y_coordinates[cell.id][pe_id],cells_y_coordinates[cell_id])) <= (CELL_RADIUS/30)*(CELL_RADIUS/30):
        #                pes_x_coordinates[cell_id].append(pes_x_coordinates[cell.id][pe_id])
        #                pes_y_coordinates[cell_id].append(pes_y_coordinates[cell.id][pe_id])
        #                pes_x_coordinates[cell.id].pop(pe_id)
        #                pes_y_coordinates[cell_id].pop(pe_id)
        #                break

        # cell.radius = cell.radius + 20
    return cells, pes
