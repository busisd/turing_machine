'''
	Author: Daniel Busis
	
	A program that defines and simulates Turing Machines.
	Designed to follow Model-View-Controller model; this
	is the model.
'''

class TuringMachine:
	def __init__(self, states, input_alpha, tape_alpha, rules, start_state, 
					accept_state = "state_accept", reject_state = "state_reject", 
					tape_end_char = '#', blank_char = '_', default_rule = None):
		'''
			Defines a Turing machine
			
			Necessary paremeters:			
			 - states is a set of strings that represent the name of each states.
			 - input_alpha is a set of strings (treated as single characters) that can
			   be written in the original input.
			 - tape_alpha is a set of strings (treated as single characters) that can be
			   written onto the tape. If start and blank character are not added by the user,
			   they are added automatically.
			 - rules is a dictionary of rules for what the Turing Machine can do. Each rules
			   is formatted as follows:
			     - {(state, char) : (new_state, new_char, direction)}
			   Where:
			     - state is in states
				 - char is in tape_alpha
				 - new_state is in states
				 - new_char is in tape_alpha
				 - direction = "L" or "R"
			   Note that rules can start empty and be added to with the add_rule() function.
			   Additionally, if it is provided as None, initializes to empty dictionary.
			   Additionally, if rules aren't provided, the following are automatically generated:
			     - For the tape end character, a rule that rewrites it and moves right for all states
				 - For the accept and reject states, a rule that rewrites any character and stays
				   in that state, moving right.
			 - start_state is one of the states in state, and where the machine starts. 
			 
			Optional paremeters:
			 - accept_state is one of the states in state, and represents the machine accepting. 
			   If not specified, defaults to "state_accept." Added to states automatically if
			   not done by the user.
			 - reject_state is one of the states in state, and represents the machine rejecting. 
			   If not specified, defaults to "state_reject." Added to states automatically if
			   not done by the user.
			 - tape_end_char is one of the strings in tape_alpha. Defaults to '#'. If not in
			   tape_alpha, it is added to tape_alpha.
			 - blank_char is one of the strings in tape_alpha. Defaults to '_'. If not in
			   tape_alpha, it is added to tape_alpha.
			 - default_rule is an optional parameter that is invoked if the machine reaches
			   a state/character combination it doesn't have a rule for. Provided in the form
			   (new_state, new_char, direction). If not provided, defaults to:
			   (reject_state, blank_char, "R").
			'''
		
		self.states = states
		self.input_alpha = input_alpha
		self.tape_alpha = tape_alpha
		if rules is not None:
			self.rules = rules
		else:
			self.rules = {}
		self.start_state = start_state
		self.accept_state = accept_state
		self.reject_state = reject_state
		
		self.tape_end_char = tape_end_char
		self.blank_char = blank_char
		if default_rule is not None:
			self.default_rule = default_rule
		else:
			self.default_rule = (reject_state, blank_char, "R")
		
		self.blank_char = blank_char
		
		if self.tape_end_char not in self.tape_alpha:
			self.tape_alpha.append(self.tape_end_char)
		if self.blank_char not in self.tape_alpha:
			self.tape_alpha.append(self.blank_char)
			
		if self.start_state not in self.states:
			self.states.append(self.start_state)
		if self.accept_state not in self.states:
			self.states.append(self.accept_state)
		if self.reject_state not in self.states:
			self.states.append(self.reject_state)
			
		for state in self.states:
			if self.rules.get((state, self.tape_end_char), None) is None:
				self.rules[(state, self.tape_end_char)] = (state, self.tape_end_char, "R")

		for char in self.tape_alpha:
			if self.rules.get((self.accept_state, char), None) is None:
				self.rules[(self.accept_state, char)] = (self.accept_state, char, "R")

		for char in self.tape_alpha:
			if self.rules.get((self.reject_state, char), None) is None:
				self.rules[(self.reject_state, char)] = (self.reject_state, char, "R")

		
		self.cur_state = None
		self.cur_head_pos = None
		self.tape = None

		
	
	
	def add_rule(self, state, char, new_state, new_char, direction):
		'''
			Adds a rule from (state, char) to (new_state, new_char, direction).
			If a rule from (state, char) already exists, it is replaced.
			
			Note: does not verify that inputted characters and states exist in
			the Turing Machine. This can be checked with verify()
		'''
		self.states[(state, char)] = (new_state, new_char, direction)
		
		
		
	def _rule_to_str(self, rule_key):
		'''
			Given the key for a rule, formats it as a string.
			
			Used for error generation.
		'''
		return str(rule_key) + " : " +str(self.rules[rule_key])
	
	
	
	def verify(self):
		'''
			Verifies that the machine is well-formed, returning a list of errors
			(empty if none found). 
			
			Includes checks for:
			 - All input characters are in the tape characters
			 - All rules are well-formed
			 - All rules are on states, symbols, and directions that exist
			 - All rules on the tape_end_char must move right and write tape_end_char
			 - default_rule follows above two conditions
			 - blank_char and tape_end_char are not in input_alpha
			 - start, accept, and reject states are in states
		'''
		
		errors = []
		
		for char in self.input_alpha:
			if char not in self.tape_alpha:
				new_error = "Error: character "+char+" in input but not tape alphabet"
				errors.append()

		if self.tape_end_char not in self.tape_alpha:
			new_error = "Error: tape end character "+self.tape_end_char+" in input but not tape alphabet"
			errors.append()
		if self.blank_char not in self.tape_alpha:
			new_error = "Error: character "+self.blank_char+" in input but not tape alphabet"
			errors.append()	
		
		for rule_key in self.rules.keys():
			if len(rule_key) != 2:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has key length != 2"
				errors.append(new_error)
				continue
			if len(self.rules[rule_key]) != 3:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has value length != 3"
				errors.append(new_error)
				continue
			
			if rule_key[0] not in self.states:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has key state that doesn't exist"
				errors.append(new_error)
			if rule_key[1] not in self.tape_alpha:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has key char that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][0] not in self.states:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has value state that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][1] not in self.tape_alpha:
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has value char that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][2] not in ("L", "R"):
				new_error = "Error: rule "+self._rule_to_str(rule_key)+" has direction that isn't 'L' or 'R'"
				errors.append(new_error)
				
			if rule_key[1] == self.tape_end_char:
				if self.rules[rule_key][1] != self.tape_end_char:
					new_error = "Error: rule "+self._rule_to_str(rule_key)+" doesn't re-write tape end!"
				if self.rules[rule_key][2] != "R":
					new_error = "Error: rule "+self._rule_to_str(rule_key)+" doesn't move right on tape end!"
				
		if len(self.default_rule) != 3:
			new_error = "Error: default rule has length != 3"
			errors.append(new_error)
		if self.default_rule[0] not in self.states:
			new_error = "Error: default rule has value state that doesn't exist"
			errors.append(new_error)
		if self.default_rule[1] not in self.tape_alpha:
			new_error = "Error: default rule has value char that doesn't exist"
			errors.append(new_error)
		if self.default_rule[2] not in ("L", "R"):
			new_error = "Error: default rule has direction that isn't 'L' or 'R'"
			errors.append(new_error)
					
		return errors
	
	
	
	def start_sim(self, input, starting_head_pos = 0):
		'''
			Initializes a simulation by creating and initializing the tape,
			setting the state to the start state, and setting the head position
			to the tape start
			
			Takes:
			 - input: a list of strings from tape_alpha
			Optionally:
			 - starting_head_pos: Defaults to 0. Starting position of the head 
			   on the tape. Must be >= 0 and <= length of the input.
		'''
		
		errors = self.verify()
		if errors: # if there are errors, return them and don't start
			return errors
		
		if starting_head_pos < 0:
			return["Error: head start position must not be negative"]
		if starting_head_pos < len(input):
			return["Error: head start position must not exceed length of input"]
		
		self.cur_state = self.start_state
		self.cur_head_pos = starting_head_pos
		self.tape = [self.tape_end_char]
		
		for input_char in input:
			if input_char not in self.input_alpha:
				return ["Error: Character " + input_char + " is not a valid part of the input alphabet"]
			self.tape.append(input_char)
		
		
		
	def step_sim(self):
		'''
			Steps the turing machine a single time, using its current state,
			head position, and tape.
			
			Should only be called after the simulation has been started 
			using start_sim.
		'''
		
		if self.cur_state is None:
			return ["Error! Simulation not initialized! Call start_sim() first!"]
		
		cur_tuple = (self.cur_state, self.tape[self.cur_head_pos])
		
		action = self.rules.get(cur_tuple, self.default_rule)
		
		self.cur_state = action[0]
		self.tape[self.cur_head_pos] = action[1]
		if action[2] == "L":
			self.cur_head_pos -= 1
		else:
			self.cur_head_pos += 1

		if self.cur_head_pos >= len(self.tape):
			self.tape.append(self.blank_char)
	
	
	
	def has_ended(self):
		'''
			Returns whether the Turing Machine has reached the accept/reject states.
			
			Returns "accept", "reject", or False as appropriate.
		'''
		if self.cur_state == self.accept_state:
			return "accept"
		elif self.cur_state == self.reject_state:
			return "reject"
		else:
			return False
		
		
	
	def get_current_state(self):
		'''
			Returns a dictionary containing the current state,
			head position, and tape of the Turing Machine, 
			formatted as follows:
			
			{
				head_pos: (int head_pos)
				cur_state: (string current_state)
				tape: (list tape)
			}
		'''
		cur_state_dict = {
			head_pos: self.head_pos,
			cur_state: self.cur_state,
			tape: self.tape
		}
		
		
			
