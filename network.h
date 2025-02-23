#ifndef _NETWORK_H
#define _NETWORK_H

#include <netinet/in.h>

// Network byte-order to host byte-order: 32-bit floating point value
float ntohf(float value);

// Network byte-order to host byte-order: 64-bit unsigned integer value
uint64_t ntohll(uint64_t value);

// Network byte-order to host byte-order: 64-bit floating point value
double ntohlf(double value);

#endif // _NETWORK_H

