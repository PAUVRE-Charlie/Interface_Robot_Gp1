#ifndef __PIVOT_H__
#define  __PIVOT_H__


float t_rot;
float v_p;


//On va effectuer une rotation ultra smooth, accel max divisée par 2
//Dans ce cas, même dans le pire des cas, un demi-tour, la vitesse maximale au niveau d'une roue serait de 0.4 m/s
// On va toujours partir du prncipe qu'on en va pas atteindre un plateau donc


int pivot(float theta, float *vg, float *vd) {
    
    switch (etat) {

        case 0: {//On est vient de recevoir l'ordre
            t_rot = sqrt(4 * e * abs(theta) / a_max);

            if (theta < 0) {
                sens = 0; //On tourne vers la droite
            }

            else {
                sens = 1; //On tourne vers la gauche
            }
            time = millis();
            etat = 1;
            break;
        }

        case 1: {//Phase d'acceleration
            if (millis() >= time + t_rot / 2) {
                time = millis();
                etat = 2;
            }
            else {
                vitesse = a_max * (millis() - time) / 2000;
            }
            break;
        }

        case 2: {//Phase de décélération
            if (millis() >= time + t_rot / 2) {
                time = millis();
                etat = 0;
                v_p = 0;
                theta = 0;
            }
            else {
                v_p = a_max * (t_rot / 2 - millis() + time)/2000;
            }
            break;
        }

    }

    if (sens == 0) { //on tourne à droite
        vd = 127 - 127 * v_p / v_max);
        vg = 127 + 127 * v_p / v_max);
    }

    else { //on tourne à gauche
        vd = 127 - 127 * v_p / v_max);
        vg = 127 + 127 * v_p / v_max);
    }

    return etat;
}

#endif

