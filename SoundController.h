#ifndef _SoundController_h_
#define _SoundController_h_

#include "Controller.h"

namespace Magnum
{
	class SoundController : public Controller
	{
	public:
		SoundController();
		~SoundController();
	public:
		virtual long func1();
		virtual short func2(long p1, short p2, short p3, int p4, float p5, char p6, unsigned char p7);
		virtual short func3(unsigned short p8, unsigned int p9, long p10);
		float func4(unsigned long p11, short p12, unsigned int p13, float p14);
		unsigned short func5(unsigned long p15, short p16, unsigned int p17, unsigned int p18, unsigned long p19, unsigned short p20, float p21, char p22, short p23);
		float func6(long p24, int p25, int p26, short p27, unsigned long p28, unsigned short p29);
		unsigned short func7(unsigned int p30, short p31);
		int func8(unsigned int p32, unsigned int p33);
		unsigned long func9(int p34, unsigned long p35);
	protected:
		virtual unsigned long func10(unsigned char p36);
		virtual short func11(char p37, unsigned short p38, int p39);
		unsigned long func12(unsigned int p40, unsigned long p41, unsigned char p42, long p43, unsigned long p44, long p45);
		long func13();
		unsigned char func14();
		char func15(short p46, unsigned int p47, long p48, unsigned char p49, int p50, unsigned int p51, unsigned int p52, unsigned long p53, char p54);
		unsigned char func16(long p55, char p56, unsigned long p57, short p58, short p59, char p60, unsigned char p61);
	private:
		virtual double func17(int p62, int p63, short p64, int p65, unsigned long p66, long p67, long p68);
		short func18();
		unsigned long func19(unsigned short p69, long p70, unsigned long p71);
		double func20(int p72, unsigned short p73, float p74, short p75, char p76);
		unsigned short func21(unsigned int p77, int p78, unsigned char p79, unsigned long p80, float p81, char p82);
	public:
		short m_var1;
		long m_var2;
		short m_var3;
		double m_var4;
		unsigned long m_var5;
		long m_var6;
		double m_var7;
		double m_var8;
		float m_var9;
	protected:
		unsigned char m_var10;
		unsigned char m_var11;
		unsigned char m_var12;
		unsigned int m_var13;
		unsigned char m_var14;
		long m_var15;
		long m_var16;
		int m_var17;
	private:
		long m_var18;
		unsigned short m_var19;
		double m_var20;
		unsigned short m_var21;
		char m_var22;
		unsigned long m_var23;
		unsigned char m_var24;
	};	
};

#endif // _SoundController_h_
