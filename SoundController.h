#ifndef _SoundController_h_
#define _SoundController_h_

#include "Controller.h"

namespace Magnum
{
	class SoundController
	{
	public:
		SoundController();
		~SoundController();
	public:
		virtual unsigned int func1(unsigned long p1, char p2, short p3, unsigned short p4);
		virtual char func2(unsigned int p5, short p6, int p7);
		virtual float func3(unsigned int p8, unsigned int p9);
		char func4(float p10);
		long func5(short p11, unsigned int p12, long p13);
		unsigned char func6(char p14, int p15, long p16, unsigned long p17, short p18, unsigned long p19, char p20, unsigned char p21, unsigned char p22);
		unsigned char func7();
		unsigned int func8(unsigned long p23);
		unsigned int func9(long p24, unsigned int p25);
	protected:
		virtual unsigned int func10(short p26);
		virtual unsigned long func11(unsigned long p27, int p28, unsigned long p29, char p30);
		short func12(unsigned int p31, unsigned long p32);
		unsigned long func13();
		short func14(unsigned long p33, unsigned char p34, float p35, unsigned short p36, unsigned long p37, unsigned long p38, unsigned char p39, unsigned int p40, int p41);
		unsigned long func15(short p42, char p43);
		short func16(char p44, unsigned long p45, unsigned int p46, long p47, int p48, int p49, unsigned int p50);
	private:
		virtual int func17(float p51, char p52, unsigned char p53, unsigned short p54);
		long func18(unsigned char p55, unsigned short p56, unsigned short p57, int p58, unsigned short p59);
		int func19(int p60);
		int func20(short p61, long p62, unsigned long p63, char p64);
		char func21(unsigned long p65, long p66, unsigned short p67, unsigned int p68, unsigned short p69);
	public:
		unsigned long m_var1;
		char m_var2;
		short m_var3;
		char m_var4;
		unsigned short m_var5;
		unsigned int m_var6;
		short m_var7;
		int m_var8;
		unsigned char m_var9;
	protected:
		long m_var10;
		int m_var11;
		long m_var12;
		unsigned short m_var13;
		long m_var14;
		long m_var15;
		float m_var16;
		float m_var17;
	private:
		unsigned int m_var18;
		short m_var19;
		unsigned int m_var20;
		unsigned char m_var21;
		unsigned short m_var22;
		unsigned short m_var23;
		unsigned short m_var24;
	};	
};

#endif // _SoundController_h_
