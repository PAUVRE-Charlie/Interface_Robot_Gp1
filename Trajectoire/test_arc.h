ndef __ARC_H__
#define __ARC_H__

double dx;
double dy;
double dx_veh;
double dy_veh;
double v_ext = 0.;

double lambda_arc; //Rappel: Ici, Vitesse_gauche = lambda *  Vitesse_droite

int arc(double x_veh, double y_veh, double x_cons, double y_cons, float theta_veh, int *vg, int *vd) {

	switch (etat) {

		case 0: {
			dx = x_cons - x_veh;
			dy = y_cons - y_veh;

			dx_veh = sin(theta_veh) * dx - cos(theta_veh) * dy;
			dy_veh = abs(cos(theta_veh) * dx + sin(theta_veh) * dy);

			lambda_arc = (1 + e * dx_veh / (dy_veh * dy_veh)) / (1 - e * dx_veh / (delta_y * delta_y));

			if (dx_veh > 0) { //On tourne vers la droite du robot
				sens = 0;
			}
			else {           //On tourne vers la gauche du robot
				sens = 1;
			}

			double angle_final = arcsin(sqrt(dy_veh * dy_veh / (dx_veh * dx_veh + dy_veh * dy_veh))) + arctan(dx_veh / dy_veh);
			
			//Pour savoir si il y aura un plateau, on va étudier la roue extérieure
			double dext = (abs(dx_veh) + e / 2) * angle_final;
			lambda_arc = 1 - 2 * e * sin(angle_final) / (e * sin(angle_final) - 2 * dy_veh);

			if (dext / v_max > v_max / a_max) {
				// Il y a un plateau, on calcul à l'avance les delta_t dont on aura besoin
				delta_acc = v_max / a_max * 1000;
				delta_plat = (dext - 2 * v_max * delta_acc) / v_max * 1000;
				etat = 1;
			}

			else {
				delta_acc = (sqrt(2 * dext / a_max)) * 1000;
				etat = 4;
			}

			time = millis();
			break;
		}

		case 1: {
			if (millis() - time < delta_acc){
				v_ext = a_max * (millis() - time) / 1000;
			}
			else
			{
				etat = 2;
				time = millis();
			}

			break;
		}

		case 2:
		{
			if (millis() - time < delta_plat)
			{
				v_ext = v_max;
			}
			else
			{
				etat = 3;
				time = millis();
			}

			break;
		}

		case 3:
		{
			if (millis() - time < delta_acc)
			{
				v_ext = v_max - a_max * (millis() - time) / 1000;
			}
			else
			{
				v_ext = 0;
				etat = 0;
			}
			break;
		}//fin cas plateau
	
		 //IL Y A UN PLATEAU
		case 4:
		{
			if (millis() - time < delta_acc)
			{
				v_ext = a_max * (millis() - time) / 1000;
			}
			else
			{
				etat = 5;
				time = millis();
			}

			break;
		}

		case 5:
		{
			if (millis() - time < delta_acc)
			{
				v_ext = sqrt(a_max * distance) - a_max * (millis() - time) / 1000;
			}
			else
			{
				v_ext = 0;
				etat = 0;
			}
			break;
		} //fin cas plateau

	}
	
	if (sens == 1) { //On tourne à gaauche
		vd = 127 + 128 * v_ext / v_max;
		vg = vd * lambda_arc;
	}

	else { //On tourne à droite
		vg = 127 + 128 * v_ext / v_max;
		vd = vg / lambda_arc;
	}
	return etat;
}


#endif
