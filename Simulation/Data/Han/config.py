CELL_NUMBER = 7

"""
Original Scenario:
1 Tick means 15 minutes
One day consists of 96 Ticks
5760 Tick is 60 days
Total SIM_TIME = 5760*3 = 6 months

If you change 1 tick length, you should recalculate handover rate loop in main.py 

Number of cell site 7, i.e., 1 tier
Channel bandwidth: 9MHz (45 Physical Resource Blocks(PRBs))
Number of User Equipments (UEs): 40
Radio Frequency (RF) scenarios setup: UEs uniformly distributed within 100 m of each BS
UE Mobility: Static: no mobility

"""
SIM_TIME = 5760 * 3  # 30000

SUBS_CATS = {0: "platinum"}
CAT_NUMBER = len(SUBS_CATS)

CELL_RADIUS = 100
TRAFFIC_STEERING = True

NUMBER_PE = 45
#PERSONAL_EQUIPMENT_ID = {0: "iot", 1: "vehicle", 2: "cell_phone", 3: "smart_watch", 4: "tablet"}
#PE_NUMBER = len(PERSONAL_EQUIPMENT_ID)

# {cat_id : {pe_id: value}} initial load per pe under cat
INITIAL_CONFIG = {
    0: {
        0: 5,
        1: 9,
        2: 25,
        3: 1,
        4: 5
    }
}

# {cell_id : [adjacency cell_id list]}
OUTFLOW_SETTING = {
    0: [1, 2, 3, 4, 5],
    1: [0, 2, 6],
    2: [0, 1, 3],
    3: [0, 2, 4],
    4: [0, 3, 5],
    5: [0, 4, 6],
    6: [0, 1, 5]
}

# 15 minutes(delta t) mean and variance setting
BASE_MEAN = 1 / 400
BASE_VAR = 1 / 3200

# {cell_id: {pe_id:{handover_mode:percentage (1 to 100)}}}
HANDOVER_SETTING = {
    0: {
        0: {
            0: 7.5,
            1: 9,
            2: 10.5,
            3: 12,
            4: 13.5
        }
    },
    1: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    },
    2: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    },
    3: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    },
    4: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    },
    5: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    },
    6: {
        0: {
            0: 2.5,
            1: 3,
            2: 3.5,
            3: 4,
            4: 4.5
        }
    }
}

# {cell_id: {pe_id:percentage (1 to 100)}}
HANDOVER_SETTING_0 = {
    0: {
        0: 7.5
    },
    1: {
        0: 2.5
    },
    2: {
        0: 2.5
    },

    3: {
        0: 2.5
    },
    4: {
        0: 2.5
    },
    5: {
        0: 2.5
    },
    6: {
        0: 2.5
    }
}

# {cell_id: {pe_id:percentage (1 to 100)}}
HANDOVER_SETTING_1 = {
    0: {
        0: 9
    },
    1: {
        0: 3
    },
    2: {
        0: 3
    },

    3: {
        0: 3
    },
    4: {
        0: 3
    },
    5: {
        0: 3
    },
    6: {
        0: 3
    }
}

# {cell_id: {pe_id:percentage (1 to 100)}}
HANDOVER_SETTING_2 = {
    0: {
        0: 10.5
    },
    1: {
        0: 3.5
    },
    2: {
        0: 3.5
    },

    3: {
        0: 3.5
    },
    4: {
        0: 3.5
    },
    5: {
        0: 3.5
    },
    6: {
        0: 3.5
    }
}

# {cell_id: {pe_id:percentage (1 to 100)}}
HANDOVER_SETTING_3 = {
    0: {
        0: 12
    },
    1: {
        0: 4
    },
    2: {
        0: 4
    },

    3: {
        0: 4
    },
    4: {
        0: 4
    },
    5: {
        0: 4
    },
    6: {
        0: 4
    }
}

# {cell_id: {pe_id:percentage (1 to 100)}}
HANDOVER_SETTING_4 = {
    0: {
        0: 13.5
    },
    1: {
        0: 4.5
    },
    2: {
        0: 4.5
    },

    3: {
        0: 4.5
    },
    4: {
        0: 4.5
    },
    5: {
        0: 4.5
    },
    6: {
        0: 4.5
    }
}

