
#include "rplidar_api.h"

#include <stdio.h>
#include <stdlib.h>

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

using namespace rp::standalone::rplidar;

RPlidarDriver * driver;

//Disposes of the stored RPLIDAR driver
void disposeDriver(){

    RPlidarDriver::DisposeDriver(driver);

}

//Disposes of the given RPLIDAR driver
void disposeDriver(RPlidarDriver * drv){

    RPlidarDriver::DisposeDriver(drv);

}

//From the RPLIDAR SDK example program
bool checkRPLIDARHealth(RPlidarDriver * drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;


    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        //printf("RPLidar health status : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            // enable the following code if you want rplidar to be reboot by software
            // drv->reset();
            return false;
        } else {
            return true;
        }

    } else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}

// Creates the driver, error checks and stores it
bool createDriver(const char * path, _u32 baudrate){

    const char * opt_com_path = path;
    _u32         opt_com_baudrate = baudrate;

    RPlidarDriver * drv = RPlidarDriver::CreateDriver(RPlidarDriver::DRIVER_TYPE_SERIALPORT);

    // Check if the driver was created
    if (!drv) {
        fprintf(stderr, "Insufficient memory, exit\n");
        exit(-2);
    }

    // Check if the driver can access the serial port
    if (IS_FAIL(drv->connect(opt_com_path, opt_com_baudrate))) {
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n", opt_com_path);
        disposeDriver(drv);
        return false;
    }

    // Check if the driver is still bound and active
    if (!checkRPLIDARHealth(drv)) {
        disposeDriver(drv);
        return false;
    }

    driver = drv;
    return true;
}

//lidar_data constructor, initializes data structures
lidar_data::lidar_data(int numberOfNodes){

    count = _countof(nodes);

}

// Starts the lidar scan
bool lidar_data::startScan(){

    // Check if the driver is still bound and active
    if (!checkRPLIDARHealth(driver)) {
        disposeDriver(driver);
        return false;
    }

    driver->startScan();
    return true;
}

// Update the lidar data
bool lidar_data::updateData(){

    u_result result = driver->grabScanData(nodes, count); //Fill nodes with data
    if (IS_OK(result)) {
        driver->ascendScanData(nodes, count);
        return true;
    }

    return false;
}

// Return a theta value for a particular data point
float lidar_data::getTheta(uint node){

    if(node >= count){
        return 0;
    }
    return (nodes[node].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f;
}

// Return a distance value for a particular data point
float lidar_data::getDistance(uint node){

    if(node >= count){
        return 0;
    }
    return nodes[node].distance_q2/4.0f;
}

// Return a quality number for a particular data point
int lidar_data::getQuality(uint node){

    if(node >= count){
        return 0;
    }
    return nodes[node].sync_quality >> RPLIDAR_RESP_MEASUREMENT_QUALITY_SHIFT;
}

// Return a sync bit boolean value for a particular data point
bool lidar_data::getSyncBit(uint node){

    if(node >= count){
        return 0;
    }
    return (nodes[node].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT);
}

