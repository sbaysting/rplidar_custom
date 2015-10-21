
#include "rplidar_api.h" //RPLIDAR standard sdk, all-in-one header

using namespace rp::standalone::rplidar;

// argv[1] = device path i.e. /dev/ttyUSB0

int main(int argc, const char * argv[]) {

    // Create RPLIDAR driver
    if(argc <= 1){
        if(createDriver() == false){
            return 1;
        }
    } else {
        if(createDriver(argv[1]) == false){
            return 1;
        }
    }

    // Create new instance of the lidar data structure to store data
    lidar_data* data = new lidar_data(360*2);

    // Start the LIDAR scanner
    if(data->startScan() == false){
        return 2;
    }

    // Run update and display data in a loop
    //int rot_count = 0;
    while(1){

        if(data->updateData() == true){ // If the data update succeeded
            for (uint pos = 0; pos < data->count ; ++pos) { // Loop through each data node
                /*printf("%s theta: %03.2f Dist: %08.2f Q: %d \n",
                    data->getSyncBit(pos) ?"S ":"  ", //Display sync bit
                    data->getTheta(pos), //Display theta value for that node
                    data->getDistance(pos), //Display distance value for that node
                    data->getQuality(pos)); //Display quality value for that node*/
                printf("%03.2f %08.2f \n",data->getTheta(pos),data->getDistance(pos));
            }
        }
    }

}
