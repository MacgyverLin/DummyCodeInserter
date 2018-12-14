import sys
from clang.cindex import Config
from clang.cindex import TypeKind
from clang.cindex import CursorKind
from clang.cindex import Index
import random as Random

################################################################################################################################
class DummyClass:
    def __init__(self, outputpath, namespace, classname, parent_classname, private_function_count, protected_function_count, public_function_count, private_member_count, protected_member_count, public_member_count, virtual_private_function_count, virtual_protected_function_count, virtual_public_function_count):
        self.sourceCode = ""
        self.outputpath = outputpath
        self.namespace = namespace
        self.classname = classname
        self.parent_classname = parent_classname
        self.private_function_count = private_function_count
        self.protected_function_count = protected_function_count
        self.public_function_count = public_function_count
        self.private_member_count = private_member_count
        self.protected_member_count = protected_member_count
        self.public_member_count = public_member_count
        self.virtual_private_function_count = virtual_private_function_count
        self.virtual_protected_function_count = virtual_protected_function_count
        self.virtual_public_function_count = virtual_public_function_count
        self.maxCtorParametersCount = 3
        self.maxMemberParametersCount = 6
        self.functionNames = []
        self.memberNames = []

        for i in range(100):
            self.functionNames.append("testFunction" + str(i))

        for i in range(100):
            self.memberNames.append("testMember" + str(i))

    def tab(self, count):
        str = ""
        for i in range(0, count):
            str += "\t"
        return str

    def generateAccess(self, access):
        if(access=="public"):
            return access + ":"
        elif(access=="protected"):
            return access + ":"
        elif(access=="private"):
            return access + ":"                        
        else:
            return ""

    def generateVirtual(self, isVirtual):
        if(isVirtual=="virtual"):
            return "virtual "
        else:
            return ""

    def generateParameter(self, maxParametersCount):
        return "()"

    def generateType(self, typeIdx):
        if(typeIdx==0):
            return "void"
        elif(typeIdx==1):
            return "char"
        elif(typeIdx==2):
            return "short"
        elif(typeIdx==3):
            return "int"
        elif(typeIdx==4):
            return "long"
        elif(typeIdx==5):
            return "unsigned char"
        elif(typeIdx==6):
            return "unsigned short"
        elif(typeIdx==7):
            return "unsigned int"
        elif(typeIdx==8):
            return "unsigned long"            
        elif(typeIdx==9):
            return "float"
        elif(typeIdx==10):
            return "double"            
        else:
            return "void"

    def getunctionNames(self, functionIdx):
        return self.functionNames[functionIdx]

    def getMemberNames(self, memberIdx):
        return self.memberNames[memberIdx]        

    def generateConstructor(self, tabcount, maxParametersCount):
        return self.tab(tabcount) + self.classname + self.generateParameter(maxParametersCount)

    def generateDestructor(self, tabcount):
        return self.tab(tabcount) + "~" + self.classname + "()"

    def generateMemberFunction(self, tabcount, isVirtual, typeIdx, functionIdx, maxParametersCount):
        str = ""
        str += self.tab(tabcount) + self.generateVirtual(isVirtual) + self.generateType(typeIdx) + " " + self.getunctionNames(functionIdx) + self.generateParameter(maxParametersCount)
        return str

    def generateMember(self, tabcount, typeIdx, memberIdx):
        str =""
        str += self.tab(tabcount) + self.generateType(typeIdx) + " " + self.getMemberNames(memberIdx)
        return str

    def generateHeaderContent(self, tabcount):
        #######################################################################
        # count total function
        totalFunctionCount = self.private_function_count + self.virtual_private_function_count
        totalFunctionCount += self.protected_function_count + self.virtual_protected_function_count
        totalFunctionCount += self.public_function_count + self.virtual_public_function_count
        # count total member
        totalMemberCount = self.private_member_count
        totalMemberCount += self.protected_member_count
        totalMemberCount += self.public_member_count

        print(totalFunctionCount)
        print(totalMemberCount)

        #######################################################################
        str = ""
        functionIdx = 0;
        memberIdx = 0;

        #######################################################################
        # constructor destructor are public
        str += self.tab(tabcount) + self.generateAccess("public") + "\n"

        # generate constructor
        str += self.generateConstructor(tabcount+1, self.maxCtorParametersCount) + ";" + "\n"
        
        # generate destructopr
        str += self.generateDestructor(tabcount+1) + ";" + "\n"

        #######################################################################
        # private member
        str += self.tab(tabcount) + self.generateAccess("private") + "\n"
        for i in range(self.private_function_count):
            str += self.generateMemberFunction(tabcount+1, ""       , Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.virtual_private_function_count):
            str += self.generateMemberFunction(tabcount+1, "virtual", Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.private_member_count):
            str += self.generateMember        (tabcount+1           , Random.randrange(0, 10), memberIdx                               ) + ";" + "\n"
            memberIdx += 1

        #######################################################################
        # protected member
        str += self.tab(tabcount) + self.generateAccess("protected") + "\n"
        for i in range(self.protected_function_count):
            str += self.generateMemberFunction(tabcount+1, ""       , Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.virtual_protected_function_count):
            str += self.generateMemberFunction(tabcount+1, "virtual", Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.protected_member_count):
            str += self.generateMember        (tabcount+1,            Random.randrange(0, 10), memberIdx) + ";" + "\n"
            memberIdx += 1

        #######################################################################
        # public member
        str += self.tab(tabcount) + self.generateAccess("public") + "\n"
        for i in range(self.public_function_count):
            str += self.generateMemberFunction(tabcount+1, ""       , Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.virtual_public_function_count):
            str += self.generateMemberFunction(tabcount+1, "virtual", Random.randrange(0, 10), functionIdx, self.maxMemberParametersCount) + ";" + "\n"
            functionIdx += 1

        for i in range(self.public_member_count):
            str += self.generateMember        (tabcount+1,            Random.randrange(0, 10), memberIdx) + ";" + "\n"
            memberIdx += 1

        return str

    def generateHeader(self, tabcount):
        str = ""
        str += self.tab(tabcount)  + "class " + self.classname + "\n"
        str += self.tab(tabcount) + "{\n"
        str += self.generateHeaderContent(tabcount)
        str += self.tab(tabcount) + "};"
        str += self.tab(tabcount) + "\n"
        return str

    def generateHeaderFile(self, tabcount):
        str = ""
        str += self.tab(tabcount) + "namespace " + self.namespace + "\n";
        str += self.tab(tabcount) + "{\n"
        str += self.generateHeader(tabcount+1)
        str += self.tab(tabcount) + "};"
        str += self.tab(tabcount) + "\n"
        return str

    def write(self, filename):
        file = open(filename, 'wt')
        self.sourceCode = self.generateHeaderFile(0)
        print(self.sourceCode)
        if(file):
            file.write(self.sourceCode)
            file.close()

################################################################################################################################
def DummyClassGenerator():
    if(len(sys.argv)!=17):
        print('Usage: DummyClassGenerator outputPath namespace classname parent_classname private_function_count protected_function_count public_function_count private_member_count protected_member_count public_member_count virtual_private_function_count virtual_protected_function_count virtual_public_function_count')
        return

    outputpath = sys.argv[1]
    namespace = sys.argv[2]
    classname = sys.argv[3]
    parent_classname = sys.argv[4]
    private_function_count = int(sys.argv[5])
    protected_function_count = int(sys.argv[6])
    public_function_count = int(sys.argv[7])
    private_member_count = int(sys.argv[8])
    protected_member_count = int(sys.argv[9])
    public_member_count  = int(sys.argv[10])
    virtual_private_function_count = int(sys.argv[11])
    virtual_protected_function_count = int(sys.argv[12])
    virtual_public_function_count = int(sys.argv[13])

    dummyClass = DummyClass(outputpath, namespace, classname, parent_classname, private_function_count, protected_function_count, public_function_count, private_member_count, protected_member_count, public_member_count, virtual_private_function_count, virtual_protected_function_count, virtual_public_function_count)
    dummyClass.write("1.cpp")

DummyClassGenerator()