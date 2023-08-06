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

#include "SHTC3_dev.h" 

int fd;

char SHTC3_CheckCrc(char data[],unsigned char len,unsigned char checksum)
{
  unsigned char bit;        // bit mask
  unsigned char crc = 0xFF; // calculated checksum
  unsigned char byteCtr;    // byte counter
  // calculates 8-Bit checksum with given polynomial
  for(byteCtr = 0; byteCtr < len; byteCtr++) {
    crc ^= (data[byteCtr]);
    for(bit = 8; bit > 0; --bit) {
      if(crc & 0x80) {
        crc = (crc << 1) ^ CRC_POLYNOMIAL;
      } else {
        crc = (crc << 1);
      }
    }
  }

  // verify checksum
  if(crc != checksum) {                 
    return 1;                       //Error
  } else {
    return 0;                       //No error
  }       
}

void SHTC3_WriteCommand(unsigned short cmd)
{   
    char buf[] = { (cmd>>8) ,cmd};
	write(fd,buf,2); 
}

void SHTC3_WAKEUP()
{     
    SHTC3_WriteCommand(SHTC3_WakeUp);                  // write wake_up command  
    usleep(300);                          //Delay 300us  
}

void SHTC3_SLEEP()
{    
 //   bcm2835_i2c_begin();
    SHTC3_WriteCommand(SHTC3_Sleep);                        // Write sleep command
}

void SHTC_SOFT_RESET()
{   
    SHTC3_WriteCommand(SHTC3_Software_RES);                 // Write reset command
    usleep(1000);                                 //Delay 1ms
}

float SHTC3_GetTemp() {
	return SHTC3_Read_DATA(SHTC3_NM_CD_ReadTH);
}

float SHTC3_GetHum() {
	return SHTC3_Read_DATA(SHTC3_NM_CD_ReadRH);
}

float SHTC3_Read_DATA(unsigned short cmd)
{   
	unsigned short DATA = 0;
	float rslt = 0.0;
	char buf[3] = {0};
	char checksum;

	SHTC3_WriteCommand(cmd);                 //Read temperature first,clock streching disabled (polling)
	usleep(20000);
	read(fd, buf, 3);

	checksum = buf[2];
	if(!SHTC3_CheckCrc(buf,2,checksum))
	    DATA = (buf[0]<<8|buf[1]);

	if (cmd == SHTC3_NM_CD_ReadTH)
		rslt = 175 * (float)DATA / 65536.0f - 45.0f;       //Calculate temperature value

	if (cmd == SHTC3_NM_CD_ReadRH)
		rslt = 100 * (float)DATA / 65536.0f;              //Calculate humidity value  

	SHTC3_SLEEP();
	SHTC3_WAKEUP();	

	return rslt;
}

int SHTC3_Open()
{   
    //printf("\n SHTC3 Sensor Test Program ...\n");
	if (fd > 0)
		return -1;
	fd = open(I2C_DEVICE, O_RDWR);
	if(fd < 0)
	{
		printf("Fail to open i2c device\r\n");
		return -1;
	}
	else
	{
		printf("Fopen : %s\r\n", I2C_DEVICE);
	}

	if(ioctl(fd, I2C_SLAVE, SHTC3_I2C_ADDRESS) < 0)
	{
		printf("I2C: Failed to connect to the device\n");
		return -1;
	}

    return 0;
}

void SHTC3_Close() {
	if (fd > 0) {
		fd = -1;
		close(fd);
	}
}


