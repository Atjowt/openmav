#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "openmav.h"
#include "network.h"

int main(int argc, char* argv[]) {

	int exitcode = EXIT_SUCCESS;

	printf("Listen to FlightGear port: ");

	uint16_t port;
	scanf("%"SCNu16, &port);

	OpenMav_Client* client = openmav_connect(port);
	if (client == NULL) {
		fprintf(stderr, "Could not connect OpenMav client\n");
		exitcode = EXIT_FAILURE;
		goto terminate;
	}

	printf("Listening on port %"PRIu16"...\n", port);

	OpenMav_Data data;

	while (1) {

		ssize_t bytes = openmav_receive(client, &data);

		// Peer sent close signal
		if (bytes == 0) {
			break;
		}

		// Failed to receive packet
		if (bytes < 0) {
			continue; // Continue, dropping a UDP packet is not the end of the world
		}

		// Print some FlightGear properties: version, altitude, ..., etc.
		// Note the conversions from network byte-order to host byte-order
		printf("%zi bytes received:\n", bytes);
		printf("version: %"PRIu32"\n", ntohl(data.version));
		printf("wheels: %"PRIu32"\n", ntohl(data.num_wheels));
		printf("altitude: %lf meters\n", ntohlf(data.altitude));
		printf("latitude: %lf radians\n", ntohlf(data.latitude));
		printf("longitude: %lf radians\n", ntohlf(data.longitude));
		printf("\n");
	}

terminate:
	printf("Exiting...\n");
	openmav_disconnect(client);
	return exitcode;
}
