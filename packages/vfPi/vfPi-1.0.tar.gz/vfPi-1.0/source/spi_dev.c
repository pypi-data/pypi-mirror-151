// License:MIT
/*
 * SPI testing utility (using spidev driver)
 *
 * Copyright (c) 2025  Starfive, Inc.
 * Author: lousl
 *
 */

#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <getopt.h>
#include <fcntl.h>
#include <time.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>
#include <sys/stat.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>





//#define X86_TEST


#ifdef X86_TEST
int spi_setmode(int speed, int mode, int bits)
{
	printf("---x86 test: %d %d %d\n", speed, mode, bits);
	return 0;
}

int spi_transfer( char *data, int len)
{
	char *databuff;
	int i;

	printf("---x86 test  transfer len is: %d\n", len);
	databuff = malloc(len);
	memcpy(databuff, data, len);
	for(i = 0; i < len; i++){
		printf("---x86 test  transfer data%d is: %d\n", i, databuff[i]);
	}
	return 0;
}

#else

#define VISIONFIVE_SPI_DEV     "/dev/spidev0.0"

static int      fd    = 0;
//static uint32_t mode  = 0;
static uint32_t speed = 500000;
static uint16_t delay = 0;
static uint8_t  bits  = 8;
static int      gmode  = 0;
//for python package
//loushl add
int spi_setmode(int speed, int mode, int bits)
{
	int retval = 0;

	fd = open(VISIONFIVE_SPI_DEV, O_RDWR);
	if(fd < 0){
		printf("open spi dev failed\n");
		return -1;
	}

	gmode = mode;
	retval = ioctl(fd, SPI_IOC_WR_MODE32, &mode);
	if(retval < 0){
		printf("set spi wr mode failed\n");
		return -1;
	}

	retval = ioctl(fd, SPI_IOC_RD_MODE32, &mode);
	if(retval < 0){
		printf("set spi rd mode failed\n");
		return -1;
	}

	retval = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if(retval < 0){
		printf("set wr bits failed\n");
		return -1;
	}

	retval = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
	if(retval < 0){
		printf("set rd bits failed\n");
		return -1;
	}

	retval = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
	if(retval < 0){
		printf("set wr speed failed\n");
		return -1;
	}

	retval = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
	if(retval < 0){
		printf("set wrd speed failed\n");
		return -1;
	}

	printf("set spi mode success\n");
	printf("spi mode: 0x%x\n", mode);
	printf("bits per word: %u\n", bits);
	printf("max speed: %u Hz (%u kHz)\n", speed, speed/1000);
	return 0;

}
//for python package
//loushl add
int spi_transfer(unsigned char *data, size_t len)
{
	int retval, i;
	unsigned char *recv_data = NULL;
	struct spi_ioc_transfer tr;

	memset((unsigned char *)&tr, 0, sizeof(struct spi_ioc_transfer));
	recv_data = malloc(len);
		if(recv_data == NULL){
			printf("-----recv data mem error\n");
			return -1;
		}
		memset(recv_data, 0, len);

	tr.tx_buf = (unsigned long)data;
	tr.rx_buf = (unsigned long)recv_data;
	tr.len = len;
	tr.delay_usecs = delay;
	tr.speed_hz = speed;
	tr.bits_per_word = bits;



#if 1

	if (gmode & SPI_TX_OCTAL)
		tr.tx_nbits = 8;
	else if (gmode & SPI_TX_QUAD)
		tr.tx_nbits = 4;
	else if (gmode & SPI_TX_DUAL)
		tr.tx_nbits = 2;
	if (gmode & SPI_RX_OCTAL)
		tr.rx_nbits = 8;
	else if (gmode & SPI_RX_QUAD)
		tr.rx_nbits = 4;
	else if (gmode & SPI_RX_DUAL)
		tr.rx_nbits = 2;
	if (!(gmode & SPI_LOOP)) {
		if (gmode & (SPI_TX_OCTAL | SPI_TX_QUAD | SPI_TX_DUAL))
			tr.rx_buf = 0;
		else if (gmode & (SPI_RX_OCTAL | SPI_RX_QUAD | SPI_RX_DUAL))
			tr.tx_buf = 0;
	}
#endif

	retval = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
	if (retval < 1){
		printf("can't send spi message");
		free(recv_data);
		return -1;
	}

    for(i=0; i<(int)tr.len; i++){
    	printf("---recv data%d is: %d\n", i, recv_data[i]);
    }
	free(recv_data);
	return 0;
}
#endif
