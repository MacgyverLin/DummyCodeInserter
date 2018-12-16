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
		virtual float func1(short p1, unsigned char p2, long p3, unsigned char p4, float p5, long p6, short p7, float p8, unsigned int p9, unsigned char p10, unsigned int p11, unsigned long p12, short p13, short p14, int p15, unsigned short p16);
		virtual float func2();
		virtual unsigned long func3(int p17, unsigned int p18, int p19, unsigned int p20, long p21, long p22, float p23, unsigned short p24, unsigned int p25, unsigned short p26, short p27, unsigned char p28);
		double func4(long p29, unsigned int p30, int p31, unsigned char p32, short p33, short p34, unsigned int p35, short p36, short p37, unsigned int p38, unsigned char p39, unsigned char p40, int p41, float p42, float p43, long p44);
		float func5(long p45, float p46, float p47, unsigned long p48, unsigned short p49, int p50, unsigned int p51, long p52, unsigned short p53, int p54, unsigned short p55, float p56, long p57);
		unsigned long func6(char p58, int p59);
		char func7(unsigned char p60, unsigned int p61, unsigned int p62, unsigned char p63, unsigned char p64, char p65, unsigned long p66, float p67, unsigned char p68, unsigned int p69, int p70, unsigned long p71, unsigned short p72);
		unsigned long func8(unsigned int p73, float p74, unsigned int p75, unsigned long p76, short p77, char p78, unsigned short p79, unsigned int p80, unsigned short p81, int p82, unsigned char p83, int p84, int p85, short p86, int p87, unsigned long p88, int p89, char p90);
		float func9(unsigned int p91, float p92, unsigned char p93, char p94, float p95, unsigned short p96, float p97, unsigned int p98);
	protected:
		virtual unsigned short func10(char p99, unsigned short p100, float p101);
		virtual double func11(unsigned long p102, short p103, unsigned char p104, int p105, int p106, float p107, unsigned char p108, unsigned short p109, int p110, unsigned short p111, short p112, unsigned char p113, short p114, unsigned int p115, char p116, int p117);
		unsigned int func12(unsigned short p118, unsigned long p119, unsigned int p120, unsigned int p121, float p122, unsigned int p123, unsigned short p124, unsigned long p125, unsigned short p126, int p127, unsigned long p128, long p129, char p130, unsigned char p131);
		unsigned short func13(unsigned long p132, char p133, unsigned short p134, float p135, unsigned short p136, unsigned int p137);
		unsigned long func14(unsigned int p138);
		unsigned long func15(unsigned int p139, float p140, char p141, unsigned long p142, unsigned char p143, short p144, char p145, unsigned int p146, float p147, unsigned long p148, float p149, float p150, unsigned short p151, float p152, unsigned short p153);
		unsigned long func16(int p154, unsigned int p155, long p156, char p157, int p158, unsigned int p159, unsigned long p160, short p161, float p162, long p163, unsigned long p164, unsigned int p165, int p166);
	private:
		virtual unsigned short func17(char p167, unsigned int p168, unsigned char p169, unsigned char p170, unsigned char p171);
		unsigned char func18(int p172, unsigned long p173, unsigned short p174, char p175, short p176, int p177, unsigned short p178, char p179, float p180, short p181);
		unsigned int func19(int p182, char p183, unsigned char p184, unsigned long p185, unsigned short p186, char p187, float p188, char p189, unsigned short p190, unsigned long p191, unsigned short p192, short p193, int p194, long p195, char p196, long p197);
		short func20(int p198, char p199, float p200, float p201, unsigned short p202, short p203, float p204, char p205, short p206, unsigned long p207, float p208, unsigned int p209, unsigned long p210, unsigned char p211, long p212, short p213, int p214);
		unsigned short func21(unsigned char p215, float p216, float p217, char p218, short p219, unsigned int p220, unsigned long p221, float p222);
	public:
		unsigned int m_var1;
		unsigned long m_var2;
		unsigned long m_var3;
		unsigned short m_var4;
		long m_var5;
		short m_var6;
		char m_var7;
		unsigned long m_var8;
		unsigned int m_var9;
	protected:
		long m_var10;
		int m_var11;
		unsigned char m_var12;
		double m_var13;
		short m_var14;
		unsigned short m_var15;
		int m_var16;
		long m_var17;
	private:
		short m_var18;
		unsigned long m_var19;
		unsigned char m_var20;
		unsigned char m_var21;
		unsigned int m_var22;
		float m_var23;
		unsigned int m_var24;
	};	
};

#endif // _SoundController_h_
