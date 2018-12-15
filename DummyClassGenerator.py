import sys
from clang.cindex import Config
from clang.cindex import TypeKind
from clang.cindex import CursorKind
from clang.cindex import Index
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

def getTypeString(typeIdx):
    if(typeIdx==0):
        return "char"
    elif(typeIdx==1):
        return "short"
    elif(typeIdx==2):
        return "int"
    elif(typeIdx==3):
        return "long"
    elif(typeIdx==4):
        return "unsigned char"
    elif(typeIdx==5):
        return "unsigned short"
    elif(typeIdx==6):
        return "unsigned int"
    elif(typeIdx==7):
        return "unsigned long"            
    elif(typeIdx==8):
        return "float"
    elif(typeIdx==9):
        return "double"
    else:
        return "void"

def getFunctionNames(functionIdx): # will replace by a dictionary
    return "testFunction" + str(functionIdx)

def getMemberNames(memberIdx): # will replace by a dictionary
    return "testMember" + str(memberIdx)

def getParameterName(parameterIdx): # will replace by a dictionary
    return "parameter" + str(parameterIdx)

class DummyParameterList:
    def __init__(self, count):
        self.paramsTypeIndices = []
        self.paramsNameIndices = []
        self.addRandomParameters(count)

    def addRandomParameters(self, count):
        for i in range(count):
            self.paramsTypeIndices.append(Random.randrange(0, 9))
            self.paramsNameIndices.append(Random.randrange(0, 100))
        return
    
    def addParameters(self, typeIdx):
        self.paramsTypeIndices.append(typeIdx)
        self.paramsNameIndices.append(Random.randrange(0, 100))
        return

    def generate(self):
        rval = ""
        for i in range(len(self.paramsTypeIndices)):
            if(not(i==0)):
                rval += ", "
            rval += getTypeString(self.paramsTypeIndices[i]) + " " + getParameterName(self.paramsNameIndices[i])
        return rval

class DummyCtor:
    def __init__(self, className, parentClassName):
        self.className = className
        self.parentClassName = parentClassName

    def generate_H(self, tabcount):
        return tab(tabcount) + self.className + "()"

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.className + "::" + self.className + "()" + "\n"
        rval += tab(tabcount) + ":" + self.parentClassName + "()" + "\n"
        rval += tab(tabcount) + "{" + "\n"
        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"
        return rval;

class DummyDtor:
    def __init__(self, className):
        self.className = className

    def generate_H(self, tabcount):
        return tab(tabcount) + "~" + self.className + "()"

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.className + "::" + "~" + self.className + "()" + "\n"
        rval += tab(tabcount) + "{" + "\n"
        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"
        return rval;

