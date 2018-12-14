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

def getFunctionNames(functionIdx):
    return "testFunction" + str(functionIdx)

def getMemberNames(memberIdx):
    return "testMember" + str(memberIdx)

class DummyCtor:
    def __init__(self, className):
        self.className = className

    def generate_H(self, tabcount):
        return tab(tabcount) + self.className + "()"

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + self.className + "::" + self.className + "()" + "\n"
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
    def __init__(self, className, access, isVirtual, functionTypeIdx, functionNameIdx, parametersTypeIdx, parametersNameIdx):
        self.className = className
        self.access = access
        self.isVirtual = isVirtual
        self.functionTypeIdx = functionTypeIdx
        self.functionNameIdx = functionNameIdx
        self.parametersTypeIdx = parametersTypeIdx
        self.parametersNameIdx = parametersNameIdx

    def generate_H(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getVirtualString(self.isVirtual) + getTypeString(self.functionTypeIdx) + " " + getFunctionNames(self.functionNameIdx) + "()"
        return rval

    def generate_CPP(self, tabcount):
        rval = ""
        rval += tab(tabcount) + getTypeString(self.functionTypeIdx) + " " + self.className + "::" + getFunctionNames(self.functionNameIdx) + "()" + "\n"
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
        rval =""
        rval += tab(tabcount) + getTypeString(self.memberTypeIdx) + " " + getMemberNames(self.memberNameIdx)
        return rval

    def generate_CPP(self, tabcount):
        rval =""
        return rval

class DummyClass:
    def __init__(self, namespace, classname, parent_classname, private_function_count, protected_function_count, public_function_count, virtual_private_function_count, virtual_protected_function_count, virtual_public_function_count, private_member_count, protected_member_count, public_member_count):
        self.sourceCode = ""
        self.namespace = namespace
        self.classname = classname
        self.parent_classname = parent_classname
        self.functionNames = []
        self.memberNames = []

        #####################################################################
        # prepare dummyClasses
        self.ctor = DummyCtor(classname)
        self.dtor = DummyDtor(classname)

        self.dummyClassPrivateFunctions = []
        for i in range(virtual_private_function_count):
            self.dummyClassPrivateFunctions.append(DummyFunction(classname, "private"  ,        "", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        for i in range(private_function_count):
            self.dummyClassPrivateFunctions.append(DummyFunction(classname, "private"  , "virtual", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        self.dummyClassProtectedFunctions = []
        for i in range(virtual_protected_function_count):
            self.dummyClassProtectedFunctions.append(DummyFunction(classname, "protected",        "", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        for i in range(protected_function_count):
            self.dummyClassProtectedFunctions.append(DummyFunction(classname, "protected", "virtual", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        self.dummyClassPublicFunctions = []
        for i in range(virtual_public_function_count):
            self.dummyClassPublicFunctions.append(DummyFunction(classname, "public"   ,        "", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        for i in range(public_function_count):
            self.dummyClassPublicFunctions.append(DummyFunction(classname, "public"   , "virtual", Random.randrange(0, 10), Random.randrange(0, 100), Random.randrange(0, 10) , Random.randrange(0, 100) ) )

        #####################################################################
        # # prepare dummyMembers
        self.dummyClassPrivateMembers = []
        for i in range(private_member_count):
            self.dummyClassPrivateMembers.append(DummyMember(classname, "private"  , Random.randrange(0, 10), Random.randrange(0, 100) ) )

        self.dummyClassProtectedMembers = []
        for i in range(protected_member_count):
            self.dummyClassProtectedMembers.append(DummyMember(classname, "protected", Random.randrange(0, 10), Random.randrange(0, 100) ) )

        self.dummyClassPublicMembers = []
        for i in range(public_member_count):
            self.dummyClassPublicMembers.append(DummyMember(classname, "public"   , Random.randrange(0, 10), Random.randrange(0, 100) ) )

    def generateHeader(self, tabcount):
        rval = ""
        rval += tab(tabcount)  + "class " + self.classname + "\n"
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
        rval += tab(tabcount) + "#ifndef _" + self.classname + "_h_" + "\n"
        rval += tab(tabcount) + "#define _" + self.classname + "_h_" + "\n"
        rval += "\n"
        rval += tab(tabcount) + "namespace " + self.namespace + "\n"
        rval += tab(tabcount) + "{\n"

        rval += self.generateHeader(tabcount+1)

        rval += tab(tabcount) + "};"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "\n"
        rval += tab(tabcount) + "#endif // _" + self.classname + "_h_\n"
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
        rval += tab(tabcount) + "#include \"" + self.classname + ".h\"" + "\n"
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
    if(len(sys.argv)!=16):
        print('Usage: DummyClassGenerator namespace classname parent_classname private_function_count protected_function_count public_function_count virtual_private_function_count virtual_protected_function_count virtual_public_function_count private_member_count protected_member_count public_member_count')
        return

    namespace = sys.argv[1]
    classname = sys.argv[2]
    parent_classname = sys.argv[3]
    private_function_count = int(sys.argv[4])
    protected_function_count = int(sys.argv[5])
    public_function_count = int(sys.argv[6])
    virtual_private_function_count = int(sys.argv[7])
    virtual_protected_function_count = int(sys.argv[8])
    virtual_public_function_count = int(sys.argv[9])
    private_member_count = int(sys.argv[10])
    protected_member_count = int(sys.argv[11])
    public_member_count  = int(sys.argv[12])

    output_h_path = classname + ".h"
    output_cpp_path = classname + ".cpp"

    dummyClass = DummyClass(namespace, classname, parent_classname, private_function_count, protected_function_count, public_function_count, virtual_private_function_count, virtual_protected_function_count, virtual_public_function_count, private_member_count, protected_member_count, public_member_count)
    dummyClass.write_H(output_h_path)
    dummyClass.write_CPP(output_cpp_path)

DummyClassGenerator()