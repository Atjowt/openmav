#ifndef _OPENMAV_H
#define _OPENMAV_H

#include <unistd.h>

#include "FGNetFDM.h"

typedef struct FGNetFDM OpenMav_Data;

// Opaque OpenMav client object
typedef struct OpenMav_Client OpenMav_Client;

OpenMav_Client* openmav_connect(uint16_t port);
void openmav_disconnect(OpenMav_Client* client);
ssize_t openmav_receive(const OpenMav_Client* client, OpenMav_Data* data);

#endif // _OPENMAV_H
