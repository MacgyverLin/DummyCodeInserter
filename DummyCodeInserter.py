import sys
from clang.cindex import Config
from clang.cindex import TypeKind
from clang.cindex import CursorKind
from clang.cindex import Index
import random as Random


class CPPAnalyzer:
    def __init__(self):
        libclangPath = "libclang.dll"
        if Config.loaded == True:
            pass
        else:
            Config.set_library_file(libclangPath)

    # open a file and print AST Node recursively
    def dumpFile(self, filename, tab=""):
        index = Index.create()
        tu = index.parse(filename)  # parse AST tree, get translation unit tu

        self.printCursor(tu.cursor, tab)  # print AST tree recursively from root(tu.cursor)

    # print AST Node recursively
    def printCursor(self, cursor, tab=""):
        print('%sFound %s, cursor.type=%s kind=%s, location=%s]' % (
        tab, cursor.spelling, cursor.type.kind, cursor.kind, cursor.location));

        for child in cursor.get_children():
            self.printCursor(child, tab + "\t")

    def printCursorInfo(self, cursor):
        print('Found %s, location=%s, %s, %s]' % (
        cursor.spelling, cursor.location.file.name, cursor.location.line, cursor.location.column));

    # visit AST Node recursively
    def visit(self, parent, visitorCB):
        visitorCB(parent)

        # Recurse for children of this node
        for child in parent.get_children():
            self.visit(child, visitorCB)

            # visit AST Node recursively, only return FUNCTIONPROTO with CXX_METHOD, CONSTRUCTOR, DESTRUCTOR

    def findMethods(self, parent, methods):
        if (parent.type.kind == TypeKind.FUNCTIONPROTO and
                (
                        parent.kind == CursorKind.CXX_METHOD or parent.kind == CursorKind.CONSTRUCTOR or parent.kind == CursorKind.DESTRUCTOR or parent.kind == CursorKind.FUNCTION_DECL)):
            methods.append(parent)

        for child in parent.get_children():
            self.findMethods(child, methods)

    # visit AST Node recursively, only return COMPOUND_STMT
    def findCompoundStatements(self, parent, compoundStatements, count, maxStatementInsertPerFunction):
        if (parent.kind == CursorKind.COMPOUND_STMT):
            count += 1
            if (count > maxStatementInsertPerFunction):
                return
            compoundStatements.append(parent)

        for child in parent.get_children():
            self.findCompoundStatements(child, compoundStatements, count, maxStatementInsertPerFunction)

    # open a file, first find methods, and the find statement inside methods
    def findCompoundStatementsInMethod(self, filename, compoundStatements, maxStatementInsertPerFunction):
        index = Index.create()
        tu = index.parse(filename)

        methods = []
        self.findMethods(tu.cursor, methods)
        for method in methods:
            count = 0
            self.findCompoundStatements(method, compoundStatements, count, maxStatementInsertPerFunction)


class CPPFile:
    # Constructor init a CPP file, load it in self.lines
    def __init__(self, filename):
        file = open(filename, 'rt')
        if (file):
            self.lines = file.readlines()
            self.filename = filename
            file.close()

    # For all compound statement,
    # use the line, column information to add a comment
    def insertMacroAfterCompoundStatements(self, compoundStatements, macro, maxDummySelectionCount, maxInsertFunction):
        dummySelectionCount = 4

        # count = len(compoundStatements)-1;
        # if(maxInsertFunction!=-1 and count>maxInsertFunction):
        #     count = maxInsertFunction
        count = 0
        for i in range(len(compoundStatements)):
            idx = i
            # if(i<=count):
            #     idx = i
            # else:
            #     break;

            location = compoundStatements[idx].location
            if (location.file.name == self.filename):
                count +=1
                if(count>maxInsertFunction and maxInsertFunction!=-1):
                    break;

                themacro = macro
                themacro += "("
                for i in range(0, dummySelectionCount):
                    if (i != 0):
                        themacro += ", "
                    themacro += str(Random.randrange(0, maxDummySelectionCount - 1))
                themacro += ")"

                line = self.lines[location.line - 1]
                self.lines[location.line - 1] = line[:location.column] + '\n\t' + themacro + '\n' + line[
                                                                                                    location.column:]

    def insertTextAtBeginning(self, comment):
        self.lines.insert(0, comment)

    def write(self, filename):
        file = open(filename, 'wt')
        if (file):
            file.writelines(self.lines)
            file.close()


def DummyCodeInserter():
    if (len(sys.argv) != 6):
        print("Usage: DummyCodeInserter inputPath outputPath totalDummyFunctionCount maxStatementInsertPerFunction maxFuntionInsert")
        print("argv nums need 5,now is:%s" %len(sys.argv));
        return

    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    totalDummyFunctionCount = int(sys.argv[3])
    maxStatementInsertPerFunction = int(sys.argv[4])
    maxInsertFunction = int(sys.argv[5])

    cppAnalyzer = CPPAnalyzer()
    # cppAnalyzer.dumpFile(sys.argv[1])

    compoundStatements = []
    cppAnalyzer.findCompoundStatementsInMethod(infilename, compoundStatements, maxStatementInsertPerFunction)
    # for compoundStatement in compoundStatements:
    #    cppAnalyzer.printCursorInfo(compoundStatement)

    cppFile = CPPFile(infilename)
    cppFile.insertMacroAfterCompoundStatements(compoundStatements, 'SHANDAI_MACRO', totalDummyFunctionCount,maxInsertFunction)
    cppFile.insertTextAtBeginning('#include "ShanDaiMacro.h"\n')
    cppFile.write(outfilename)


DummyCodeInserter()