class DummyFunction:
    def __init__(
        self, className, access, isVirtual, functionTypeIdx, functionNameIdx, parameterList):
        self.className = className
        self.access = access
        self.isVirtual = isVirtual
        self.functionTypeIdx = functionTypeIdx
        self.functionNameIdx = functionNameIdx
        self.parameterList = parameterList

    def generate_H(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getVirtualString(self.isVirtual) + getTypeString(self.functionTypeIdx) + " " + getFunctionNames(self.functionNameIdx) + "(" + self.parameterList.generate() + ")"
        return rval

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getTypeString(self.functionTypeIdx) + " " + self.className + "::" + getFunctionNames(self.functionNameIdx) + "(" + self.parameterList.generate() + ")" + "\n"
        rval += tab(tabcount) + "{" + "\n"
        rval += tab(tabcount+1) + getTypeString(self.functionTypeIdx) + " rval;\n"
        rval += tab(tabcount+1) + "ShadaiMacro(" + str(self.functionNameIdx) + ")\n"
        rval += tab(tabcount+1) + "return rval;\n"
        rval += tab(tabcount) + "}" + "\n"
        rval += "\n"        
        return rval

class DummyMember:
    def __init__(self, className, access, memberTypeIdx, memberNameIdx):
        self.access = access
        self.memberTypeIdx = memberTypeIdx
        self.memberNameIdx = memberNameIdx

    def generate_H(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getTypeString(self.memberTypeIdx) + " " + getMemberNames(self.memberNameIdx)
        return rval

    def generate_CPP(self, tabcount):
        rval = ""
        return rval

class DummyClass:
    def __init__(self, namespace, className, parentClassName, privateFunctionCount, protectedFunctionCount, publicFunctionCount, virtualPrivateFunctionCount, virtualProtectedFunctionCount, virtualPublicFunctionCount, privateMemberCount, protectedMemberCount, publicMemberCount, ctorMaxParameterCount, functionMaxParameterCount):
        self.sourceCode = ""
        self.namespace = namespace
        self.className = className
        self.parentClassName = parentClassName
        self.functionNames = []
        self.memberNames = []

        #####################################################################
        # prepare dummyClasses
        self.ctor = DummyCtor(className, parentClassName)
        self.dtor = DummyDtor(className)

        self.dummyClassPrivateFunctions = []
        for i in range(virtualPrivateFunctionCount):
            self.dummyClassPrivateFunctions.append(DummyFunction(className, "private"  ,        "", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        for i in range(privateFunctionCount):
            self.dummyClassPrivateFunctions.append(DummyFunction(className, "private"  , "virtual", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.dummyClassProtectedFunctions = []
        for i in range(virtualProtectedFunctionCount):
            self.dummyClassProtectedFunctions.append(DummyFunction(className, "protected",        "", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        for i in range(protectedFunctionCount):
            self.dummyClassProtectedFunctions.append(DummyFunction(className, "protected", "virtual", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        self.dummyClassPublicFunctions = []
        for i in range(virtualPublicFunctionCount):
            self.dummyClassPublicFunctions.append(DummyFunction(className, "public"   ,        "", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        for i in range(publicFunctionCount):
            self.dummyClassPublicFunctions.append(DummyFunction(className, "public"   , "virtual", Random.randrange(0, 10), Random.randrange(0, 100), DummyParameterList(Random.randrange(0, functionMaxParameterCount)) ) )

        #####################################################################
        # # prepare dummyMembers
        self.dummyClassPrivateMembers = []
        for i in range(privateMemberCount):
            self.dummyClassPrivateMembers.append(DummyMember(className, "private"  , Random.randrange(0, 10), Random.randrange(0, 100) ) )

        self.dummyClassProtectedMembers = []
        for i in range(protectedMemberCount):
            self.dummyClassProtectedMembers.append(DummyMember(className, "protected", Random.randrange(0, 10), Random.randrange(0, 100) ) )

        self.dummyClassPublicMembers = []
        for i in range(publicMemberCount):
            self.dummyClassPublicMembers.append(DummyMember(className, "public"   , Random.randrange(0, 10), Random.randrange(0, 100) ) )

    def generateHeader(self, tabcount):
        rval = ""
        rval += tab(tabcount)  + "class " + self.className + "\n"
        rval += tab(tabcount) + "{\n"

        #######################################################################
        # constructor destructor are public
        rval += tab(tabcount) + getAccessString("public") + "\n"

        # generate constructor
        rval += self.ctor.generate_H(tabcount+1) + ";" + "\n"

        # generate destructopr
        rval += self.dtor.generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # public function
        rval += tab(tabcount) + getAccessString("public") + "\n"

        for i in range(len(self.dummyClassPublicFunctions)):
            rval += self.dummyClassPublicFunctions[i].generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # protected function
        rval += tab(tabcount) + getAccessString("protected") + "\n"
        for i in range(len(self.dummyClassProtectedFunctions)):
            rval += self.dummyClassProtectedFunctions[i].generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # private function
        rval += tab(tabcount) + getAccessString("private") + "\n"

        for i in range(len(self.dummyClassPrivateFunctions)):
            rval += self.dummyClassPrivateFunctions[i].generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # public member
        rval += tab(tabcount) + getAccessString("public") + "\n"

        for i in range(len(self.dummyClassPublicMembers)):
            rval += self.dummyClassPublicMembers[i].generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # protected member
        rval += tab(tabcount) + getAccessString("protected") + "\n"

        for i in range(len(self.dummyClassProtectedMembers)):
            rval += self.dummyClassProtectedMembers[i].generate_H(tabcount+1) + ";" + "\n"

        #######################################################################
        # private member
        rval += tab(tabcount) + getAccessString("private") + "\n"

        for i in range(len(self.dummyClassPrivateMembers)):
            rval += self.dummyClassPrivateMembers[i].generate_H(tabcount+1) + ";" + "\n"

        rval += tab(tabcount) + "};"
        rval += tab(tabcount) + "\n"
        return rval

    def generate_H(self, tabcount):
        rval = ""
        rval += tab(tabcount) + "#ifndef _" + self.className + "_h_" + "\n"
        rval += tab(tabcount) + "#define _" + self.className + "_h_" + "\n"
        rval += "\n"
        rval += tab(tabcount) + "namespace " + self.namespace + "\n"
        rval += tab(tabcount) + "{\n"

        rval += self.generateHeader(tabcount+1)

        rval += tab(tabcount) + "};"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "#endif // _" + self.className + "_h_\n"
        return rval

    def generateSource(self, tabcount):
        rval = ""

        # generate constructor
        rval += self.ctor.generate_CPP(tabcount) + "\n"

        # generate destructopr
        rval += self.dtor.generate_CPP(tabcount) + "\n"

        #######################################################################
        # public function
        for i in range(len(self.dummyClassPublicFunctions)):
            rval += self.dummyClassPublicFunctions[i].generate_CPP(tabcount) + "\n"

        #######################################################################
        # protected function
        for i in range(len(self.dummyClassProtectedFunctions)):
            rval += self.dummyClassProtectedFunctions[i].generate_CPP(tabcount) + "\n"

        #######################################################################
        # private function
        for i in range(len(self.dummyClassPrivateFunctions)):
            rval += self.dummyClassPrivateFunctions[i].generate_CPP(tabcount) + "\n"

        return rval

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + "#include \"" + self.className + ".h\"" + "\n"
        rval += tab(tabcount) + "#include \"ShadaiMacro.h\"\n"
        rval += tab(tabcount) + "using namespace " + self.namespace + ";" + "\n"
        rval += tab(tabcount) + "\n"
        rval += self.generateSource(tabcount)
        return rval

    def write_H(self, filename):
        file = open(filename, 'wt')
        self.sourceCode = self.generate_H(0)
        print(self.sourceCode)
        if(file):
            file.write(self.sourceCode)
            file.close()

    def write_CPP(self, filename):
        file = open(filename, 'wt')
        self.sourceCode = self.generate_CPP(0)
        print(self.sourceCode)
        if(file):
            file.write(self.sourceCode)
            file.close()            

# python DummyClassGenerator.py MyNameSpace MyClass MyParentClass 1 2 3 4 5 6 7 8 9 10 11 12
################################################################################################################################
def DummyClassGenerator():
    if(len(sys.argv)!=18):
        print('Usage: DummyClassGenerator namespace classname parentClassName privateFunctionCount protectedFunctionCount publicFunctionCount virtualPrivateFunctionCount virtualProtectedFunctionCount virtualPublicFunctionCount privateMemberCount protectedMemberCount publicMemberCount ctorMaxParameterCount functionMaxParameterCount')
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
    privateMemberCount = int(sys.argv[10])
    protectedMemberCount = int(sys.argv[11])
    publicMemberCount  = int(sys.argv[12])
    ctorMaxParameterCount = int(sys.argv[13])
    functionMaxParameterCount  = int(sys.argv[14])

    output_h_path = classname + ".h"
    output_cpp_path = classname + ".cpp"

    dummyClass = DummyClass(namespace, classname, parentClassname, privateFunctionCount, protectedFunctionCount, publicFunctionCount, virtualPrivateFunctionCount, virtualProtectedFunctionCount, virtualPublicFunctionCount, privateMemberCount, protectedMemberCount, publicMemberCount, ctorMaxParameterCount, functionMaxParameterCount)
    dummyClass.write_H(output_h_path)
    dummyClass.write_CPP(output_cpp_path)

DummyClassGenerator()