def main():
	'''
		Runs a test on a TM that accepts strings in the form:
		{0^n1^n2^n}
	'''
	TM = TuringMachine(["look_for_0", "look_for_1", "look_for_2", "reset"], 
					["0", "1", "2"], 
					["0", "1", "2", "_", "#", "X"], 
					{	("reset", "#"):("look_for_0", "#", "R"),
						("look_for_0", "X"):("look_for_0", "X", "R"),
						("look_for_0", "0"):("look_for_1", "X", "R"),
						("look_for_0", "1"):("state_reject", "1", "R"),
						("look_for_0", "2"):("state_reject", "2", "R"),
						("look_for_0", "_"):("state_accept", "_", "R"),
						("look_for_1", "0"):("look_for_1", "0", "R"),
						("look_for_1", "X"):("look_for_1", "X", "R"),
						("look_for_1", "1"):("look_for_2", "X", "R"),
						("look_for_1", "2"):("state_reject", "2", "R"),
						("look_for_1", "_"):("state_reject", "_", "R"),
						("look_for_2", "1"):("look_for_2", "1", "R"),
						("look_for_2", "X"):("look_for_2", "X", "R"),
						("look_for_2", "2"):("reset", "X", "R"),
						("look_for_2", "_"):("state_accept", "_", "R"),
						("reset", "X"):("reset", "X", "L"),
						("reset", "0"):("reset", "0", "L"),
						("reset", "1"):("reset", "1", "L"),
						("reset", "2"):("reset", "2", "L"),
						("reset", "_"):("reset", "_", "L"),
					}, 
					"reset", 
					# accept_state = "state_accept", 
					# reject_state = "state_reject", 
					tape_end_char = '#', 
					blank_char = '_', 
					default_rule = None)
					
	print(TM.start_sim("000111222"))
	while not TM.has_ended():
		print(TM.tape, TM.cur_state, TM.cur_head_pos)
		TM.step_sim()
	print(TM.has_ended())
	
	# TM.step_sim()
	# print(TM.tape, TM.cur_state, TM.cur_head_pos)
	# print(TM.has_ended())
	# TM.step_sim()
	# print(TM.tape, TM.cur_state, TM.cur_head_pos)
	# print(TM.has_ended())
	# TM.step_sim()
	# print(TM.tape, TM.cur_state, TM.cur_head_pos)
	# print(TM.has_ended())

	
	print(TM.start_sim("120"))
	while not TM.has_ended():
		print(TM.tape, TM.cur_state, TM.cur_head_pos)
		TM.step_sim()
	print(TM.has_ended())
	
	print(TM.start_sim("0011222"))
	while not TM.has_ended():
		print(TM.tape, TM.cur_state, TM.cur_head_pos)
		TM.step_sim()
	print(TM.has_ended())
	
if __name__ == "__main__":
	main()


