import sys
from enum import Enum
import random as Random

################################################################################################################################
def tab(count):
    rval = ""
    for i in range(0, count):
        rval += "\t"
    return rval

def getAccessString(access):
    if(access=="public"):
        return access + ":"
    elif(access=="protected"):
        return access + ":"
    elif(access=="private"):
        return access + ":"                        
    else:
        return ""

def getVirtualString(isVirtual):
    if(isVirtual=="virtual"):
        return "virtual "
    else:
        return ""

functionCount = 0
def getNextFunctionName(): # will replace by a dictionary
    global functionCount
    functionCount += 1
    return "func" + str(functionCount)

variableCount = 0
def getNextVariableName(): # will replace by a dictionary
    global variableCount
    variableCount += 1
    return "m_var" + str(variableCount)

parameterCount = 0
def getNextParameterName(): # will replace by a dictionary
    global parameterCount
    parameterCount += 1
    return "p" + str(parameterCount)

macroCount = 0
def getNextMacroName():
    global macroCount
    macroCount += 1
    return "DummyMacro" + str(macroCount)

################################################################################################################################
class CPPType:
    def __init__(self, typeIdx):
        self.typeIdx = typeIdx

    def generate(self):
        if(self.typeIdx==0):
            return "char"
        elif(self.typeIdx==1):
            return "short"
        elif(self.typeIdx==2):
            return "int"
        elif(self.typeIdx==3):
            return "long"
        elif(self.typeIdx==4):
            return "unsigned char"
        elif(self.typeIdx==5):
            return "unsigned short"
        elif(self.typeIdx==6):
            return "unsigned int"
        elif(self.typeIdx==7):
            return "unsigned long"            
        elif(self.typeIdx==8):
            return "float"
        elif(self.typeIdx==9):
            return "double"
        else:
            return "void"
    
    def isVoid(self):
        return self.typeIdx>9;

class CPPParameterList:
    def __init__(self, count):
        self.paramsTypes = []
        self.addRandomParameters(count)

    def addRandomParameters(self, count):
        for i in range(count):
            self.paramsTypes.append(CPPType(Random.randrange(0, 9)))
    
    def addParameters(self, typeIdx):
        self.paramsTypes.append(CPPType(typeIdx))

    def generate(self):
        rval = ""
        for i in range(len(self.paramsTypes)):
            if(not(i==0)):
                rval += ", "
            rval += self.paramsTypes[i].generate() + " " + getNextParameterName()
        return rval

class CPPCtor:
    def __init__(self, className, parentClassName):
        self.className = className
        self.parentClassName = parentClassName

    def generateHeader(self, tabcount):
        return tab(tabcount) + self.className + "()"

    def generateCPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.className + "::" + self.className + "()" + "\n"
        rval += tab(tabcount) + ": " + self.parentClassName + "()" + "\n"
        rval += tab(tabcount) + "{" + "\n"

        rval += "\n"
        rval += tab(tabcount+1) + getNextMacroName() + "()\n"
        rval += "\n"

        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"
        return rval;

class CPPDtor:
    def __init__(self, className):
        self.className = className

    def generateHeader(self, tabcount):
        return tab(tabcount) + "~" + self.className + "()"

    def generateCPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.className + "::" + "~" + self.className + "()" + "\n"
        rval += tab(tabcount) + "{" + "\n"

        rval += "\n"
        rval += tab(tabcount+1) + getNextMacroName() + "()\n"
        rval += "\n"

        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"
        return rval;

