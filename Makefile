.PHONY: all run clean

CC := gcc
CFLAGS := -std=c99 -Wpedantic -O3

all: iconnect

iconnect: openmav.o network.o iconnect.o
	$(CC) -o $@ $^

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $<

run: iconnect
	./$<

clean:
	rm -f *.o iconnect
