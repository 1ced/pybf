

from bf import bf_core as BF


def BFRunner(coreinst, pgm):

	coreinst.Load(pgm)
	coreinst.PrintPgmMemory()
	retval = True

	while retval != None:
		retval = coreinst.step()
		coreinst.PrintRegisters()

def TestHeader(testno):
	print """
		************************************************
		******************* TEST {0} *********************
		************************************************ 
	""".format(testno)


#test incrementing and decrementing a register
#counts up to 5 and down to 1 in register 0
bfexe_IncDecTest = '+++++------'

#test incrementing and decrementing the data pointer
#increments register 0 to 3, increments register 1 to 4, 
#then bringst them both back to zero, then brings them both to 1
bfexe_DataPointerTest = '+++>++++<--->----<+>+'

#increment register 0 to 5 and store it in the output register
bfexe_OutputDataRegTest = '+++++.'

#import 3 from the import register into 3 different registers (0,1,2) 
bfexe_InputDataRegTest = ',>,>,'


#loop test program. basically the ']' operator is a branch if not zero
#this program loads two registers with numbers (R0 = 3, R1 = 4)
#the loop adds R0 and R1 by decrementing R0, R1 until they are zero
#each time R0 or R1 is decremented R2 is incremented, effectively adding R0 and R1
#this is exceptionally tedious. probably there is a slicker way to do it in a nested loop
bfexe_LoadR0R1 = '+++>++++<'
bfexe_LoopTest = bfexe_LoadR0R1 + '[->>+<<]>[->+<]'

#nested loop test (multiplier)
#load R0 = 3, R1 = 4
#R2 is a temporary copy register
#R3 will have the product of multiplying R0 and R1

#enter mul loop, use R0 as the test reg
#copy R1 to R2, use R1 as the test reg
#copy R2 to R1 and R3, use R2 as the test reg

#[> enter the main loop, point at R1
#[>+<-] increment dp, +R2, decrementdp, -R1, exit loop with dp == R1
#> enter the next loop on R2; always enter loops on the test register (?)
#[<+] decremnt dp to R1, inc R1, increment to R3, inc R3, dec dp to R2, dec R2, test R2==0, repeat, exit with dp == R2
#<<-] move dp to R0, dec R0, loop back to the beginning of the outer loop to inc dp to R1 and start again
bfexe_NestedLoopTest = bfexe_LoadR0R1 + '[>[>+<-]>[<+>>+<-]<<-]'

core = BF()

#Test the data operators
TestHeader(1) 
BFRunner(core,bfexe_IncDecTest)

#Test the data pointer operators
TestHeader(2) 
BFRunner(core,bfexe_DataPointerTest)

#Test printing one of the registers to the output register
TestHeader(3) 
BFRunner(core,bfexe_DataPointerTest)

#Test printing one of the registers to the output register
TestHeader(4) 
print "output register: {0}".format(core.outreg) #check to see what is in the output register
BFRunner(core,bfexe_OutputDataRegTest)
print "output register: {0}".format(core.outreg) #check to see if 5 was moved into the output register

#Test reading the input register
#import 3 from the import register into 3 different registers (0,1,2)
TestHeader(5) 
core.inreg = 3
print core.inreg #[put something in the input register]
BFRunner(core,bfexe_InputDataRegTest)

#test the [ and ] loop operators
#loop set register 0 to be the loop counter (loop exits when the register pointed to by the data pointer is 0)
TestHeader(6)
BFRunner(core,bfexe_LoopTest)

#test the [ and ] loop operators
#loop set register 0 to be the loop counter (loop exits when the register pointed to by the data pointer is 0)
TestHeader(7)
BFRunner(core,bfexe_NestedLoopTest)







