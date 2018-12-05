#include <errno.h>
#include <fcntl.h> 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>


int set_interface_attribs(int fd, int speed)
{
    struct termios tty;

    if (tcgetattr(fd, &tty) < 0) {
        printf("Error from tcgetattr: %s\n", strerror(errno));
        return -1;
    }

    cfsetospeed(&tty, (speed_t)speed);
    cfsetispeed(&tty, (speed_t)speed);

    tty.c_cflag |= (CLOCAL | CREAD);    /* ignore modem controls */
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;         /* 8-bit characters */
    tty.c_cflag &= ~PARENB;     /* no parity bit */
    tty.c_cflag &= ~CSTOPB;     /* only need 1 stop bit */
    tty.c_cflag &= ~CRTSCTS;    /* no hardware flowcontrol */

    /* setup for non-canonical mode */
    tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    tty.c_oflag &= ~OPOST;

    /* fetch bytes as they become available */
    tty.c_cc[VMIN] = 1;
    tty.c_cc[VTIME] = 1;

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        printf("Error from tcsetattr: %s\n", strerror(errno));
        return -1;
    }
    return 0;
}

void set_mincount(int fd, int mcount)
{
    struct termios tty;

    if (tcgetattr(fd, &tty) < 0) {
        printf("Error tcgetattr: %s\n", strerror(errno));
        return;
    }

    tty.c_cc[VMIN] = mcount ? 1 : 0;
    tty.c_cc[VTIME] = 5;        /* half second timer */

    if (tcsetattr(fd, TCSANOW, &tty) < 0)
        printf("Error tcsetattr: %s\n", strerror(errno));
}


void readFromTemp(int arm_state, double *results){
    char *portname = "/dev/ttyUSB0";
    int temp_fd;
    int wlen;
    double tempReading = 0;
    temp_fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    if (temp_fd < 0) {
        printf("Error opening %s: %s\n", portname, strerror(errno));
        exit(-1);
    }
    set_interface_attribs(temp_fd, B9600);
    tcdrain(temp_fd);    /* delay for output */

    /* simple noncanonical input */
    do {
        unsigned char buf[80];
        int rdlen;

        rdlen = read(temp_fd, buf, sizeof(buf) - 1);
        if (rdlen > 0) {
            buf[rdlen] = 0;
            printf("Read %d: \"%s\"\n", rdlen, buf);
            tempReading = atof( buf);

        } else if (rdlen < 0) {
            printf("Error from read: %d: %s\n", rdlen, strerror(errno));
        }
        /* repeat read to get full message */
    } while (1);



}

int main()
{
    char *portname = "/dev/ttyUSB0";
    int arm_fd;
    int wlen;
    int arm_state = 0;
    double results[4];
    arm_fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    if (arm_fd < 0) {
        printf("Error opening %s: %s\n", portname, strerror(errno));
        return -1;
    }
    /*baudrate 115200, 8 bits, no parity, 1 stop bit */
    set_interface_attribs(arm_fd, B9600);
    //set_mincount(arm_fd, 0);                /* set to pure timed read */

    /* simple output */
    // wlen = write(arm_fd, "Hello!\n", 7);
    // if (wlen != 7) {
    //     printf("Error from write: %d, %d\n", wlen, errno);
    // }
    tcdrain(arm_fd);    /* delay for output */


    /* simple noncanonical input */
    do {
        unsigned char buf[80];
        int rdlen;

        rdlen = read(arm_fd, buf, sizeof(buf) - 1);
        if (rdlen > 0) {
            buf[rdlen] = 0;
            printf("Read %d: \"%s\"\n", rdlen, buf);
            arm_state = atoi( buf);

            readFromTemp(arm_state, results);

        } else if (rdlen < 0) {
            printf("Error from read: %d: %s\n", rdlen, strerror(errno));
        }
        /* repeat read to get full message */
    } while (1);
}