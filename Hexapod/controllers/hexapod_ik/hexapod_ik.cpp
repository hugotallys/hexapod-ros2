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

#define L1 0.08
#define L2 0.1142

using namespace webots; // all the webots classes are defined in the "webots" namespace
using namespace std;

Robot *robot = new Robot(); // create the Robot instance.

Motor *joint11 = robot->getMotor("joint11");
Motor *joint12 = robot->getMotor("joint12");
Motor *joint13 = robot->getMotor("joint13");

int timeStep = ( int ) robot->getBasicTimeStep(); // get the time step of the current world.

int T = int(1000 / timeStep);

double deg2rad(double angle) {
  return angle * (M_PI/180.0);
}

void delay(int ms) {
  for (int iter = ms / timeStep; iter > 0; iter--) {
    robot->step(timeStep);
  } 
}

void invkine(double *p, double *q) {
  double x = p[0];
  double y = p[1];
  double z = p[2];
  
  double L = sqrt(x*x + y*y + z*z);
  
  q[0] = atan2(x, y) - M_PI;  
  q[1] = (M_PI / 2.) - acos( (L1*L1 + L*L - L2*L2)/(2*L1*L) ) - atan2( sqrt(x*x + y*y), z) + M_PI;
  q[2] = (M_PI / 2.) - acos( (L1*L1 + L2*L2 - L*L)/(2*L1*L2) );
}

void writePosition(double a11, double a12, double a13) {  
  joint11->setPosition( deg2rad( 90.0 - a11 ) );
  joint12->setPosition( -deg2rad( 90.0 - a12 ) );
  joint13->setPosition( deg2rad( 90.0 - a13 ) );
  delay(50);
}

void setJointsPosition(double a11, double a12, double a13) {  
  joint11->setPosition( a11 );
  joint12->setPosition( a12 );
  joint13->setPosition( a13 );
  delay(1000);
}

int main(int argc, char **argv) {
  
  /*int t = 0;
  double w[3] = { 0.1, 0.2, 0.05};
  double a[3] = { 50.0, 30.0, 0.0};
  double b[3] = { 90., 60., 120. };
  */
  double thetas[3] = { 0., 0., 0. };
  double ballPos[3] = { 0.1275 - 0.0875, -0.1305 + 0.0505, -0.07 };
  
  invkine(ballPos, thetas); // 0.44 -0.44 0.5
  
  /*vector<vector<double>> pos(3, vector<double>(T));
  
  for (int row = 0; row < 3; row++) {
    for (int col = 0; col < T; col++) {
      pos[row][col] = b[row] - a[row] * sin(w[row]*col);
    }
  }*/
  
  while (robot->step(timeStep) != -1) {
    // setJointsPosition( 0.44, -0.44, 0.5 );
    // setJointsPosition( -thetas[0], -thetas[1], thetas[2] );
    // writePosition(pos[0][t], pos[1][t], pos[2][t]);
    // t = (t + 1) % T;
  }
  
  // Exit cleanup code
  
  delete robot;
  delete joint11;
  delete joint12;
  delete joint13;
  
  return 0;
}
