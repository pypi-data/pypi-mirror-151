/*
Copyright (c) 2022-2027 Starfive

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#ifndef _SHTC3_DEV_H_
#define _SHTC3_DEV_H_

#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <stdlib.h>

#include <stdint.h> 
#include <getopt.h> 
#include <fcntl.h> 
#include <sys/ioctl.h> 
#include <linux/types.h> 
#include <linux/i2c.h>
#include <linux/i2c-dev.h> 

//i2c address
#define SHTC3_I2C_ADDRESS	    	0x70
#define I2C_DEVICE					"/dev/i2c-1"

//Commands
#define SHTC3_WakeUp                0x3517
#define SHTC3_Sleep                 0xB098
#define SHTC3_NM_CE_ReadTH          0x7CA2
#define SHTC3_NM_CE_ReadRH          0x5C24
#define SHTC3_NM_CD_ReadTH          0x7866
#define SHTC3_NM_CD_ReadRH          0x58E0
#define SHTC3_LM_CE_ReadTH          0x6458
#define SHTC3_LM_CE_ReadRH          0x44DE
#define SHTC3_LM_CD_ReadTH          0x609C
#define SHTC3_LM_CD_ReadRH          0x401A
#define SHTC3_Software_RES          0x401A
#define SHTC3_ID               0xEFC8

#define CRC_POLYNOMIAL              0x131 // P(x) = x^8 + x^5 + x^4 + 1 = 100110001
extern int fd;

char SHTC3_CheckCrc(char data[],unsigned char len,unsigned char checksum);
void SHTC3_WriteCommand(unsigned short cmd);
void SHTC3_WAKEUP(void);
void SHTC3_SLEEP(void);
void SHTC_SOFT_RESET(void);
float SHTC3_Read_DATA(unsigned short cmd);
int SHTC3_Open(void);
void SHTC3_Close(void);
float SHTC3_GetTemp(void);
float SHTC3_GetHum(void);

#endif //_SHTC3_DEV_H_