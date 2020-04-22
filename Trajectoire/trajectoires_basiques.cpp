const float e = 0; //Valeur à trouver
const float a_max = 0.5;//   en m/s^2
const float v_max = 1.0; //  en m/s
const float pi = 3.1416;

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


void setup() {
    etat = 0;
    compteur = 0;

    cumError_d = 0;
    cumError_g = 0;
    lastError_d = 0;
    lastError_g = 0;
    previousTime = millis();

    Serial.begin(9600);
}

void loop() {

    //PARTIE LECTURE
      //Kamil et Seb lisent le tableau de Aziz et Guillaume (l'identifiant id et l'ordre o) quand il faut
      //Alexis et Charlie update les mesures ici, et les stockent dans vd_mes et vg_mes



  
    
      
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
    
    
                                                       
    
    //PARTIE ECRITURE
    //A compléter par Charlie et Alexis
}
