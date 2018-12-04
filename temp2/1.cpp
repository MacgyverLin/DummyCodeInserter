#include "ShanDaiMacro.h"
#include "1.h"

A::A(){
	SHANDAI(5, 5, 0, 4)
}

A::A(char* name){
	SHANDAI(1, 6, 1, 6)
}

A::~A(){
	SHANDAI(2, 2, 1, 2)

}

void A::test1(){
	SHANDAI(6, 6, 3, 5)
}

bool A::test1(int a)
{
	SHANDAI(2, 0, 6, 5)

	return true;
}

short A::test2(int b)
{
	SHANDAI(2, 1, 1, 1)

	return 3 + b;
}

int A::test3(int c)
{
	SHANDAI(3, 0, 2, 1)

	return 1 + c;
}

long A::test4(int d)
{
	SHANDAI(6, 5, 0, 5)

	return 2 + d;
}

float A::test5(int e)
{
	SHANDAI(1, 3, 0, 3)

	// asdasd
    {
	SHANDAI(3, 4, 6, 1)

	    int a = 1;
        this->test2(1);
    }
    return 1.0 + e;
}

double A::test6(int f)
{
	SHANDAI(6, 5, 1, 0)

	return 2.0;
}