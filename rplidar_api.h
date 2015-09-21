#ifndef _RPLIDAR_API_H
#define _RPLIDAR_API_H

#include "rplidar_sdk_v1.4.5/sdk/sdk/include/rplidar.h"
#include <stdio.h>
#include <stdlib.h>

using namespace rp::standalone::rplidar;

extern RPlidarDriver * driver;

void disposeDriver();
void disposeDriver(RPlidarDriver * drv);
bool checkRPLIDARHealth(RPlidarDriver * drv);
bool createDriver(const char * path = "/dev/ttyUSB0", _u32 baudrate = 115200);

struct lidar_data{

    rplidar_response_measurement_node_t nodes[360*2];
    size_t count;

    lidar_data(int numberOfNodes);
    bool startScan();
    bool updateData();
    float getTheta(uint node);
    float getDistance(uint node);
    int getQuality(uint node);
    bool getSyncBit(uint node);

};

#endif
