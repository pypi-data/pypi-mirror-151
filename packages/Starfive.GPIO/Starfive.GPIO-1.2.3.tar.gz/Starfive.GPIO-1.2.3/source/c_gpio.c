#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "Python.h"
#include "gpio.h"
#include "gpio-utils.h"
#include "c_gpio.h"


#define GPIO44 	492	
#define GPIO22 	470

#define GPIO_KEY1     GPIO44
#define FISCV_GPIO    GPIO22                
#define MAX_BUF	      128                   //Define array size

const int GPIO2line[49] = {
// 0    1	2	 3	  4    5   6   7   8	9	10   11  12  13  14  15  16  17  18  19
   0,   1,  2,   3,   4,  -1,  6, -1,  8,   9,  10,  -1, -1, -1, -1, -1, -1, 17, -1, 19,
//20   21   22   23  24   25   26  27  28   29  30   31   32  33 34  35  36  37  38  39
  20,  21,  22,  -1, -1,  -1,  -1, -1, -1,  -1, -1,  -1,  -1, -1, -1,-1, -1, -1, -1, -1,
// 40  41  42  43  44  45  46  47  48
   -1, -1, -1, -1, 44, -1, 46, -1, -1
};

int gpio_direction[49];

const char gpiochip[] = "gpiochip0";

int get_gpio_offset(int gpio, unsigned int *gpiooffset) {

	if (gpio < 0 && gpio > 49) {
		PyErr_SetString(PyExc_ValueError, "The gpio set is invalid on a Starfive board");
		return 1;
	}

	if (GPIO2line[gpio] < 0) {
		PyErr_SetString(PyExc_ValueError, "The gpio set is invalid on a Starfive board");
		return 1;
	}
	
	*gpiooffset = GPIO2line[gpio];
	
	return 0;
}

int gpio_set_value(unsigned int gpio, unsigned int value)
{
	struct gpio_v2_line_config config;
	struct gpio_v2_line_values values;
	struct gpio_v2_line_request ;
	int ret = 0, fd1;
	unsigned int i, num_lines = 1, gpiooffset = 0 ;
	unsigned int lines[2] = {0};
	//char gpiodes[] = "gpio-hammer" ;
	
	memset(&config, 0, sizeof(config));
	
	get_gpio_offset(gpio, &gpiooffset);
	
	ret = gpiotools_request_config(gpiochip, gpiooffset, &config); 
	if (ret < 0)
		goto exit_error;

	if (config.flags != GPIO_V2_LINE_FLAG_OUTPUT)
		goto exit_error;

	lines[0] = gpiooffset;
	ret = gpiotools_request_line(gpiochip, lines, num_lines,
				 &config, "gpio-hammer");

	if (ret < 0)
		goto exit_error;
	else
		fd1 = ret;

	values.mask = 0;
	values.bits = 0;
	
	for (i = 0; i < num_lines; i++)
		gpiotools_set_bit(&values.mask, i);

	for (i = 0; i < num_lines; i++) {
		if (value)
			gpiotools_set_bit(&values.bits, i);
	}

	ret = gpiotools_set_values(fd1, &values);
	if (ret < 0)
		goto exit_close_error;

exit_close_error:
	ret = gpiotools_release_line(fd1);
exit_error:
	return ret;
}

int gpio_get_value(unsigned int gpio, unsigned int *value)
{
	struct gpio_v2_line_config config;
	struct gpio_v2_line_values values;
	struct gpio_v2_line_request ;
	int ret = 0, fd1;
	unsigned int i, num_lines = 1, gpiooffset = 0;
	unsigned int lines[2] = {0};
	//char gpiodes[] = "gpio-hammer" ;
	
	memset(&config, 0, sizeof(config));
	get_gpio_offset(gpio, &gpiooffset);
	ret = gpiotools_request_config(gpiochip, gpiooffset, &config); 
	if (ret < 0)
		goto exit_error;

	if (config.flags != GPIO_V2_LINE_FLAG_INPUT)
		goto exit_error;

	lines[0] = gpiooffset;
	ret = gpiotools_request_line(gpiochip, lines, num_lines,
				 &config, "gpio-hammer");

	if (ret < 0)
		goto exit_error;
	else
		fd1 = ret;

	values.mask = 0;
	values.bits = 0;
	
	for (i = 0; i < num_lines; i++)
		gpiotools_set_bit(&values.mask, i);

	ret = gpiotools_get_values(fd1, &values);
	if (ret < 0)
		goto exit_close_error;

	for (i = 0; i < num_lines; i++)
		*value = gpiotools_test_bit(values.bits, i);

exit_close_error:
	gpiotools_release_line(fd1);
exit_error:
	return ret;
}

