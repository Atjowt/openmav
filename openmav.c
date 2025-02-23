#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>
#include <arpa/inet.h>

#include "openmav.h"

struct OpenMav_Client {
	int sockfd;
	struct sockaddr_in client_addr;
	socklen_t addr_len;
};

OpenMav_Client* openmav_connect(uint16_t port) {

	OpenMav_Client* client = calloc(1, sizeof(OpenMav_Client));

	// Create UDP socket
	client->sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (client->sockfd < 0) {
		perror("socket creation failed");
		free(client);
		return NULL;
	}

	// Configure server address
	struct sockaddr_in server_addr = { 0 };
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY; // Use any host address
	server_addr.sin_port = htons(port); // Use provided port

	// Bind the UDP socket
	if (bind(client->sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
		perror("bind failed");
		free(client);
		return NULL;
	}

	return client;
}

void openmav_disconnect(OpenMav_Client* client) {
	close(client->sockfd);
	free(client);
}

ssize_t openmav_receive(const OpenMav_Client* client, OpenMav_Data* data) {
	socklen_t addr_len = sizeof(client->client_addr);
	return recvfrom (
		client->sockfd,
		data,
		sizeof(OpenMav_Data),
		0,
		(struct sockaddr*)&client->client_addr,
		&addr_len
	);
}

