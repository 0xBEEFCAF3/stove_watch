CC = gcc
CFLAGS = -Wall -g

all: sync 

sync:
	mkdir -p bin
	gcc sync.c -o bin/sync


clean:
	rm -rf bin

