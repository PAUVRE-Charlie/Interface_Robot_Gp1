#ifndef __DEMI_CERCLE_H__
#define __DEMI_CERCLE_H__

float lambda_dc; //rapport à conserver pour effectuer un demi-cercle
float v_dc;      //vitesse de la roue interieur

float dg_dc;//Distance entre la roue gauche et la consigne
float dd_dc;//Distance entre la roue droite et la consigne, en soit inutile, une seule suffit, mais si jamais on en a besoin à un moment elle est là

int demi_cercle(float diametre, float *vg, float *vd) {

	switch (etat) {

		//INITIALISATION
		case 0: {

			if (diametre < 0) {
				diametre = abs(diametre);
				sens = 0; //vers la droite
			}

			else {
				sens = 1; //vers la gauche
			}

			lambda_dc = (diametre + e) / (diametre - e);

			if (diametre >= 2 * (v_max * v_max) / (lambda_dc * lambda_dc * pi * a_max) + e) {
				// Il y a un plateau, on calcul à l'avance les delta_t dont on aura besoin
				delta_acc = v_max / (lambda_dc * a_max)*1000; 
				delta_plat = ((diametre - e) * pi * lambda_dc / (2 * v_max) - v_max / (lambda_dc * a_max))*1000;
				etat = 1;
			}

			else {
				//Il n'y a pas de plateau
				delta_acc = (sqrt(2 * pi * (diametre - e) / a_max))*1000;
				etat = 4;
			}

			time = millis();
			break;
		}


	
	//IL Y A UN PLATEAU, ET DONC 3 PHASES ASSOCIEES
		case 1: {
			if (millis() - time < delta_acc) {
				v_dc = a_max * (millis() - time) / 1000;
			}
			else {
				etat = 2;
				time = millis();
			}

			break;
		}

		case 2: {
			if (millis() - time < delta_plat) {
				v_dc = v_max / lambda_dc;
			}
			else {
				etat = 3;
				time = millis();
			}

			break;
		}
		
		case 3: {
			if (millis() - time < delta_acc) {
				v_dc = v_max/lambda_dc - a_max * (millis() - time) / 1000;
			}
			else {
				v_dc = 0;
				etat = 0;
			}
			break;
		}//fin cas plateau


	//IL N'Y A PAS DE PLATEAU
		case 4: {
			if (millis() - time < delta_acc) {
				v_dc = a_max * (millis() - time) / 1000;
			}
			else {
				etat = 5;
				time = millis();
			}

			break;
		}

		case 5: {
			if (millis() - time < delta_acc) {
				v_dc = sqrt(a_max * 2 * (diametre - e) * pi) / 2 - a_max * (millis() - time) / 1000;
			}
			else {
				v_dc = 0;
				etat = 0;
			}
			break;
		} //fin cas plateau
	}


	//ATTRIBUTION DES VITESSES

	if (sens == 0) {
		vd = 127 + 128 * v_dc / v_max;
		vg = 127 + 128 * v_dc * lambda_dc / v_max;
	}

	else {
		vg = 127 + 128 * v_dc / v_max;
		vd = 127 + 128 * v_dc * lambda_dc / v_max;
	}

	return etat;
}

#endif

