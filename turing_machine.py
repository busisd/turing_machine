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
		

		
	def verify():
		'''
			Verifies that the machine is well-formed, returning True if it does
			and False if not.
			
			Includes checks for:
			 - All rules on the tape_end_char must move right and write tape_end_char
			 - All rules are on states and symbols that exist
			 - default_rule follows above two conditions
			 - blank_char and tape_end_char are not in input_alpha
			 - start, accept, and reject states are in states
		'''
		
		pass
		
		
		
		
		
		
		