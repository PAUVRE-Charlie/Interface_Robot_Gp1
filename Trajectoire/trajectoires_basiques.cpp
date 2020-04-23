const float e = 0.20; //Valeur à trouver
const float a_max = 0.5;//   en m/s^2
const float v_max = 1.0; //  en m/s
const float pi = 3.1416;
const float R = 0.05; // à savoir en m 

//Moteur 1
const int pin1Motor1 = 5;
const int pin2Motor1 = 9;
const int pinPMotor1 = 6;
const int pin1A = 12;
const int pin1B = 3;

int encoder_pos1 = 0; // position de l'encodeur du moteur 1
int previous_encoder_pos1 = 0;
float pos_p1 = 0.;
float temps1=0.;
float temps_p1=0.;

//Moteur 2 
const int pin1Motor2 = 10;
const int pin2Motor2 = 11;
const int pinPMotor2 = 8;
const int pin2A = 7;
const int pin2B = 2;

int encoder_pos2 = 0; //position de l'encodeur du moteur 2
int previous_encoder_pos2=0;
float pos_p2 = 0.; //angle de l'encodeur en ° (voir Charlie)
float temps2=0.;
float temps_p2=0.;

//Besoin de ces 3 infos pour se repérer dans l'espace de façon orientée
float x_veh;
float y_veh;
float angle_veh;


//Vitesses doivent toujours etre dispo pour qu'on puisse y acceder quand on veut
float vg;
float vd;
float vd_mes;
float vg_mes;

//Compteur pour lire les instructions de l'odri une par une
int compteur;


//Variables utiles pour plusieurs Headers
int etat;           //sert à effectuer chaque fonction sans inhiber le reste du programme tout en connaissant l'état actuel des actions menées
unsigned long time; //sert à effectuer des chronos à chaque fois, à rafraichir dès qu'il ne sert plus
int sens;           //sert pour les différentiels entre les roues. 0=droite et 1=gauche
unsigned long delta_acc;
unsigned long delta_plat;

//Pour les PID
unsigned long currentTime, previousTime;
double elapsedTime;
float output_d, output_g;

#include "demi_cercle.h"
#include "pivot.h"
#include "ligne_droite.h"
#include "pid.h"
#include "b1_change.h"
#include "b2_change.h"

void setup() {
    etat = 0;
    compteur = 0;

    cumError_d = 0;
    cumError_g = 0;
    lastError_d = 0;
    lastError_g = 0;
    
    previousTime = millis();
    
   //Moteur1
    pinMode(pin1Motor1, OUTPUT);
    pinMode(pin2Motor1, OUTPUT);
    pinMode(pinPMotor1, OUTPUT);
  
  
    pinMode(pin1A,INPUT_PULLUP);
    pinMode(pin1B,INPUT_PULLUP);
    attachInterrupt(1,B1Change,CHANGE);
  
  //Moteur2
    pinMode(pin1Motor2, OUTPUT);
    pinMode(pin2Motor2, OUTPUT);
    pinMode(pinPMotor2, OUTPUT);
  
  
    pinMode(pin2A,INPUT_PULLUP);
    pinMode(pin2B,INPUT_PULLUP);
  
    attachInterrupt(0,B2Change,CHANGE);
    
    Serial.begin(9600);
}

void loop() {

    //PARTIE LECTURE
      //Kamil et Seb lisent le tableau de Aziz et Guillaume (l'identifiant id et l'ordre o) quand il faut
      //Alexis et Charlie update les mesures ici, et les stockent dans vd_mes et vg_mes
      
  previous_encoder_pos1 = encoder_pos1;
  float pos1 = (float)encoder_pos1*360/500/50*14.4; // en degrés attention aux valeurs de motoréduction (50 et 500 dents)
    
  //calcul des vitesses de rotation du moteur et vitesse de la roue 1  
  temps1=millis();
  float vitesse1 = (pos1-pos_p1)/(temps1-temps_p1)*1000; //degré par seconde
  float vitesse_mot1=vitesse1*R;
  Serial.print("Vitesse_mot1 : ");
  Serial.println(vitesse_mot1);
  temps_p1 =temps1;
  pos_p1 = pos1;

  previous_encoder_pos2 = encoder_pos2;
  float pos2 = (float)encoder_pos2*360/500/50*14.4; // en degrés pareil 
  
  //calcul des vitesses de rotation du moteur et vitesse de la roue 2  
  temps2=millis();
  float vitesse2 = (pos2-pos_p2)/(temps2-temps_p2)*1000;
  float vitesse_mot2=vitesse2*R;
  Serial.print("Vitesse_mot2 : ");
  Serial.println(vitesse_mot2);
  pos_p2 = pos2; 
    
  float vitesse_rotation_robot = (vitesse_mot2-vitesse_mot1)/e;
  angle_veh = angle_veh + vitesse_rotation_robot*(temps2-temps_p2);
  
  temps_p2 =temps2;   
    //PARTIE CALCUL
    
    if (id == 0) {
        etat = pivot(o, &vg, &vd);
    }

    else if (id == 1) {
        etat = ligne_droite(o, &vg, &vd);
    }

    else {
        etat = demi_cercle(o, &vg, &vd);
    }
    
    
   
    
    //RECTIFICATION PID
    currentTime = millis();                                        
    elapsedTime = (float)((currentTime - previousTime) / 1000);    
    pid(vg_mes, vd_mes, &vg, &vd, elapsedTime);
    previousTime = currentTime;                        
    
    vg = constrain(vg, 0, 255);
    vd = constrain(vd, 0, 255);
                                                       
    
    //PARTIE ECRITURE
    //A compléter par Charlie et Alexis
    
 if (128<=PWM1<=255){ 
		digitalWrite(pin1Motor1, LOW);
		digitalWrite(pin2Motor1, HIGH);
    	PWM1 = 2*(PWM1-128);  //on redéfinitl'échelle des pourcetages
    }
if (0<=PWM1<=127){
    	digitalWrite(pin1Motor1, HIGH);
  		digitalWrite(pin2Motor1, LOW);
    	PWM1 = 2*(127-PWM1);  //on redéfinit l'échelle des pourcetages
    }
if (0<=PWM2<=127){
    	digitalWrite(pin1Motor2, HIGH);
      	digitalWrite(pin2Motor2, LOW);
    	PWM2 = 2*(127-PWM2);  //on redéfinit l'échelle des pourcetages
    }
if (128<=PWM2<=255){
    	digitalWrite(pin1Motor2, LOW);
  		digitalWrite(pin2Motor2, HIGH);
    	PWM2 = 2*(PWM2-128);  //on redéfinit l'échelle des pourcetages
    }
     analogWrite(pinPMotor1, PWM1);
     analogWrite(pinPMotor2, PWM2);
  
}
