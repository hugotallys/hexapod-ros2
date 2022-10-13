#include <Servo.h>

Servo joint11, joint12, joint13;

void writePosition(double a11, double a12, double a13) {
  joint11.write( a11 );   // initial position
  joint12.write( a12 );   // initial position
  joint13.write( a13 );   // initial position
  delay(500);
}

void setup() {  
  joint11.attach( 9 );    // attaches the servo on pin 9 to the servo object
  joint12.attach( 10 );   // attaches the servo on pin 9 to the servo object
  joint13.attach( 11 );   // attaches the servo on pin 9 to the servo object
}

void loop() {
  writePosition( 90., 90., 90. );
  /* writePosition( 0., 90., 170. );
  writePosition( 0., 160., 170. );
  writePosition( 0., 30., 90. );
  writePosition( 90., 90., 90. ); */
}
