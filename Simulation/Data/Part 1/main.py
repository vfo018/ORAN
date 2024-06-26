from config import *
from personal_equipment import PersonalEquipment
from category import Category
from cell import Cell
from utils import *
import pandas as pd
import pprint
import time


def main():
    start_time = time.time()

    inflow_setting = create_inflow_setting(OUTFLOW_SETTING)

    print("Scenario will be created")

    cells = create_scenerio(inflow_setting, OUTFLOW_SETTING)

    print("Scenario created, simulation will start")

    # time iteration and creating the data frame
    df = simulation(cells)

    print("Simulation ended, data will be exported")
    try:
        df.to_csv('output_handover_scenario_test1.csv', index=False)
        print("Data export completed")
        print("--- %s seconds ---" % (time.time() - start_time))
    except AttributeError:
        print('Error')


def simulation(cells):
    multiplier = 1

    data = {
        't': [],
        'cell_id': [],
        'cat_id': [],
        'pe_id': [],
        'pe_number': [],
        'power': [],
        'load': [],
        'cell_load': [],
        'has_anomaly': [],
        'cell_barring': [],
        'traffic_steering': [],
        'cell_distance': [],
        'cell_radius': []
    }

    mod = 30
    mod_step = int(mod * 0.08)
    mod_smooth_period = 5
    mod_smooth_counter = 0
    num_anomaly = int(SIM_TIME * ANOMALY_PERCENTAGE)
    anomaly_steps = sorted(sample_with_minimum_distance(n=SIM_TIME - mod, k=num_anomaly, d=mod + 1))
    anomaly_step_ends = [x + mod for x in anomaly_steps]
    anomaly_idx = 0

    for t in range(SIM_TIME):
        # Add random anomalities to data based on anomaly_idx
        has_anomaly = 0
        if anomaly_idx < num_anomaly:
            if t >= anomaly_steps[anomaly_idx] and t <= anomaly_step_ends[anomaly_idx]:
                has_anomaly = 1
                # if mod_smooth_counter == 0:
                #     multiplier = 1.002
                # if mod_smooth_counter == mod_step * 1:  # 1 - 2
                #     multiplier = 1.004
                # if mod_smooth_counter == mod_step * 2:  # 3 - 4
                #     multiplier = 1.008
                # if mod_smooth_counter == mod_step * 3:  # 4 - 7
                #     multiplier = 1.016
                # if mod_smooth_counter == mod_step * 4:  # 6 - 9
                #     multiplier = 1.032
                # if mod_smooth_counter == mod_step * 5:  # 8 - 12
                #     multiplier = 1.064
                # if mod_smooth_counter == (mod - (mod_step * 5)):
                #     multiplier = 1.032
                # if mod_smooth_counter == (mod - (mod_step * 4)):
                #     multiplier = 1.016
                # if mod_smooth_counter == (mod - (mod_step * 3)):
                #     multiplier = 1.008
                # if mod_smooth_counter == (mod - (mod_step * 2)):
                #     multiplier = 1.004
                # if mod_smooth_counter == (mod - (mod_step * 1)):
                #     multiplier = 1.002
                # if mod_smooth_counter == mod:
                #     multiplier = 1
                # mod_smooth_counter += 1

                if t == anomaly_step_ends[anomaly_idx]:
                    anomaly_idx += 1
                    # mod_smooth_counter = 0

        # Determine handover rates
        cat_new_load, cell_new_load = 0, 0

        # now we need to assign handovers to other cells and categories.
        if t == 0:
            pe_list = []
            dic_cell_load = {i: [] for i in range(CELL_NUMBER)}
            for cell in cells:
                for cat in cell.cat_list:
                    for pe in cat.pe_list:
                        cell_new_load += pe.load * multiplier
                        pe_list.append(pe)
                cell.update_load(cell_new_load)
                dic_cell_load[cell.id] = cell.load
                # print(cell.id, cell.load)
                cell_new_load = 0
            for pe in pe_list:
                data['cell_load'].append(dic_cell_load[pe.cell_id])
            # print(data['cell_load'])


        traffic_steering, cell_barring = 0, 0

        # now loads are balanced, write information to dictionary so that we can convert it to pandas and csv
        # cell_id to pe_id dictionary
        dic = {i: [] for i in range(CELL_NUMBER)}
        dic_cell_load = {i: [] for i in range(CELL_NUMBER)}
        dic_cell_radius = {i: [] for i in range(CELL_NUMBER)}

        pe_list, pe_old_cell_id = [], []
        for cell in cells:
            pe_list_load = []

            # for cat1 in cell.cat_list:
            #     for pe1 in cat1.pe_list:
            #         cell_new_load += pe1.load * multiplier
            #         # print(pe1.pe_id)
            # cell.update_load(cell_new_load)
            # if cell.id == 1:
            #     print(cell.pe_list)
            # print(len(cell.pe_list))
            # print(cell.load)
            # cell_new_load = 0
            # print(len(cell.pe_list))
            # cell.calculate_load()
            # cell.increase_load()
            # cell.decrease_load()
            if t > 0:
                cell_radius = cell.update_radius()
                # dic_cell_radius[cell.id] = cell_radius
            else:
                cell_radius = CELL_RADIUS
                dic_cell_radius[cell.id] = cell_radius
            if cell.load > PRB and cell.cell_radius == MIN_CELL_RADIUS:
                cell_barring = 1
                cell.update_barring(cell_barring)
            else:
                cell_barring = 0
                cell.update_barring(cell_barring)
            # if cell.load > PRB and cell.cell_radius > MIN_CELL_RADIUS:
            #     cell_barring = 1
            #     cell.update_barring(cell_barring)
            #     # data['cell_barring'].append(cell.cell_barring)
            # else:
            #     cell_barring = 0
            #     cell.update_barring(cell_barring)
                # data['cell_barring'].append(cell.cell_barring)

            for cat in cell.cat_list:
                for pe in cat.pe_list:
                    data['t'].append(t)
                    data['cell_id'].append(pe.cell_id)
                    data['cat_id'].append(cat.cat_id)
                    data['pe_id'].append(pe.pe_id)
                    data['pe_number'].append(pe.pe_id % PE_NUMBER)
                    data['power'].append(pe.power)
                    pe.set_load(pe.load * multiplier)
                    data['load'].append(pe.load)
                    # data['cell_load'].append(cell.load)
                    # if t == 0:
                    #     data['cell_load'].append(cell.load)
                        # print(data['cell_load'])
                    # data['cell_load'].append(dic_cell_load.get(pe.cell_id))
                    # data['cell_load'].append(pe.cell_id.load)
                    data['has_anomaly'].append(has_anomaly)
                    data['cell_barring'].append(cell.cell_barring)
                    data['cell_distance'].append(pe.update_distance())
                    data['cell_radius'].append(dic_cell_radius[pe.cell_id])
                    # print(data['cell_load'])
                    pe_list.append(pe)
                    pe_old_cell_id.append(pe.cell_id)
                    dic[pe.cell_id].append(pe.load)
                    if has_anomaly == 1 or (pe.cell_dist > cell_radius and cell.load > BARRING_THRE):
                        traffic_steering = 1
                        pe.update_steering(traffic_steering)
                        data['traffic_steering'].append(pe.traffic_steering)
                        handover_scenario(pe, cells, OUTFLOW_SETTING)
                    else:
                        traffic_steering = 0
                        pe.update_steering(traffic_steering)
                        data['traffic_steering'].append(pe.traffic_steering)
                    # data['cell_distance'].append(pe.update_distance())
                    # handover_scenario(pe, cells, OUTFLOW_SETTING)
                    # print(cell.id)
                    # print(pe.pe_id)
                    # dic[pe.cell_id].append(pe.load)
                    # pe_list.append(pe)
            #         if pe.cell_id == cell.id:
            #             pe_list_load.append(pe.load * multiplier)
        # print(dic[1])
        if t > 0:
            for cell in cells:
                # print(cell.id)
                cell_load = sum(dic[cell.id])
                cell.update_load(cell_load)
                dic_cell_load[cell.id] = cell_load
                dic_cell_radius[cell.id] = cell.cell_radius
            # print(dic_cell_load)
            i = 0
            for pe in pe_list:
                # print('pe_id', pe.pe_id)
                pe_old_cell = pe_old_cell_id[i]
                # print('cell_id', pe_old_cell)
                data['cell_load'].append(dic_cell_load[pe_old_cell])
                # data['cell_radius'].append(dic_cell_radius[pe.cell_id])
                i += 1
            # print(len(A))
                # data['cell_radius'].append(dic_cell_radius[pe_old_cell])
                # print(dic_cell_load[pe_old_cell])

            # print(data['cell_load'])

    try:
        return pd.DataFrame(data)
    except ValueError as e:
        print(f"Error creating DataFrame: {e}")
        return None


