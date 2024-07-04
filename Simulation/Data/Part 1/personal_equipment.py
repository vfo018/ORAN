from config import *
from distribution import gaussian_distribution
import random
class PersonalEquipment(object):
	"""
	docstring for PersonalEquipment
	string or int id - id can be in this format: 3 digits, First digit is id of cell it is connected Second one is category it is inside, 
	int: pe_id : which Personal Equipment (iot mobile bla bla)
	string : pe_name: auto_generated
	int: init_load : Under cell i category j what is the load  

	"""
	def __init__(self, pe_id, init_load, init_power, cell_id):
		self.pe_id = pe_id
		# self.pe_name = PERSONAL_EQUIPMENT_ID[pe_id]
		self.init_load = init_load
		self.ho_dist = gaussian_distribution
		self.load = init_load
		self.power = init_power
		self.handover_mode = 0
		self.cell_dist = 100
		self.cell_id = cell_id
		self.handover = 0
		self.cell_load = PRB
		self.cell_dist = 0
		self.has_anomaly = 0

	def assign_category(self, cat_id):
		self.cat_id = cat_id
		
	def assign_handover_params(self, handover_setting):
		self.handover_param = handover_setting[self.pe_id]
		self.update_handover_params()

	def update_handover_params(self):
		self.handover_mean = self.load * BASE_MEAN * self.handover_param[self.handover_mode]
		self.handover_var = self.load * BASE_VAR * self.handover_param[self.handover_mode]

	def set_load(self, load):
		self.load = load

	def set_cell_load(self, load):
		self.cell_load = load

	def update_handover(self, handover):
		self.handover = handover

	def set_handover_mode(self,handover_mode):
		self.handover_mode = handover_mode
		self.update_handover_params()
		
	def get_normal_distribution(self):
		return gaussian_distribution(self.handover_mean, self.handover_var)

	def update_cell_id(self, cell_id):
		self.cell_id = cell_id

	def update_anomaly(self, has_anomaly):
		self.has_anomaly = has_anomaly

	def update_distance(self):
		if 0 < self.power <= 0.05:
			# cell_dist = random.uniform(120, 130)
			cell_dist = random.uniform(126, 130)
		elif 0.05 < self.power <= 0.1:
			# cell_dist = random.uniform(110, 120)
			cell_dist = random.uniform(122, 126)
		elif 0.1 < self.power <= 0.2:
			# cell_dist = random.uniform(100, 110)
			cell_dist = random.uniform(118, 122)
		elif 0.2 < self.power <= 0.3:
			# cell_dist = random.uniform(90, 100)
			cell_dist = random.uniform(116, 118)
		elif 0.4 < self.power <= 0.6:
			# cell_dist = random.uniform(80, 90)
			cell_dist = random.uniform(114, 116)
		elif 0.6 < self.power <= 0.8:
			# cell_dist = random.uniform(60, 80)
			cell_dist = random.uniform(112, 114)
		elif 0.8 < self.power <= 1.0:
			# cell_dist = random.uniform(50, 60)
			cell_dist = random.uniform(110, 112)
		elif 1.0 < self.power <= 1.2:
			# cell_dist = random.uniform(40, 50)
			cell_dist = random.uniform(108, 110)
		elif 1.2 < self.power <= 1.4:
			# cell_dist = random.uniform(30, 40)
			cell_dist = random.uniform(106, 108)
		elif 1.4 < self.power <= 1.6:
			# cell_dist = random.uniform(20, 30)
			cell_dist = random.uniform(104, 106)
		elif 1.6 < self.power <= 1.8:
			# cell_dist = random.uniform(10, 20)
			cell_dist = random.uniform(102, 104)
		else:
			# cell_dist = random.uniform(1, 10)
			cell_dist = random.uniform(100, 102)
		self.cell_dist = cell_dist
		return cell_dist

	def perform_handover(self, source_cell, target_cell):
		"""
        Logic to transfer PE from source cell to target cell.
        """
		# Decrease load from source and increase in target
		# source_cell.decrease_load_list(self.pe_id, self.load)
		# target_cell.increase_load_list(self.pe_id, self.load)
		# Update PE's cell_id
		self.update_cell_id(target_cell.id)
		# self.cell_id = target_cell.id
	# print(f"Handed over PE {pe.pe_id} from Cell {source_cell.id} to Cell {target_cell.id}")
