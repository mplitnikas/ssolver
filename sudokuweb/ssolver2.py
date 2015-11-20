def subtract(list1, list2):
	"""
	Subtracts elements of list1 from list2, returns the items
	contained in list2 that are not in list1 (but not vice-versa!)
	"""
	return [x for x in list2 if x not in list1]

def add(list1, list2):
	"""adds elements of two lists, eliminating duplicates"""
	return list1 + subtract(list1, list2)

full = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def possible(list1):
	"""
	Returns difference between given list and a full row 1-9.
	Data type is ['a', 'b', 'c']
	"""
	global full
	return subtract(list1, full)

def b_conv(x_coord, y_coord):
	"""
	Stepwise conversion method. Tells which of 9 3x3 boxes
	contains the selected x, y coordinates.
	"""
	if x_coord in range (0, 3):
		if y_coord in range (0, 3): return 1
		if y_coord in range (3, 6): return 2
		if y_coord in range (6, 9): return 3
	if x_coord in range (3, 6):
		if y_coord in range (0, 3): return 4
		if y_coord in range (3, 6): return 5
		if y_coord in range (6, 9): return 6
	if x_coord in range (6, 9):
		if y_coord in range (0, 3): return 7
		if y_coord in range (3, 6): return 8
		if y_coord in range (6, 9): return 9

side_length = 9

def iterate(func, func2 = None):

	global side_length

	for range(0, side_length):
		func2()
		for range (0, side_length):
			func()


class Engine(object):


	"""
	Runs the commands necessary to use Logic rules, and tracks cells.
	Engine is created at the beginning of the puzzle and runs it
	through to completion.
	"""

	def __init__(self):
		self.cells = []
		self.cell_populate()
		
		while True:
			print "Would you like to enter info by hand or via text file?"
			print "1. Manually"
			print "2. From sample"
#			print "3. From string"
			style = raw_input("> ")
			if style == '1':
				self.input()
				break
			elif style == '2':
				self.test_input()
				break
			else:
				print "Please enter either a 1 or 2."

		self.display()

	
	def cell_populate(self):

		"""
		Fills out 81 cells in the 9x9 grid. They all start with value = 0.
		Gives each an x, y, and box number to allow searches.
		"""
		for y in range(0, 9):
			self.cells.append([])
			for x in range(0, 9):
				self.cells[y].append(" ")

	def display(self):

		"""
		Clears out the last output, and updates with a new grid.
		Gives a space after the grid, and then the three lines
		at the bottom will be for I/O; this keeps the grid
		stable as it updates.
		"""
		print "\n" * 15
		for line in self.cells:
			print line
		print ""

	def test_input(self):
		self.cells = [
			['3', '1', '7', '.', '4', '.', '5', '9', '6'],
			['.', '6', '.', '.', '5', '.', '.', '3', '.'],
			['.', '.', '.', '.', '.', '.', '.', '.', '.'],
			['1', '.', '5', '4', '9', '3', '6', '.', '8'],
			['6', '3', '.', '.', '8', '.', '.', '1', '9'],
			['7', '9', '.', '.', '1', '.', '.', '5', '4'],
			['.', '7', '.', '.', '.', '.', '.', '6', '.'],
			['.', '4', '.', '7', '2', '5', '.', '8', '.'],
			['8', '.', '.', '9', '6', '1', '.', '.', '2'],
			]
	
	def input(self):

		"""
		Iterates through all cells and allows the user to enter the 
		correct value for each.
		"""
		for y in range(0, 9):
			for x in range(0, 9):
				self.set(x, y, "X")
				self.display()
				print "Please enter the number for the highlighted cell.\n"
				snum = raw_input("> ")
				if snum == '':
					self.set(x, y, ".")
					self.display()
				elif len(snum) >= 1:
					self.set(x, y, snum[0])
					self.display()

	def col_get(self, line_num):
		
		col_list = []

		for y in range(0, 9):
			col_list.append(self.get(line_num, y))

		return col_list

	def row_get(self, line_num):
		
		row_list = []

		for x in range(0, 9):
			row_list.append(self.get(x, line_num))

		return row_list

	def box_get(self, box_num):

		box_list = []

		for x in range(0, 9):
			for y in range(0, 9):
				if box_num == b_conv(x, y):
					box_list.append(self.get(x, y))

		return box_list

	def get(self, x, y):
		
		return self.cells[y][x]

	def set(self, x, y, value):
		
		self.cells[y][x] = value


class Logic(Engine):


	"""holds all of the rule methods used to determine and eliminate values"""
	def __init__(self):
		super(Logic, self).__init__()
		#vision = Display()
		#self.input() disabled for testing, look in Engine for sample data
		new = 0
		while True:
			new = self.solver()
			if new == 0:
				print "Final pass completed."
				break
			raw_input("One pass completed. > ")
		print "Hooray!"
		print "The sudoku has been solved!"
		print "^ - ^"

	def solver(self):
		#while self.final_checker() == False:
		solved = 0
		for y in range(0, 9):
			for x in range(0, 9):
				self.display()
				print "x: %r, y: %r, choices: %r" % (x, y, self.choices(x, y))
				if self.choices(x, y):
					if len(self.choices(x, y)) == 1:
						print "Setting to %r" % self.choices(x, y)[0],
						self.set(x, y, self.choices(x, y)[0])
						solved += 1
						raw_input(" >continue ")
		return solved


	def choices(self, x, y):

		if self.get(x, y) == ".":
			r = self.row_get(y)
			c = self.col_get(x)
			b = self.box_get(b_conv(x, y))
			rcb = add(r, add(c, b))

			return possible(rcb)

	def final_checker(self):
		"""Does the last check to see if all 81 cells are solved and happy."""
		global full

		for x in range(0, 9):
			for y in range(0, 9):

				if self.choices(x, y) != None:
					return True
					print "Solved!!!"
					exit()
				else:
					return False
				

class Display(object):
	"""
	In theory this will be used to drive a 2d display through cocos or other.
	"""
	def update(self):
		pass

puzzle3 = Logic()
#print puzzle3.display()
#print puzzle3.choices(0, 7)[0]
