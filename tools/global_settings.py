PATH = '..\Wyniki_beh'

MEASURED_VARIABLES = ['IMM','FOC','HAP','ANG','SAD','FEA','GUI','DIS','ARO','VAL']

EVENT_NAMES_FORMAL = [f'S{n_sce}_{part_name}' for n_sce in range(1,6) \
                      for part_name in ["P1P2","P3","P4","P5"]]

EVENT_NAMES_INFORMAL = [f'S{n_sce}_P{n_part}' for n_sce in range(1,6) \
                        for n_part in range(2,6)]

DICT_INFORMAL_2_FORMAL = {EVENT_NAMES_INFORMAL[n]:EVENT_NAMES_FORMAL[n] \
                          for n in range(len(EVENT_NAMES_INFORMAL))}

TIME_POINT_LIST = [f"TP{n}" for n in [1,2,3,4,5,61,62,63,64,71,72,73,81,82,83]]