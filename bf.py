


class bf_core:

	def __init__(self):
		self.instructions = []
		self.ops = {'>':self.inc_dp, '<':self.dec_dp, '+':self.inc_reg, '-':self.dec_reg, '.':self.reg_print, ',':self.reg_store, '[':self.loop_enter, ']':self.loop_end}
		self.dp = 0
		self.pc = 0
		self.reg = [0]
		self.maxreg = len(self.reg)
		self.stack = []
		self.outreg = 0
		self.outdv = 0
		self.inreg = 0
		self.verbose = True

		#program info
		self.instructioncount = 0
		self.memoryused = 1

	#============================================================
	#Increment data pointer operation (> operator)
	#============================================================
	def inc_dp(self):

		self.dp = self.dp + 1

		while len(self.reg) < self.dp+1 :
			self.reg.append(0)
			self.memoryused = len(self.reg)
		
		self.pc = self.pc + 1

	#============================================================
	#Decrement the data pointer (< operator)
	#============================================================
	def dec_dp(self):

		self.dp = self.dp - 1

		if self.dp < 0:
			print "data pointer underflow on instruction {0}, exiting".format(self.pc)
			self.gtfo()

		else:
			self.pc = self.pc + 1 

	#============================================================
	#Increment the register (+ operator)
	#============================================================
	def inc_reg(self):

		self.reg[self.dp] = self.reg[self.dp] + 1
		self.pc = self.pc + 1 


	#============================================================
	#Decrement the register (- operator)
	#============================================================
	def dec_reg(self):

		self.reg[self.dp] = self.reg[self.dp] - 1
		self.pc = self.pc + 1 

	#============================================================
	#Output the data in register (. operator)
	#============================================================
	def reg_print(self):
		
		self.VerbosePrint(self.reg[self.dp])
		self.outreg = self.reg[self.dp]
		self.outdv = 1
		self.pc = self.pc + 1
		

	#============================================================
	#Store data in a register (, operator)
	#============================================================
	def reg_store(self):

		print self.inreg
		self.reg[self.dp] = self.inreg
		self.pc = self.pc + 1


	#============================================================
	#Loop entry ([ operator)
	#============================================================
	def loop_enter(self):

		#look and see if we are going into an infinite loop
		if self.instructions[self.pc+1] == ']':
			print "infinite loop detected (empty loop) at op {0}".format(self.pc)
			self.gtfo()

		#if it looks safe, store the address of the first op in the loop stack
		else:
			self.stack.append(self.pc+1) 
			self.pc = self.pc + 1


	#============================================================
	#Loop exit test (] operator)
	#============================================================
	def loop_end(self):

		#break the loop if the register pointed to by the data pointer is 0
		if self.reg[self.dp] == 0:

			self.pc = self.pc+1
			#if for some reason, like an extra ']' happens, catch the stack underflow
			try:
				self.stack.pop()
			except:
				print "loop stack underflow at instruction {0}, exiting".format(self.pc)
				self.gtfo()

			try:
				self.VerbosePrint("breaking loop, stack ptr val: {0}, pc: {1}, dp: {2}, reg: {3}".format(self.stack[-1],self.pc, self.dp, self.reg[self.dp]))
			except: 
				self.VerbosePrint("breaking loop, stack ptr val: {0}, pc: {1}, dp: {2}, reg: {3}".format('empty',self.pc, self.dp, self.reg[self.dp]))
		

		#the data poiner points to a register containing a value greater than zero, loop again
		else:

			#set the program counter back to the beginning of the loop
			self.VerbosePrint("looping, stack ptr val: {0}, pc: {1}, dp: {2}, reg: {3}".format(self.stack[-1],self.pc, self.dp, self.reg[self.dp]))
			self.pc = self.stack[-1]

	#============================================================
	#Single step an instruction
	#============================================================
	def step(self,data=None):


		self.PrintCore()

		if self.pc > self.instructioncount-1:
			print "exiting bc pc: ({0}) > program length: ({1})".format(self.pc,self.instructioncount)
			self.Terminator()
			return None

		else:
			inst = self.instructions[self.pc]
			self.VerbosePrint("step: executing " + inst)
			self.outdv = 0
			self.ops[inst]()

			#check to see if we are outputting data on this instruction
			return (self.outdv, self.outreg)

	#============================================================
	#Run
	#============================================================
	def Run(self,pgm,addr=0):
		pass

	#============================================================
	#Load a program
	#============================================================
	def Load(self,pgm):

		self.dp = 0
		self.reg = [0]
		self.pc = 0
		self.maxreg = len(self.reg)
		self.stack = []
		self.outreg = 0
		self.outdv = 0
		self.memoryused = 1

		#program info

		self.instructions = []
		self.instructioncount = 0
		for op in pgm:
			self.instructions.append(op)
		
		self.instructioncount = len(self.instructions)



	#============================================================
	#Program terminiation due to exception
	#============================================================
	def gtfo(self):
		self.pc = len(self.instructions)+1


	#************************************************************
	#Reporting Utility Functions
	#************************************************************
	def Terminator(self):
		print "program exited normally"


	def VerbosePrint(self,msg):

		if self.verbose == True:
			print msg

	def PrintPgmMemory(self):

		pgmstr = ''
		for n in self.instructions:
			pgmstr += n

		print "{0} bytes: ".format(self.instructioncount) , pgmstr
		

	def PrintRegisters(self):
		print 'registers: ', self.reg


	def PrintCore(self):		

		print """core info:\n\
		Data Pointer: 		{0} ({8})
		Program Counter: 	{1}
		Registers: 		{2}
		Loop Stack: 		{3}
		Output Register: 	{4}
		Input Register: 	{5}
		Program Size: 		{6}
		Memory Used: 		{7}
		"""\
		.format(\
		self.dp,\
		self.pc,\
		self.reg,\
		self.stack,\
		self.outreg,\
		self.inreg,\
		self.instructioncount,\
		self.memoryused,\
		self.reg[self.dp]\
		)

		#program info


	def PrintState(self):
		self.PrintCore()
		
		


