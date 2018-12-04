#import "Student.h" 

@implementation Student
{
	int x; //这里定义的变量，没有修饰符为私有作用域。 一般也是用来定义隐藏信息的
}

-(void)aa
{
	//使用成员变量
	a = 8;
	self->c = 9; //self指代自身
}

+(void)ab
{
	//静态方法中 不能调用成员变量
	//可以使用静态变量  
}

-(void)ac 
{
}

-(int)ad:(int)pa  ae : (int)pb 
{
}

+(int)af : (int)pa : (int)pb 
{
}

@end