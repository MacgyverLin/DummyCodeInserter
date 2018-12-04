#include "1.h"

A::A(){}

A::A(char* name){}

A::~A(){
}

void A::test1(){}

bool A::test1(int a)
{
	return true;
}

short A::test2(int b)
{
	return 3 + b;
}

int A::test3(int c)
{
	return 1 + c;
}

long A::test4(int d)
{
	return 2 + d;
}

float A::test5(int e)
{
	// asdasd
    {
	    int a = 1;
        this->test2(1);
    }
    return 1.0 + e;
}

double A::test6(int f)
{
	return 2.0;
}