#ifndef __B1CHANGE_H__
#define __B1CHANGE_H__

void b1change(int *encoder_pos1){
encoder_pos1 += (digitalRead(pin1A)==digitalRead(pin1B))?-1:1;
}

#endif
