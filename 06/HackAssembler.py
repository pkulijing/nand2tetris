import re
import sys
class HackAssembler:
	"""
	Assembler for Hack computer in courser Nand to Tetris.
	Author: Jing LI
	Date: Sep 3, 2016
	"""
	destDict = {
		"A":"100",
		"D":"010",
		"M":"001", 
		"AD":"110",
		"AM":"101",
		"MD":"011",
		"AMD":"111"
	}
	def destPart(self, dest):
		if not dest:
			return "000"
		try:
			return self.destDict[dest]
		except KeyError:
			print "Wrong dest: " + dest

	compDictA = {
		"0":"101010",
		"1":"111111",
		"-1":"111010",
		"D":"001100",
		"A":"110000",
		"!D":"001101",
		"!A":"110001",
		"-D":"001111",
		"-A":"110011",
		"D+1":"011111",
		"A+1":"110111",
		"D-1":"001110",
		"A-1":"110010",
		"D+A":"000010",
		"D-A":"010011",
		"A-D":"000111",
		"D&A":"000000",
		"D|A":"010101"
	}
	compDictM = {
		"M":"110000",
		"!M":"110001",
		"-M":"110011",
		"M+1":"110111",
		"M-1":"110010",
		"D+M":"000010",
		"D-M":"010011",
		"M-D":"000111",
		"D&M":"000000",
		"D|M":"010101"
	}
	def compPart(self,comp):
		if not comp:
			raise Exception("No comp.")
		try:
			if 'M' in comp:
				return "1" + self.compDictM[comp]
			else:
				return "0" + self.compDictA[comp]
		except KeyError:
			raise Exception("Wrong comp: " + comp)

	jumpDict = {
		"JGT":"001",
		"JEQ":"010",
		"JLT":"100",
		"JGE":"011", 
		"JNE":"101", 
		"JLE":"110", 
		"JMP":"111"
	}
	def jumpPart(self, jump):
		if not jump:
			return "000"
		try:
			return self.jumpDict[jump]
		except KeyError:
			raise Exception("Wrong jump: " + jump)

	pValid = re.compile(r"(@?[\w=+\-();.!&|$]*)(?://.*)?$")
	pAInstNum = re.compile(r"@(\d+)")
	pAInstVar = re.compile(r"@([a-zA-Z_.$:][\w.$:]*)")
	pLInst = re.compile(r"\(([a-zA-Z_.$:][\w.$:]*)\)")
	pCInst = re.compile(r"(?:(?P<dest>[AMD]+)=)?(?P<comp>[01\-!ADM+|&]+)(?:;(?P<jump>[A-Z]+))?")
	pInputFileName = re.compile(r"([\w/.]+)[.]asm")
	pSpace = re.compile(r"\s+")
	def makeOutputName(self):
		matched = self.pInputFileName.match(self.inputName)
		if matched:
			return matched.group(1) + ".hack"
		return self.inputName + ".hack"
	def firstPass(self):
		lineno = 0
		with open(self.inputName, 'r') as fp:
			for line0 in fp:
				line = re.sub(self.pSpace, '', line0)
				valid = self.pValid.match(line)
				if valid:
					if len(valid.group(1)) == 0:
						continue
					isLInst = self.pLInst.match(valid.group(1))
					if isLInst:
						label = isLInst.group(1)
						if label not in self.symbolTable:
							self.symbolTable[label] = lineno
					else:
						lineno += 1
				else:
					raise Exception("Wrong line: " + line0) 
	def secondPass(self):
		with open(self.outputName, 'w') as outfp:
			with open(self.inputName, 'r') as infp:
				for line in infp:
					line = re.sub(self.pSpace, '', line)
					inst = self.pValid.match(line).group(1)
					if len(inst) != 0 and not self.pLInst.match(inst):
						outfp.write(self.binaryInst(inst) + "\n")

	def binaryInst(self, inst):
		isAInstNum = self.pAInstNum.match(inst)
		if isAInstNum:
			num = isAInstNum.group(1)
			res = format(int(num), "016b")
			if res[0] == '1' or len(res) > 16:
				raise Exception("Wrong line number " + num)
			return res
		isAInstVar = self.pAInstVar.match(inst)
		if isAInstVar:
			var = isAInstVar.group(1)
			if var not in self.symbolTable:
				self.symbolTable[var] = self.nextPos
				self.nextPos += 1
			return format(self.symbolTable[var], "016b")
		isCInst = self.pCInst.match(inst)
		if isCInst:
			return "111" + self.compPart(isCInst.group("comp")) + self.destPart(isCInst.group("dest")) + self.jumpPart(isCInst.group("jump"))
		raise Exception("No match for " + inst)

	def __init__(self, filename):
		self.symbolTable = {
			"SP":0,
			"LCL":1,
			"ARG":2,
			"THIS":3,
			"THAT":4,
			"SCREEN":16384,
			"KBD":24576,
			"R0":0,
			"R1":1,
			"R2":2,
			"R3":3,
			"R4":4,
			"R5":5,
			"R6":6,
			"R7":7,
			"R8":8,
			"R9":9,
			"R10":10,
			"R11":11,
			"R12":12,
			"R13":13,
			"R14":14,
			"R15":15
		}
		self.nextPos = 16
		self.inputName = filename
		self.outputName = self.makeOutputName()
		self.firstPass()
		self.secondPass()

filename = sys.argv[1]
assembler = HackAssembler(filename)


