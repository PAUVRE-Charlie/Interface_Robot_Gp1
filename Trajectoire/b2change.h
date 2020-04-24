#ifndef __B2CHANGE_H__
#define __B2CHANGE_H__

void b2change(int *ender_pos_2){
  encoder_pos_2 += (digitalRead(pin2A)==digitalRead(pin2B))?-1:1;
  }
  
#endif
