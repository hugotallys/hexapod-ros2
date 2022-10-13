/*
*
* File: hexapod_ik.cpp
* Date: 12/10/2022
* Description: Inverse kinematics of a 18 dof hexapod robot.
* Author: Hugo Tallys Martins Oliveira
*
*/

#include <math.h>
#include <webots/Robot.hpp>
#include <webots/Motor.hpp>

using namespace webots; // all the webots classes are defined in the "webots" namespace

Robot *robot = new Robot(); // create the Robot instance.

Motor *joint11 = robot->getMotor("joint11");
Motor *joint12 = robot->getMotor("joint12");
Motor *joint13 = robot->getMotor("joint13");

int timeStep = (int)robot->getBasicTimeStep(); // get the time step of the current world.

double deg2rad(double angle) {
  return angle * (M_PI/180.0);
}

void delay(int ms) {
  for (int iter = ms / timeStep; iter > 0; iter--) {
    robot->step(timeStep);
  } 
}

void writePosition(double a11, double a12, double a13) {  
  joint11->setPosition( deg2rad( 90.0 - a11 ) );
  joint12->setPosition( -deg2rad( 90.0 - a12 ) );
  joint13->setPosition( deg2rad( 90.0 - a13 ) );
  delay(500);
}

int main(int argc, char **argv) {
  while (robot->step(timeStep) != -1) {
    writePosition( 90., 90., 90. );
    writePosition( 0., 90., 170. );
    writePosition( 0., 160., 170. );
    writePosition( 0., 30., 90. );
    writePosition( 90., 90., 90. );
  }
  
  // Exit cleanup code
  
  delete robot;
  delete joint11;
  delete joint12;
  delete joint13;
  
  return 0;
}