def create_scenerio(inflow_setting, outflow_setting):
    scenerio = []

    for x in range(CELL_NUMBER):

        cat_list = []
        pe_list = []
        pe_list_id = []
        for y in range(CAT_NUMBER):

            pe_load_dict = INITIAL_CONFIG[y]
            pe_power_dict = INITIAL_CONFIG_POWER[y]
            # pe_list = []

            for z in range(PE_NUMBER):
                pe = PersonalEquipment(z + x * PE_NUMBER, pe_load_dict[z + x * PE_NUMBER], pe_power_dict[z + x * PE_NUMBER], x)
                pe.assign_category(y)
                pe_list.append(pe)
                pe_list_id.append(pe.pe_id)
            cat = Category(y, pe_list)
            cat_list.append(cat)

        cell = Cell(x, cat_list, pe_list_id)
        cell.assign_flow_lists(inflow_setting[x], outflow_setting[y])
        # cell.assign_handover_setting(HANDOVER_SETTING[x])
        # print(cell.load)
        scenerio.append(cell)
    return scenerio


def create_inflow_setting(outflow):
    # input type : {cell_id : [list of other cell ids]}
    # output type : {cell_id : [{cell_id: ratio }]}
    cell_ratios = {key: 1 / len(value) for key, value in outflow.items()}
    return {key: [{v: cell_ratios[v]} for v in value] for key, value in outflow.items()}


