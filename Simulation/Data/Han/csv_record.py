import csv

cell_0_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_0_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_1_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_1_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_2_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_2_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_3_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_3_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_4_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_4_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_5_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_5_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

cell_6_fileHeader = ["time_period", "cell_id", "pe_id", "load"]
cell_6_total_load_fileHeader = ["time_period", "total_load", "cell_barring", "cell_radius", "pes_num"]

pes_results_fileHeader = ["time_period", "cell_id", "pe_id", "pe_load", "pes_num"]


cell_0_results = []
cell_0_total_load_results = []
cell_1_results = []
cell_1_total_load_results = []
cell_2_results = []
cell_2_total_load_results = []
cell_3_results = []
cell_3_total_load_results = []
cell_4_results = []
cell_4_total_load_results = []
cell_5_results = []
cell_5_total_load_results = []
cell_6_results = []
cell_6_total_load_results = []
pes_results = []

def save_result_csv(folder_path):
    cell_0_csvFile = open(f'{folder_path}/cell_0_results.csv', "w")
    cell_0_writer = csv.writer(cell_0_csvFile)
    cell_0_writer.writerow(cell_0_fileHeader)
    cell_0_writer.writerows(cell_0_results)
    cell_0_csvFile.close()

    cell_0_total_load_csvFile = open(f'{folder_path}/cell_0_total_load_results.csv', "w")
    cell_0_total_load_writer = csv.writer(cell_0_total_load_csvFile)
    cell_0_total_load_writer.writerow(cell_0_total_load_fileHeader)
    cell_0_total_load_writer.writerows(cell_0_total_load_results)
    cell_0_total_load_csvFile.close()

    cell_1_csvFile = open(f'{folder_path}/cell_1_results.csv', "w")
    cell_1_writer = csv.writer(cell_1_csvFile)
    cell_1_writer.writerow(cell_1_fileHeader)
    cell_1_writer.writerows(cell_1_results)
    cell_1_csvFile.close()

    cell_1_total_load_csvFile = open(f'{folder_path}/cell_1_total_load_results.csv', "w")
    cell_1_total_load_writer = csv.writer(cell_1_total_load_csvFile)
    cell_1_total_load_writer.writerow(cell_1_total_load_fileHeader)
    cell_1_total_load_writer.writerows(cell_1_total_load_results)
    cell_1_total_load_csvFile.close()

    cell_2_csvFile = open(f'{folder_path}/cell_2_results.csv', "w")
    cell_2_writer = csv.writer(cell_2_csvFile)
    cell_2_writer.writerow(cell_2_fileHeader)
    cell_2_writer.writerows(cell_2_results)
    cell_2_csvFile.close()

    cell_2_total_load_csvFile = open(f'{folder_path}/cell_2_total_load_results.csv', "w")
    cell_2_total_load_writer = csv.writer(cell_2_total_load_csvFile)
    cell_2_total_load_writer.writerow(cell_2_total_load_fileHeader)
    cell_2_total_load_writer.writerows(cell_2_total_load_results)
    cell_2_total_load_csvFile.close()

    cell_3_csvFile = open(f'{folder_path}/cell_3_results.csv', "w")
    cell_3_writer = csv.writer(cell_3_csvFile)
    cell_3_writer.writerow(cell_3_fileHeader)
    cell_3_writer.writerows(cell_3_results)
    cell_3_csvFile.close()

    cell_3_total_load_csvFile = open(f'{folder_path}/cell_3_total_load_results.csv', "w")
    cell_3_total_load_writer = csv.writer(cell_3_total_load_csvFile)
    cell_3_total_load_writer.writerow(cell_3_total_load_fileHeader)
    cell_3_total_load_writer.writerows(cell_3_total_load_results)
    cell_3_total_load_csvFile.close()

    cell_4_csvFile = open(f'{folder_path}/cell_4_results.csv', "w")
    cell_4_writer = csv.writer(cell_4_csvFile)
    cell_4_writer.writerow(cell_4_fileHeader)
    cell_4_writer.writerows(cell_4_results)
    cell_4_csvFile.close()

    cell_4_total_load_csvFile = open(f'{folder_path}/cell_4_total_load_results.csv', "w")
    cell_4_total_load_writer = csv.writer(cell_4_total_load_csvFile)
    cell_4_total_load_writer.writerow(cell_4_total_load_fileHeader)
    cell_4_total_load_writer.writerows(cell_4_total_load_results)
    cell_4_total_load_csvFile.close()

    cell_5_csvFile = open(f'{folder_path}/cell_5_results.csv', "w")
    cell_5_writer = csv.writer(cell_5_csvFile)
    cell_5_writer.writerow(cell_5_fileHeader)
    cell_5_writer.writerows(cell_5_results)
    cell_5_csvFile.close()

    cell_5_total_load_csvFile = open(f'{folder_path}/cell_5_total_load_results.csv', "w")
    cell_5_total_load_writer = csv.writer(cell_5_total_load_csvFile)
    cell_5_total_load_writer.writerow(cell_5_total_load_fileHeader)
    cell_5_total_load_writer.writerows(cell_5_total_load_results)
    cell_5_total_load_csvFile.close()

    cell_6_csvFile = open(f'{folder_path}/cell_6_results.csv', "w")
    cell_6_writer = csv.writer(cell_6_csvFile)
    cell_6_writer.writerow(cell_6_fileHeader)
    cell_6_writer.writerows(cell_6_results)
    cell_6_csvFile.close()

    cell_6_total_load_csvFile = open(f'{folder_path}/cell_6_total_load_results.csv', "w")
    cell_6_total_load_writer = csv.writer(cell_6_total_load_csvFile)
    cell_6_total_load_writer.writerow(cell_6_total_load_fileHeader)
    cell_6_total_load_writer.writerows(cell_6_total_load_results)
    cell_6_total_load_csvFile.close()

    pes_results_csvFile = open(f'{folder_path}/pes_results.csv', "w")
    pes_results_writer = csv.writer(pes_results_csvFile)
    pes_results_writer.writerow(pes_results_fileHeader)
    pes_results_writer.writerows(pes_results)
    pes_results_csvFile.close()