#include <bits/endian.h>

#include "network.h"

float ntohf(float value) {
	uint32_t tmp = ntohl(*(uint32_t*)&value);
	float res = *(float*)&tmp;
	return res;
}

uint64_t ntohll(uint64_t value) {
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	uint64_t hi = ntohl(value & 0xFFFFFFFF);
	uint64_t lo = ntohl(value >> 32);
	return (hi << 32) | lo;
#else
	return value;
#endif
}

double ntohlf(double value) {
	uint64_t tmp = ntohll(*(uint64_t*)&value);
	double res = *(double*)&tmp;
	return res;
}