def handover_scenario(pe, cells, outflow_settings):
    source_cell = next((cell for cell in cells if cell.id == pe.cell_id), None)
    if source_cell:
        adjacent_cell_ids = outflow_settings.get(pe.cell_id, [])
        # print(adjacent_cell_ids)
        target_cell_id = random.choice(adjacent_cell_ids)
        target_cell = next((cell for cell in cells if cell.id == target_cell_id and cell.cell_barring == 0), None)
        if target_cell:
            if pe.traffic_steering == 1 or target_cell.cell_radius > pe.cell_dist:
                pe.perform_handover(source_cell, target_cell)
        # if pe.traffic_steering == 1:
        #     if target_cell and source_cell:
        #         pe.perform_handover(source_cell, target_cell)
        #         break
        # else:
        #     if target_cell:
        #         if source_cell.cell_radius < pe.cell_dist:
        #             # Perform handover logic
        #             pe.perform_handover(source_cell, target_cell)
        #             break  # Break after successful handover to the first available cell


def _print_scenario(cells):
    for cell in cells:
        print(f"Cell id: {cell.id} : ")
        for cat in cell.cat_list:
            print(f"Cat id: {cat.cat_id} : ")
            for pe in cat.pe_list:
                print(
                    f"PE Name: {pe.pe_name} Load: {pe.init_load} Ho_param: {pe.handover_param} Ho_mean: {pe.handover_mean} Ho_var: {pe.handover_var}")

        print()


if __name__ == '__main__':
    main()
