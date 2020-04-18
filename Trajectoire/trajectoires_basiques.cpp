const byte moteur_d = A1;
const byte moteur_g = A2;

const float e = 0; //Valeur � trouver
const float a_max = 0.5;//   en m/s^2
const float v_max = 1.0; //  en m/s
const float pi = 3.1416

//Besoin de ces 3 infos pour se rep�rer dans l'espace de fa�on orient�e
float x_veh;
float y_veh;
float angle_veh;

//Coordon�es du prochain point � atteindre
//On pourrait aussi rajouter une orientation si on veut, � voir
float delta_x;
float delta_y;

//Vitesses doivent toujours etre dispo pour qu'on puisse y acceder quand on veut
float vg;
float vd;

//Variables utiles pour plusieurs Headers
int etat; //sert � effectuer chaque fonction sans inhiber le reste du programme tout en connaissant l'�tat actuel des actions men�es
unsigned long time; //sert � effectuer des chronos � chaque fois, � rafraichir d�s qu'il ne sert plus
int sens; //sert pour les diff�rentiels entre les roues. 0=droite et 1=gauche

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
    //PARTIE LECTURE o� Aziz et Guillaume envoient x_cons, y-cons et theta_cons
    //Si theta = 0, on en conclut que c'est un ligne droite ou un demi cercle, sinon c'est un pivot d'angle theta

    if (theta != 0) {
        etat = pivot(&theta, &vg, &vd);
    }

    else if ((cos(angle_veh)*sqrt((x_cons-x_veh)*(xcons-x_veh)+(y_cons-y-veh)*(y_cons-y_veh)) == (x_cons-x_veh)) && (sin(angle_veh) * sqrt((x_cons - x_veh) * (xcons - x_veh) + (y_cons - y - veh) * (y_cons - y_veh)) == (y_cons - y_veh)))
}