# ifndef __LIGNE_DROITE_H__
#define __LIGNE_DROITE_H__

float v_ld;      //vitesse de chaque roue



int ligne_droite(float distance, float* vg, float* vd)
{

	switch (etat)
	{

		//INITIALISATION
	case 0:
	{
		if (distance < 0) {
			distance = abs(distance);
			sens = 0; //marche arriere
		}

		else {
			sens = 1; //marche avant
		}

		if (distance / (2*v_max) > v_max / a_max)
		{
			// Il y a un plateau, on calcul à l'avance les delta_t dont on aura besoin
			delta_acc = v_max / a_max * 1000;
			delta_plat = (distance - 2 * v_max * delta_acc) / v_max * 1000;
			etat = 1;
		}

		else
		{
			//Il n'y a pas de plateau
			delta_acc = (sqrt(2*distance / a_max)) * 1000;
			etat = 4;
		}

		time = millis();
		break;
	}



	//IL Y A UN PLATEAU, ET DONC 3 PHASES ASSOCIEES
	case 1:
	{
		if (millis() - time < delta_acc)
		{
			v_ld = a_max * (millis() - time) / 1000;
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
			v_ld = v_max;
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
			v_ld = v_max - a_max * (millis() - time) / 1000;
		}
		else
		{
			v_ld = 0;
			etat = 0;
		}
		break;
	}//fin cas plateau


//IL N'Y A PAS DE PLATEAU
	case 4:
	{
		if (millis() - time < delta_acc)
		{
			v_ld = a_max * (millis() - time) / 1000;
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
			v_ld = sqrt(a_max * distance / 2) - a_max * (millis() - time) / 1000;
		}
		else
		{
			v_ld = 0;
			etat = 0;
		}
		break;
	} //fin cas plateau
	}


	//ATTRIBUTION DES VITESSES

	if (sens == 1) {
		vd = 127 + 128 * v_ld / v_max;
		vg = 127 + 128 * v_ld / v_max;
	}

	else {
		vd = 127 - 128 * v_ld / v_max;
		vg = 127 - 128 * v_ld / v_max;
	}
	return etat;
}


#endif
