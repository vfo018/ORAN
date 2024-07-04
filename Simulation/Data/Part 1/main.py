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

    cells = create_scenario(inflow_setting, OUTFLOW_SETTING)

    print("Scenario created, simulation will start")

    # time iteration and creating the data frame
    df = simulation(cells)

    print("Simulation ended, data will be exported")
    try:
        df.to_csv('output_handover_scenario_testing_UE70.csv', index=False)
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
    # check PING-PONG effects
    dic_traffic_steering_history = {i: [] for i in range(CELL_NUMBER)}

    for t in range(SIM_TIME):
        # Add random anomalities to data based on anomaly_idx
        has_anomaly = 0
        if anomaly_idx < num_anomaly:
            if anomaly_steps[anomaly_idx] <= t <= anomaly_step_ends[anomaly_idx]:
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

        # now we need to assign handovers to other cells and categories.
        if t == 0:
            pe_list = []
            dic_cell_load = {i: [] for i in range(CELL_NUMBER)}
            cat_new_load, cell_new_load = 0, 0
            dic_traffic_steering = {i: 0 for i in range(CELL_NUMBER)}
            for cell in cells:
                for cat in cell.cat_list:
                    for pe in cat.pe_list:
                        cell_new_load += pe.load * multiplier
                        pe_list.append(pe)
                cell.update_load(cell_new_load)
                dic_cell_load[cell.id] = cell.load
                radius_flag = cell.update_radius_flag()
                if cell.load > STEERING_THRE:
                    dic_traffic_steering[cell.id] = 1
                else:
                    dic_traffic_steering[cell.id] = 0
                # print(cell.id, cell.load)
                cell_new_load = 0
                dic_traffic_steering_history[cell.id].append(dic_traffic_steering[cell.id])
                cell.update_radius()
            for pe in pe_list:
                data['cell_load'].append(dic_cell_load[pe.cell_id])
                data['traffic_steering'].append(dic_traffic_steering[pe.cell_id])
                data['cell_barring'].append(0)
                data['cell_radius'].append(CELL_RADIUS)
            # print(data['cell_load'])

        traffic_steering, cell_barring = 0, 0

        # now loads are balanced, write information to dictionary so that we can convert it to pandas and csv
        # cell_id to pe_id dictionary
        dic = {i: [] for i in range(CELL_NUMBER)}
        dic_cell_load = {i: [] for i in range(CELL_NUMBER)}

        pe_list, pe_old_cell_id = [], []
        # dic_cell_barring = {i: [] for i in range(CELL_NUMBER)}
        dic_cell_radius = {i: 0 for i in range(CELL_NUMBER)}
        # dic_cell_steering = {i: 0 for i in range(CELL_NUMBER)}
        # for cell in cells:
        #     if t > 0:
        #         cell_old_radius = cell.cell_radius
        #         cell_radius = cell.update_radius()
        #         if cell_radius > cell_old_radius:
        #             dic_traffic_steering[cell.id] = 2
        #         elif cell_radius < cell_old_radius:
        #             dic_traffic_steering[cell.id] = 1
        #         else:
        #             dic_traffic_steering[cell.id] = 0
        #         # print(cell_radius)
        #         dic_cell_radius[cell.id] = cell_radius
        #     else:
        #         cell_radius = CELL_RADIUS
        #         dic_cell_radius[cell.id] = cell_radius
        #
        #     # Check for ping-pong effect in traffic steering
        #     if len(dic_traffic_steering_history[cell.id]) >= PINGPONG:
        #         last_four_steerings = dic_traffic_steering_history[cell.id][-PINGPONG:]
        #         if (last_four_steerings == [1, 2, 1, 2] and dic_traffic_steering[cell.id] == 1) or \
        #                 (last_four_steerings == [2, 1, 2, 1] and dic_traffic_steering[cell.id] == 2):
        #             cell.update_barring(0)
        #             dic_traffic_steering[cell.id] = 0
        #
        #     # Update traffic steering history
        #     dic_traffic_steering_history[cell.id].append(dic_traffic_steering[cell.id])
        #     if len(dic_traffic_steering_history[cell.id]) > PINGPONG:
        #         dic_traffic_steering_history[cell.id].pop(0)

        for cell in cells:
            for cat in cell.cat_list:
                if cat.pe_list is not None:
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
                        # data['cell_barring'].append(cell.cell_barring)
                        # if t > 0:
                        #     data['cell_barring'].append(dic_cell_barring[pe.cell_id])
                        data['cell_distance'].append(pe.update_distance())
                        # data['cell_radius'].append(dic_cell_radius[pe.cell_id])
                        # if t > 0:
                        #     data['traffic_steering'].append(dic_traffic_steering[pe.cell_id])
                        # print(data['cell_load'])
                        pe_list.append(pe)
                        pe_old_cell_id.append(pe.cell_id)
                        dic[pe.cell_id].append(pe.load)

        dic_cell_barring = {i: 0 for i in range(CELL_NUMBER)}
        dic_traffic_steering = {i: 0 for i in range(CELL_NUMBER)}
        if t > 0:
            for cell in cells:
                # print(cell.id)
                cell_load = sum(dic[cell.id])
                cell.update_load(cell_load)
                dic_cell_load[cell.id] = cell_load
                # print(dic_cell_load)
                if cell.load > PRB and cell.cell_radius == MIN_CELL_RADIUS:
                    cell_barring = 1
                    cell.update_barring(cell_barring)
                    dic_cell_barring[cell.id] = cell_barring
                else:
                    cell_barring = 0
                    cell.update_barring(cell_barring)
                    dic_cell_barring[cell.id] = cell_barring

            for cell in cells:
                cell_old_radius = cell.cell_radius
                dic_cell_radius[cell.id] = cell_old_radius
                dic_traffic_steering[cell.id] = cell.update_radius_flag()
                # cell_radius = cell.update_radius()
                # # dic_cell_radius[cell.id] = cell_radius
                # if cell_radius > cell_old_radius:
                #     dic_traffic_steering[cell.id] = 2
                #     # dic_cell_radius[cell.id] = cell_radius
                # elif cell_radius < cell_old_radius:
                #     dic_traffic_steering[cell.id] = 1
                #     # dic_cell_radius[cell.id] = cell_radius
                # else:
                #     dic_traffic_steering[cell.id] = 0
                    # dic_cell_radius[cell.id] = cell_radius

                # Check for ping-pong effect in traffic steering
                if len(dic_traffic_steering_history[cell.id]) >= PINGPONG:
                    last_four_steerings = dic_traffic_steering_history[cell.id][-PINGPONG:]
                    if (last_four_steerings == [1, 2, 1, 2] and dic_traffic_steering[cell.id] == 1) or \
                            (last_four_steerings == [2, 1, 2, 1] and dic_traffic_steering[cell.id] == 2):
                        dic_traffic_steering[cell.id] = 0

                # Update traffic steering history
                dic_traffic_steering_history[cell.id].append(dic_traffic_steering[cell.id])
                if len(dic_traffic_steering_history[cell.id]) > PINGPONG:
                    dic_traffic_steering_history[cell.id].pop(0)

            cell_3 = next((cell for cell in cells if cell.id == 3), None)
            if cell_3:
                if all(dic_cell_barring[i] == 1 for i in OUTFLOW_SETTING[3]):
                    cell_3.update_barring(1)
                    dic_cell_barring[3] = 1
                # print(dic_traffic_steering)


            i = 0
            for pe in pe_list:
                # print('pe_id', pe.pe_id)
                pe_old_cell = pe_old_cell_id[i]
                # print('cell_id', pe_old_cell)
                data['cell_load'].append(dic_cell_load[pe_old_cell])
                data['cell_barring'].append(dic_cell_barring[pe_old_cell])
                data['cell_radius'].append(dic_cell_radius[pe.cell_id])
                data['traffic_steering'].append(dic_traffic_steering[pe_old_cell])
                # data['cell_radius'].append(dic_cell_radius[pe.cell_id])
                i += 1
                if has_anomaly == 1 or (
                        pe.cell_dist > dic_cell_radius[pe.cell_id] and dic_cell_load[pe_old_cell] > STEERING_THRE):
                    if dic_cell_barring[pe.cell_id] != 1:
                        handover = 1
                        pe.update_handover(handover)
                        # data['traffic_steering'].append(pe.traffic_steering)
                        handover_scenario(pe, cells, OUTFLOW_SETTING)
                    else:
                        random_float = np.random.rand()
                        if random_float >= 2 / 3:
                            handover = 1
                            pe.update_handover(handover)
                            # data['traffic_steering'].append(pe.traffic_steering)
                            handover_scenario(pe, cells, OUTFLOW_SETTING)
                else:
                    handover = 0
                    pe.update_handover(handover)

            for cell in cells:
                cell.update_radius()

        # print(dic_traffic_steering_history)
            # print(len(A))
            # data['cell_radius'].append(dic_cell_radius[pe_old_cell])
            # print(dic_cell_load[pe_old_cell])

            # print(data['cell_load'])

    try:
        return pd.DataFrame(data)
    except ValueError as e:
        print(f"Error creating DataFrame: {e}")
        return None


def create_scenario(inflow_setting, outflow_setting):
    scenario = []

    for x in range(CELL_NUMBER):

        cat_list = []
        pe_list = []
        pe_list_id = []
        for y in range(CAT_NUMBER):

            pe_load_dict = INITIAL_CONFIG[y]
            pe_power_dict = INITIAL_CONFIG_POWER[y]
            # pe_list = []

            for z in range(PE_NUMBER):
                pe = PersonalEquipment(z + x * PE_NUMBER, pe_load_dict[z + x * PE_NUMBER],
                                       pe_power_dict[z + x * PE_NUMBER], x)
                pe.assign_category(y)
                pe_list.append(pe)
                pe_list_id.append(pe.pe_id)
            cat = Category(y, pe_list)
            cat_list.append(cat)

        cell = Cell(x, cat_list, pe_list_id)
        cell.assign_flow_lists(inflow_setting[x], outflow_setting[y])
        # cell.assign_handover_setting(HANDOVER_SETTING[x])
        # print(cell.load)
        scenario.append(cell)
    return scenario


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
            if pe.handover == 1 or target_cell.cell_radius > pe.cell_dist:
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
