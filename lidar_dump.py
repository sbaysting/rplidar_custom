from reader import rplidar

lidar = rplidar(device='/dev/ttyUSB2')
lidar.connect()
lidar.dump()