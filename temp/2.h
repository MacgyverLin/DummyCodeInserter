@interface Student : NSObject //@interface声明。  没有@interface  只有@implementation也能定义一个类
{
@public  //作用域  任意地方
int a;

@protected  //当前及子类
int b;

@private  //当前(包括.m)
int c;

@package //框架中都可访问，，，没用过
int d;
}
-(void)aa; //- 对象方法  调用[stu aa]

+(void)ab; //+ 类方法    调用[Student aa] 

-(void)ac:(int)pa; //带一个int 型参数 pa    [stu ac:pa]    

-(int)ad:(int)pa  ae : (int)pb; //多个参数，可以有多个方法名   [stu ad:pa ae:pb]

+(int)af:(int)pa : (int)pb; //多个参数，只保留第一个方法名   [stu af:pa :pb]

@end