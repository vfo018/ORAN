import numpy as np


CELL_NUMBER = 7
CELL_RADIUS = 130
MIN_CELL_RADIUS = 10
BARRING_DISTANCE = 30
BARRING_THRE = 45
PE_NUMBER = 40
TOTAL_PE_NUMBER = PE_NUMBER * CELL_NUMBER
PRB = 45
TOTAL_PRB = PRB * CELL_NUMBER
AVG_PRB = PRB/PE_NUMBER
"""
Assume each UE holding 1 PRB in 1 tick.
"""
"""
Original Scenario:
1 Tick means 15 minutes
One day consists of 96 Ticks
5760 Tick is 60 days
Total SIM_TIME = 5760*3 = 6 months

If you change 1 tick length, you should recalculate handover rate loop in main.py 
"""
# SIM_TIME = 5760*3 #30000

SIM_TIME = 96

# define percentage of anomalies number of occurence
ANOMALY_PERCENTAGE = 0.025

# SUBS_CATS = {0:"silver", 1:"gold", 2:"platinium"}
SUBS_CATS = {0:"platinium"}
CAT_NUMBER = len(SUBS_CATS)

PERSONAL_EQUIPMENT_ID = {0:"iot",1:"vehicle",2:"cell_phone",3:"smart_watch",4:"tablet"}
# PE_NUMBER = len(PERSONAL_EQUIPMENT_ID)

# {cat_id : {pe_id: value}} percentage of pe types under category i
# Generate initial loads for all UEs (PE_NUMBER * CELL_NUMBER UEs)
MU = PRB/PE_NUMBER
SIGMA = MU/3
INITIAL_LOADS = np.random.normal(MU, SIGMA, TOTAL_PE_NUMBER)
INITIAL_CONFIG = {
	0: {}
}
for i, v in enumerate(INITIAL_LOADS):
	key = i
	value = v
	INITIAL_CONFIG[0][key] = float(value)

# {cell_id : [adjacency cell_id list]}
OUTFLOW_SETTING = {
	0: [1, 3, 6],
	1: [0, 2, 3],
	2: [1, 3, 4],
	3: [0, 1, 2, 4, 5, 6],
	4: [2, 3, 5],
	5: [3, 4, 6],
	6: [0, 3, 5]
}


# 15 minutes(delta t) mean and variance setting
BASE_MEAN = 1/400
BASE_VAR = 1/3200






ANOMALY_HANDOVER_SETTING = {
	0:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	},
	1:{
		0:0.5,
		1:10,
		2:2.5,
		3:2.5,
		4:1
	},
	2:{
		0:2,
		1:40,
		2:10,
		3:10,
		4:4
	},
	# 2:{
	# 	0:1,
	# 	1:20,
	# 	2:5,
	# 	3:5,
	# 	4:2
	# },

	3:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	},
	4:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	}
}

REVERSE_ANOMALY_HANDOVER_SETTING = {
	0:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	},
	1:{
		0:2,
		1:40,
		2:10,
		3:10,
		4:4
	},
	2:{
		0:2,
		1:40,
		2:10,
		3:10,
		4:4
	},
	# 2:{
	# 	0:1,
	# 	1:20,
	# 	2:5,
	# 	3:5,
	# 	4:2
	# },

	3:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	},
	4:{
		0:1,
		1:20,
		2:5,
		3:5,
		4:2
	}
}