class CPPFunction:
    def __init__(
        self, className, access, isVirtual, functionType, parameterList):
        self.className = className
        self.access = access
        self.isVirtual = isVirtual
        self.functionType = functionType
        self.parameterList = parameterList

    def generateHeader(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getVirtualString(self.isVirtual) + self.functionType.generate() + " " + getNextFunctionName() + "(" + self.parameterList.generate() + ")"
        return rval

    def generateCPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.functionType.generate() + " " + self.className + "::" + getNextFunctionName() + "(" + self.parameterList.generate() + ")" + "\n"
        rval += tab(tabcount) + "{" + "\n"

        if(not self.functionType.isVoid()): # except void, the function has return value
            rval += tab(tabcount+1) + self.functionType.generate() + " rval;\n"
        
        rval += "\n"
        rval += tab(tabcount+1) + getNextMacroName() + "()\n"
        rval += "\n"

        if(not self.functionType.isVoid()): # except void, the function has return value
            rval += tab(tabcount+1) + "return rval;\n"
        
        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"
        return rval

class CPPVariable:
    def __init__(self, className, access, variableType):
        self.access = access
        self.variableType = variableType

    def generateHeader(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.variableType.generate()  + " " + getNextVariableName()
        return rval

    def generateCPP(self, tabcount):
        rval = ""
        return rval

class CPPClass:
    def __init__(self, namespace, className, parentClassName, privateFunctionCount, protectedFunctionCount, publicFunctionCount, virtualPrivateFunctionCount, virtualProtectedFunctionCount, virtualPublicFunctionCount, privateVariableCount, protectedVariableCount, publicVariableCount, ctorMaxParameterCount, functionMaxParameterCount):
        self.sourceCode = ""
        self.namespace = namespace
        self.className = className
        self.parentClassName = parentClassName

        #####################################################################
        # prepare functions
        self.ctor = CPPCtor(className, parentClassName)

        self.dtor = CPPDtor(className)

        self.privateFunctions = []
        for i in range(privateFunctionCount):
            self.privateFunctions.append(CPPFunction(className, "private"  ,        "", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.virtualPrivateFunctions = []
        for i in range(virtualPrivateFunctionCount):
            self.virtualPrivateFunctions.append(CPPFunction(className, "private"  , "virtual", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.protectedFunctions = []
        for i in range(protectedFunctionCount):
            self.protectedFunctions.append(CPPFunction(className, "protected",        "", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.virtualProtectedFunctions = []
        for i in range(virtualProtectedFunctionCount):
            self.virtualProtectedFunctions.append(CPPFunction(className, "protected", "virtual", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.publicFunctions = []
        for i in range(publicFunctionCount):
            self.publicFunctions.append(CPPFunction(className, "public"   ,        "", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.virtualPublicFunctions = []
        for i in range(virtualPublicFunctionCount):
            self.virtualPublicFunctions.append(CPPFunction(className, "public"   , "virtual", CPPType(Random.randrange(0, 10)), CPPParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        #####################################################################
        # prepare CPPMembers
        self.privateVariables = []
        for i in range(privateVariableCount):
            self.privateVariables.append(CPPVariable(className, "private"  , CPPType(Random.randrange(0, 10)) ) )

        self.protectedVariables = []
        for i in range(protectedVariableCount):
            self.protectedVariables.append(CPPVariable(className, "protected", CPPType(Random.randrange(0, 10)) ) )

        self.publicVariables = []
        for i in range(publicVariableCount):
            self.publicVariables.append(CPPVariable(className, "public"   , CPPType(Random.randrange(0, 10)) ) )

    def generateHeaderBody(self, tabcount):
        rval = ""

        if(not self.parentClassName==""):
            rval += tab(tabcount)  + "class " + self.className + " : public " + self.parentClassName + "\n"
        else:
            rval += tab(tabcount)  + "class " + self.className + "\n"

        rval += tab(tabcount) + "{\n"

        #######################################################################
        # constructor destructor are public
        rval += tab(tabcount) + getAccessString("public") + "\n"

        # generate constructor
        rval += self.ctor.generateHeader(tabcount+1) + ";" + "\n"

        # generate destructopr
        rval += self.dtor.generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # public function
        rval += tab(tabcount) + getAccessString("public") + "\n"

        for i in range(len(self.publicFunctions)):
            rval += self.publicFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        for i in range(len(self.virtualPublicFunctions)):
            rval += self.virtualPublicFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # protected function
        rval += tab(tabcount) + getAccessString("protected") + "\n"

        for i in range(len(self.protectedFunctions)):
            rval += self.protectedFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        for i in range(len(self.virtualProtectedFunctions)):
            rval += self.virtualProtectedFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # private function
        rval += tab(tabcount) + getAccessString("private") + "\n"

        for i in range(len(self.privateFunctions)):
            rval += self.privateFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        for i in range(len(self.virtualPrivateFunctions)):
            rval += self.virtualPrivateFunctions[i].generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # public member
        rval += tab(tabcount) + getAccessString("public") + "\n"

        for i in range(len(self.publicVariables)):
            rval += self.publicVariables[i].generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # protected member
        rval += tab(tabcount) + getAccessString("protected") + "\n"

        for i in range(len(self.protectedVariables)):
            rval += self.protectedVariables[i].generateHeader(tabcount+1) + ";" + "\n"

        #######################################################################
        # private member
        rval += tab(tabcount) + getAccessString("private") + "\n"

        for i in range(len(self.privateVariables)):
            rval += self.privateVariables[i].generateHeader(tabcount+1) + ";" + "\n"

        rval += tab(tabcount) + "};"
        rval += tab(tabcount) + "\n"
        return rval

    def generateHeader(self, tabcount):
        rval = ""
        rval += tab(tabcount) + "#ifndef _" + self.className + "_h_" + "\n"
        rval += tab(tabcount) + "#define _" + self.className + "_h_" + "\n"
        rval += "\n"
        rval += tab(tabcount) + "#include \"" + self.parentClassName + ".h\"" + "\n"
        rval += "\n"
        rval += tab(tabcount) + "namespace " + self.namespace + "\n"
        rval += tab(tabcount) + "{\n"

        rval += self.generateHeaderBody(tabcount+1)

        rval += tab(tabcount) + "};"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "#endif // _" + self.className + "_h_\n"
        return rval

    def generateCPPBody(self, tabcount):
        rval = ""

        # generate constructor
        rval += self.ctor.generateCPP(tabcount) + "\n"

        # generate destructopr
        rval += self.dtor.generateCPP(tabcount) + "\n"

        #######################################################################
        # public function
        for i in range(len(self.publicFunctions)):
            rval += self.publicFunctions[i].generateCPP(tabcount) + "\n"

        for i in range(len(self.virtualPublicFunctions)):
            rval += self.virtualPublicFunctions[i].generateCPP(tabcount) + "\n"

        #######################################################################
        # protected function
        for i in range(len(self.protectedFunctions)):
            rval += self.protectedFunctions[i].generateCPP(tabcount) + "\n"

        for i in range(len(self.virtualProtectedFunctions)):
            rval += self.virtualProtectedFunctions[i].generateCPP(tabcount) + "\n"

        #######################################################################
        # private function
        for i in range(len(self.privateFunctions)):
            rval += self.privateFunctions[i].generateCPP(tabcount) + "\n"

        for i in range(len(self.virtualPrivateFunctions)):
            rval += self.virtualPrivateFunctions[i].generateCPP(tabcount) + "\n"

        return rval

    def generateCPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + "#include \"" + self.className + ".h\"" + "\n"
        rval += tab(tabcount) + "#include \"DummyMacro.h\"\n"
        rval += tab(tabcount) + "using namespace " + self.namespace + ";" + "\n"
        rval += tab(tabcount) + "\n"
        rval += self.generateCPPBody(tabcount)
        return rval

    def writeHeader(self, filename):
        file = open(filename, 'wt')
        self.sourceCode = self.generateHeader(0)
        print(self.sourceCode)
        if(file):
            file.write(self.sourceCode)
            file.close()

    def writeCPP(self, filename):
        file = open(filename, 'wt')
        self.sourceCode = self.generateCPP(0)
        print(self.sourceCode)
        if(file):
            file.write(self.sourceCode)
            file.close()            

# python CPPClassGenerator.py Magnum SoundController Controller 1 2 3 4 5 6 7 8 9 30 40
################################################################################################################################
def CPPClassGenerator():
    if(len(sys.argv)!=15):
        print('Usage: CPPClassGenerator namespace classname parentClassName privateFunctionCount protectedFunctionCount publicFunctionCount virtualPrivateFunctionCount virtualProtectedFunctionCount virtualPublicFunctionCount privateVariableCount protectedVariableCount publicVariableCount ctorMaxParameterCount functionMaxParameterCount')
        return

    namespace = sys.argv[1]
    classname = sys.argv[2]
    parentClassname = sys.argv[3]
    privateFunctionCount = int(sys.argv[4])
    protectedFunctionCount = int(sys.argv[5])
    publicFunctionCount = int(sys.argv[6])
    virtualPrivateFunctionCount = int(sys.argv[7])
    virtualProtectedFunctionCount = int(sys.argv[8])
    virtualPublicFunctionCount = int(sys.argv[9])
    privateVariableCount = int(sys.argv[10])
    protectedVariableCount = int(sys.argv[11])
    publicVariableCount  = int(sys.argv[12])
    ctorMaxParameterCount = int(sys.argv[13])
    functionMaxParameterCount  = int(sys.argv[14])

    output_h_path = classname + ".h"
    output_cpp_path = classname + ".cpp"

    cppClass = CPPClass(namespace, classname, parentClassname, privateFunctionCount, protectedFunctionCount, publicFunctionCount, virtualPrivateFunctionCount, virtualProtectedFunctionCount, virtualPublicFunctionCount, privateVariableCount, protectedVariableCount, publicVariableCount, ctorMaxParameterCount, functionMaxParameterCount)
    cppClass.writeHeader(output_h_path)
    cppClass.writeCPP(output_cpp_path)

CPPClassGenerator()