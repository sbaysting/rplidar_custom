
#include "rplidar_api.h" //RPLIDAR standard sdk, all-in-one header

using namespace rp::standalone::rplidar;

int main(int argc, const char * argv[]) {

    // Create RPLIDAR driver
    if(createDriver() == false){
        return 1;
    }

    lidar_data* data = new lidar_data(360*2);

    if(data->startScan() == false){
        return 2;
    }

    while(1){
        if(data->updateData() == true){
            for (uint pos = 0; pos < data->count ; ++pos) {
                printf("%s theta: %03.2f Dist: %08.2f Q: %d \n",
                    data->getSyncBit(pos) ?"S ":"  ",
                    data->getTheta(pos),
                    data->getDistance(pos),
                    data->getQuality(pos));
            }
        }
    }

}
