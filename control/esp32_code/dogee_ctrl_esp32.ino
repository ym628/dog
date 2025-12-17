#include <ESP32_Servo.h>

enum {
  M0 = 0,
  M1,
  M2,
  M3,
  S1,
  S2,
  US
};

const int BUFFER_SIZE = 7 * sizeof(short);

// 创建舵机实例
Servo servo_25;
Servo servo_26;

short status[] = { 0, 0, 0, 0, 90, 10 };


short check_val = -12345;

// 舵机转动
void set_servo(short* angles) {
  servo_25.write(angles[0]);
  servo_26.write(angles[1]);
}


void setup() {

  Serial.begin(115200);

  servo_25.attach(25, 500, 2500);
  servo_26.attach(26, 500, 2500);

  short init_speeds[] = { 0, 0, 0, 0 };
  short init_angles[] = { 90, 10 };
  set_servo(init_angles);

}


void loop() {
  if (Serial.available() > 0) {
    short curr_status[] = { 0, 0, 0, 0, 110, 90, 1 };
    Serial.readBytes((char*)curr_status, BUFFER_SIZE);

    short angles[] = { curr_status[S1], curr_status[S2] };
    short check = curr_status[US];

    if (!(check ^ check_val)) {
      set_servo(angles);
      Serial.println("SUCC");
    }
  }
}
