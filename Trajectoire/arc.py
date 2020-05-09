from time import *
from math import *

### Code de la route ###
vmax = 1.0 #en m/s (en vrai je crois que c'est 0.42, a verifier)
amax = 0.5 #en m/s^2 (la ca correspond a la valeur de r et epsmax

### Contraintes techniques ###
wmax = 10.5   #en rad s-1
epsmax = 12.5 #en rad.s-2
r = 0.04      #4cm
L = 0.3       #30cm

### Valeurs caracteristiques ###
tau_plat = vmax / amax

### Variables utiles pour le prgm ###
start = 0.

def arc(x,y,theta,xc,yc):

    global dx, dy
    global dx_veh, dy_veh
    global rayon, rapport, tau

    vdroit = open("vdroit", "w")
    vgauche = open("vgauche", "w")
    essai = open("essai", "w")

    dx = xc-x
    dy = yc-y

    dx_veh = sin(theta)*dy + cos(theta)*dx
    dy_veh = cos(theta)*dy - sin(theta)*dx

    rayon = abs((dx_veh*dx_veh+dy_veh*dy_veh)/(2*dx_veh))
    rapport = (2*rayon - L)/(2*rayon +L)
    d_ext = abs((rayon+L/2)*atan2(dy_veh,rayon-dx_veh))
    tau = sqrt(d_ext/amax)

    essai.write(str(rayon) + " ; " + str(rapport) + " ; " + str(d_ext))

    ### IL Y A UN PLATEAU ###
    if dy_veh/(rayon - dx_veh) >= tan(2*vmax*vmax/amax/(2*rayon+L)):

        start = time()

        while time() - start < tau_plat:
            if dx_veh < 0: #On tourne a gauche
                vdroit.write(str(127 + 127*(time()-start)*amax/vmax) + " ; ")
                vgauche.write(str(127 + abs(rapport)*127*(time()-start)*amax/vmax) + " ; ")
            else:
                vgauche.write(str(127 + 127 * (time() - start) * amax/vmax) + " ; ")
                vdroit.write(str(127 + abs(rapport) * 127 * (time() - start) * amax/vmax) + " ; ")
        vgauche.write("\n")
        vdroit.write("\n")

        start = time()

        while time()-start < d_ext/vmax - tau_plat:
            if dx_veh < 0:  # On tourne a gauche
                vdroit.write(str(255) + " ; ")
                vgauche.write(str(rapport * 255) + " ; ")
            else:
                vgauche.write(str(255) + " ; ")
                vdroit.write(str(rapport * 255) + " ; ")
        vgauche.write("\n")
        vdroit.write("\n")

        start = time()

        while time() - start < tau_plat:
            if dx_veh < 0:  # On tourne a gauche
                vdroit.write(str(255 - 127 * (time() - start) * amax/vmax) + " ; ")
                vgauche.write(str(255*rapport - rapport * 127 * (time() - start) * amax/vmax) + " ; ")
            else:
                vgauche.write(str(255 - 127 * (time() - start) * amax/vmax) + " ; ")
                vdroit.write(str(255 * rapport - rapport * 127 * (time() - start) * amax/vmax) + " ; ")
        vgauche.write("127")
        vdroit.write("127")

        return 0


    ### IL N'Y A PAS DE PLATEAU
    else:

        start = time()

        while time() - start < tau:
            if dx_veh > 0: #On tourne a gauche
                vdroit.write(str(127 + 127*(time()-start)*amax)+ " ; ")
                vgauche.write(str(127 + rapport*127*(time()-start)*amax)+" ; ")
            else:
                vgauche.write(str(127 + 127 * (time() - start) * amax) + " ; ")
                vdroit.write(str(127 + rapport * 127 * (time() - start) * amax) + " ; ")
        vgauche.write("\n")
        vdroit.write("\n")

        start = time()

        while time() - start < tau:
            if dx_veh > 0:  # On tourne a gauche
                vdroit.write(str(127 + 127*amax*tau/vmax - 127 * (time() - start) * amax) + " ; ")
                vgauche.write(str(127 + rapport*(127*amax*tau/vmax - 127 * (time() - start) * amax)) + " ; ")
            else:
                vgauche.write(str(127 + 127 * amax * tau / vmax - 127 * (time() - start) * amax) + " ; ")
                vdroit.write(str(127 + rapport * (127 * amax * tau / vmax - 127 * (time() - start) * amax)) + " ; ")
        vgauche.write("127")
        vdroit.write("127")

        return 0


arc(0,0,1.57,1.5,1.5)




