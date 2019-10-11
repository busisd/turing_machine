'''
	Author: Daniel Busis
	
	A program that defines and simulates Turing Machines
'''

class TuringMachine:
	def __init__(self, states, input_alpha, tape_alpha, rules, start_state, 
					accept_state = "state_accept", reject_state = "state_reject", 
					start_char = '#', blank_char = '_', default_rule = None):
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
			 - start_state is one of the states in state, and where the machine starts. 
			 
			Optional paremeters:
			 - accept_state is one of the states in state, and represents the machine accepting. 
			   If not specified, defaults to "state_accept." Added to states automatically if
			   not done by the user.
			 - reject_state is one of the states in state, and represents the machine rejecting. 
			   If not specified, defaults to "state_reject." Added to states automatically if
			   not done by the user.
			 - start_char is one of the strings in tape_alpha. Defaults to '#'. If not in
			   tape_alpha, it is added to tape_alpha.
			 - blank_char is one of the strings in tape_alpha. Defaults to '_'. If not in
			   tape_alpha, it is added to tape_alpha.
			 - default_rule is an optional parameter that is invoked if the machine reaches
			   a state/character combination it doesn't have a rule for. Provided in the form
			   (new_state, new_char, direction). If not provided, defaults to:
			   (reject_state, blank_char, "R").
			   
			Other components:
			 - tape is a list of characters, that starts with only tape_end_char.
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
		self.tape = [blank_char]
		
		if self.tape_end_char not in self.tape_alpha:
			self.tape_alpha.append(self.tape_end_char)
		if self.blank_char not in self.tape_alpha:
			self.tape_alpha.append(self.blank_char)
			
		if self.start_state not in self.states:
			self.states.append(self.start_state)
		if self.end_state not in self.states:
			self.states.append(self.end_state)
		
	
	
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
			 - All rules are well-formed
			 - All rules are on states, symbols, and directions that exist
			 - All rules on the tape_end_char must move right and write tape_end_char
			 - default_rule follows above two conditions
			 - blank_char and tape_end_char are not in input_alpha
			 - start, accept, and reject states are in states
		'''
		
		errors = []
		
		for rule_key in self.rules.keys():
			if len(rule_key) != 2:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has key length != 2"
				errors.append(new_error)
				continue
			if len(self.rules[rule_key]) != 3:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has value length != 3"
				errors.append(new_error)
				continue
			
			if rule_key[0] not in self.states:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has key state that doesn't exist"
				errors.append(new_error)
			if rule_key[1] not in self.tape_alpha:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has key char that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][0] not in self.rules:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has value state that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][1] not in self.tape_alpha:
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has value char that doesn't exist"
				errors.append(new_error)
			if self.rules[rule_key][2] not in ("L", "R"):
				new_error = "Error: rule "+_rule_to_str(rule_key)+" has direction that isn't 'L' or 'R'"
				errors.append(new_error)
				
		if len(self.default_rule) != 3:
			new_error = "Error: default rule has length != 3"
			errors.append(new_error)
		if default_rule[0] not in self.rules:
			new_error = "Error: default rule has value state that doesn't exist"
			errors.append(new_error)
		if default_rule[1] not in self.tape_alpha:
			new_error = "Error: default rule has value char that doesn't exist"
			errors.append(new_error)
		if default_rule[2] not in ("L", "R"):
			new_error = "Error: default rule has direction that isn't 'L' or 'R'"
			errors.append(new_error)
		
		return errors
		
		
		
		
		
		
		