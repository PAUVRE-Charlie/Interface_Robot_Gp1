const byte moteur_d = A1; //envoie du PWM au moteur droit
const byte moteur_g = A2; //envoie du PWM au moteur gauche
const byte mesure_d = A3; //reception en PWM de la vitesse mesurée à droite
const byte mesure_g = A4; //reception en PWM de la vitesse mesurée à gauche

const float e = 0; //Valeur à trouver
const float a_max = 0.5;//   en m/s^2
const float v_max = 1.0; //  en m/s
const float pi = 3.1416;

//Besoin de ces 3 infos pour se repérer dans l'espace de façon orientée
float x_veh;
float y_veh;
float angle_veh;

//Coordonées du prochain point à atteindre
//On pourrait aussi rajouter une orientation si on veut, à voir
float delta_x;
float delta_y;

//Vitesses doivent toujours etre dispo pour qu'on puisse y acceder quand on veut
float vg;
float vd;
float vd_mes;
float vg_mes;

//Variables utiles pour plusieurs Headers
int etat; //sert à effectuer chaque fonction sans inhiber le reste du programme tout en connaissant l'état actuel des actions menées
unsigned long time; //sert à effectuer des chronos à chaque fois, à rafraichir dès qu'il ne sert plus
int sens; //sert pour les différentiels entre les roues. 0=droite et 1=gauche

#include "demi_cercle.h"
#include "pivot.h"


void setup() {

    pinMode(A0, INPUT);
    pinMode(A1, OUTPUT);
    pinMode(A2, OUTPUT);

    analogWrite(A2, 0);
    analogWrite(A1, 0);

    etat = 0;

    Serial.begin(9600);
}

void loop() {
    
    //Si etat = 0 on lit, sinon on ignore la commande
    //PARTIE LECTURE (où Aziz et Guillaume envoient x_cons, y-cons et theta_cons et Alexis et Charlie envoient les mesures)
    //Si theta = 0, on en conclut que c'est un ligne droite ou un demi cercle, sinon c'est un pivot d'angle theta
    
    vd_mes = analogRead(A3);
    vg_mes = analogRead(A4);
    
    //PARTIE CALCUL
    //Penser à rajouter un PID dans chaque prgm
    if (theta != 0) {
        etat = pivot(&theta, &vg, &vd);
    }

    else if ((cos(angle_veh) * sqrt((x_cons - x_veh) * (xcons - x_veh) + (y_cons - y - veh) * (y_cons - y_veh)) == (x_cons - x_veh)) && (sin(angle_veh) * sqrt((x_cons - x_veh) * (xcons - x_veh) + (y_cons - y - veh) * (y_cons - y_veh)) == (y_cons - y_veh))) {
        etat = ligne_droite(x_cons, y_cons, x_veh, y_veh, &vg, &vd);
    }

    else {
        etat = demi_cercle(x_eh, y_veh, x_consigne, y_consigne, &vg, &vd, &sens);
    }
    
    //PARTIE ECRITURE
    analogWrite(A1, vd);
    analogWrite(A2, vg);
}