void output_gpio(int gpio, unsigned int value)
{
	gpio_set_value(gpio, value);
}

void input_gpio(int gpio, int *value)
{
	unsigned int get_value;
	
	gpio_get_value(gpio, &get_value);
	*value = (int) get_value;
}

int output_py(unsigned int gpio, int value) {
	unsigned int gpiooffset, set_value;
	
	if (get_gpio_offset(gpio, &gpiooffset))
	  return 0;

   if (gpio_direction[gpio] != OUTPUT)
   {
	  PyErr_SetString(PyExc_RuntimeError, "The GPIO port has not been set up as OUTPUT");
	  return 0;
   }

   if (value < 0)
   		return 0;

   set_value = (unsigned int ) value;
   output_gpio(gpio, set_value);
   return 1;
}

int input_py(int gpio) {
	unsigned int gpiooffset = 0;
	int value = 0;
	
	if (get_gpio_offset(gpio, &gpiooffset))
	  return 0;

   if (gpio_direction[gpio] != INPUT)
   {
	  PyErr_SetString(PyExc_RuntimeError, "The GPIO port has not been set up as INPUT");
	  return 0;
   }

   input_gpio(gpio, &value);
   return value;
}

int gpio_set_dir(unsigned int gpio, int direction)
{
	struct gpio_v2_line_config config;
	struct gpio_v2_line_request ;
	int ret = 0, fd1;
	unsigned int num_lines = 1, GPIOOffset = 0;
	unsigned int lines[2] = {0};
	
	//char gpiodes[] = "gpio-hammer" ;
	
	memset(&config, 0, sizeof(config));

	get_gpio_offset(gpio, &GPIOOffset);
	
	ret = gpiotools_request_config(gpiochip, GPIOOffset, &config);	
	if (ret < 0)
		goto exit_error;

	if (direction == INPUT)
		config.flags = GPIO_V2_LINE_FLAG_INPUT;

	if (direction == OUTPUT)
		config.flags = GPIO_V2_LINE_FLAG_OUTPUT;

	lines[0] = GPIOOffset;
	ret = gpiotools_request_line(gpiochip, lines, num_lines,
			     &config, "gpio-hammer");
	if (ret < 0)
		goto exit_error;
	else
		fd1 = ret;
	ret = gpiotools_release_line(fd1);
exit_error:
	return ret;
}
 
void setup_gpio(int gpio, int direction, int pud)
{
	gpio_set_dir(gpio, direction);
}

int setup_one(int gpio, int direction, int initial) {
	unsigned int gpiooffset;
	int pud = 0;
	
	if (get_gpio_offset(gpio, &gpiooffset))
	  return 0;
	
	setup_gpio(gpio, direction, pud);
	gpio_direction[gpio] = direction;

	if (direction == OUTPUT && (initial == LOW || initial == HIGH)) {
	output_gpio(gpio, initial);
	}
	return 1;
}

void cleanup_one(unsigned int gpio, int *found)
{
	unsigned int gpiooffset;

	if (get_gpio_offset(gpio, &gpiooffset))
	  return;

   // set everything back to input
   if (gpio_direction[gpio] != -1) {
	  setup_gpio(gpio, INPUT, PUD_OFF);
	  gpio_direction[gpio] = -1;
	  *found = 1;
   }
}


