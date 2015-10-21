#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>
#include <avr/wdt.h>

/* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_L3GD20_Unified       dofsensor = Adafruit_L3GD20_Unified(30303);
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
boolean boot = false;

void displaySensorDetails(void)
{
  sensor_t sensor, sensor1, sensor2, sensor3;
  accel.getSensor(&sensor);
  dofsensor.getSensor(&sensor1);
  mag.getSensor(&sensor2);
  bmp.getSensor(&sensor3);
  Serial.println("");
  Serial.println("------------------------------------");
  Serial.println("INS Sensor Information");
  Serial.println("");
  Serial.print  ("Accelerometer:     "); Serial.println(sensor.name);
  Serial.print  ("Gyroscope:         "); Serial.println(sensor1.name);
  Serial.print  ("Compass:           "); Serial.println(sensor2.name);
  Serial.print  ("Pressure:          "); Serial.println(sensor3.name);
  Serial.print  ("Temperature:       "); Serial.println(sensor3.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" m/s^2");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" m/s^2");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" m/s^2");  
  Serial.println("------------------------------------");
  Serial.println("");
  Serial.println("START DATA");
  delay(500);
  boot = true;
}

/**************************************************************************/
/*!
    @brief  Initialises all the sensors used by this example
*/
/**************************************************************************/
void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
  
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
  if(!bmp.begin())
  {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.println("Ooops, no BMP180 detected ... Check your wiring!");
    while(1);
  }
  
  /* Display some basic information on the accelerometer sensor */
  displaySensorDetails();
}

/**************************************************************************/
/*!

*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  
  /* Initialise the sensors */
  initSensors();
}

/**************************************************************************/
/*!
    @brief  Constantly check the roll/pitch/heading/altitude/temperature
*/
/**************************************************************************/

String input = "";
boolean inputComplete = false;

void loop(void)
{
  if(boot){
    serialEvent(); // Listen for a serial incoming transmission
    
    if(inputComplete){ // If incoming RX is complete
      if(input.endsWith("reset")){ // If it's a reset signal, reset it
        reset();
      }    
      inputComplete = false;
      input = "";
    }
    sensors_event_t accel_event;
    sensors_event_t mag_event;
    sensors_event_t bmp_event;
    sensors_vec_t   orientation;
  
    /* Calculate pitch and roll from the raw accelerometer data */
    accel.getEvent(&accel_event);
    if (dof.accelGetOrientation(&accel_event, &orientation))
    {
      /* 'orientation' should have valid .roll and .pitch fields */
      Serial.print("roll,");
      Serial.print(orientation.roll);
      Serial.print(",");
      Serial.print("pitch,");
      Serial.print(orientation.pitch);
      Serial.print(",");
    }
    
    /* Calculate the heading using the magnetometer */
    mag.getEvent(&mag_event);
    if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
    {
      /* 'orientation' should have valid .heading data now */
      Serial.print("heading,");
      Serial.print(orientation.heading);
      Serial.print(",");
    }
  
    /* Calculate the altitude using the barometric pressure sensor */
    bmp.getEvent(&bmp_event);
    if (bmp_event.pressure)
    {
      /* Get ambient temperature in C */
      float temperature;
      bmp.getTemperature(&temperature);
      /* Convert atmospheric pressure, SLP and temp to altitude (measured in m)   */
      Serial.print("alt,");
      Serial.print(bmp.pressureToAltitude(seaLevelPressure,
                                          bmp_event.pressure,
                                          temperature)); 
      Serial.print(",");
      /* Display the temperature (measured in C)*/
      Serial.print("temp,");
      Serial.print(temperature);
      Serial.print(",");
    }
    
    /* Display the acceleration results (acceleration is measured in m/s^2) */
    Serial.print("accelx,"); Serial.print(accel_event.acceleration.x); Serial.print(",");
    Serial.print("accely,"); Serial.print(accel_event.acceleration.y); Serial.print(",");
    Serial.print("accelz,"); Serial.print(accel_event.acceleration.z); Serial.println("");
    delay(100);
  }
  
}

void serialEvent(){ //RX serial listener
  while(Serial.available()){
    char tmpChar = (char)Serial.read(); //Get one byte of the message
    input += tmpChar; //Append it to the string
    if(input.endsWith("reset")){
      inputComplete = true;
    }
  }
}

void reset(){ // Reset the software
  
  Serial.println("Resetting..."); 
  wdt_enable(WDTO_15MS);
  while(1)
  {
  }
  
}
