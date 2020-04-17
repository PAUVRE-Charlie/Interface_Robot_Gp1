# ifndef __LIGNE_DROITE_H__
#define __LIGNE_DROITE_H__

float v_ld;      //vitesse de chaque roue

unsigned long delta_acc;
unsigned long delta_plat;

int demi_cercle(float x, float y, float x_consigne, float y_consigne, float* vg, float* vd)
{

	switch (etat)
	{

		//INITIALISATION
		case 0:
			{
				delta_y = y_consigne - y;


				if (delta_y/v_max > v_max/a_max)
				{
					// Il y a un plateau, on calcul à l'avance les delta_t dont on aura besoin
					delta_acc = v_max / a_max * 1000;
					delta_plat = (delta_y / v_max - v_max / a_max)* 1000;
					etat = 1;
				}

				else
				{
					//Il n'y a pas de plateau
					delta_acc = (sqrt(delta_y / a_max)) * 1000;
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
					v_ld = sqrt(a_max * delta_y / 2) - a_max * (millis() - time) / 1000;
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

	vd = 127 + 128 * v_ld / v_max;
	vg = 127 + 128 * v_ld / v_max;

	return etat;
}



















#endif
