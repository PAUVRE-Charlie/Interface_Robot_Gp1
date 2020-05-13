from time import *
from math import *

### Contraintes techniques
wmax = 10.5   #en rad s-1
epsmax = 12.5 #en rad.s-2
r = 0.04      #4cm
L = 0.3       #30cm

start = 0

### ATTENTION angle en radian, ou sinon le convertir mais il faut etre coherent ###


def rotation(angle):
    global tau_plat
    global tau
    vdroit = open("vdroit", "w")
    vgauche = open("vgauche", "w")

    tau_plat = wmax/epsmax
    tau = sqrt(L*abs(angle)/(2*r*epsmax))


    ###IL N'Y A PAS DE PLATEAU
    if abs(angle) < 2*r*epsmax*tau_plat*tau_plat/L:

        start = time()

        ### SI ON PIVOTE VERS LA GAUCHE ###
        if angle >= 0:

            while time() - start < tau:
                vdroit.write(str(127 + 127/wmax * (time()-start)*epsmax) + " ; ")
                vgauche.write(str(127 - 127 / wmax * (time() - start) * epsmax) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time()- start < tau:
                vdroit.write(str(127 + 127/wmax * (tau - (time()-start))*epsmax) + " ; ")
                vgauche.write(str(127 - 127/wmax * (tau - (time()-start))*epsmax) + " ; ")
                sleep(0.01)
            vdroit.write(str(127))
            vgauche.write(str(127))

            return 0

        ###SI ON PIVOTE VERS LA DROITE
        else:

            while time() - start < tau:
                vgauche.write(str(127 + 127 / wmax * (time() - start) * epsmax) + " ; ")
                vdroit.write(str(127 - 127 / wmax * (time() - start) * epsmax) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time() - start < tau:
                vgauche.write(str(127 + 127 / wmax * (tau - (time() - start)) * epsmax) + " ; ")
                vdroit.write(str(127 - 127 / wmax * (tau - (time() - start)) * epsmax) + " ; ")
                sleep(0.01)
            vdroit.write(str(127))
            vgauche.write(str(127))

            return 0



    ### IL Y A UN PLATEAU
    else:

        start = time()

        ### SI ON PIVOTE VERS LA GAUCHE ###
        if angle >= 0:

            while time() - start < tau_plat:
                vdroit.write(str(127 + 127 / wmax * (time() - start) * epsmax) + " ; ")
                vgauche.write(str(127 - 127 / wmax * (time() - start) * epsmax) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time() - start < (abs(angle) - 2*r*epsmax*tau_plat*tau_plat/L)/wmax:
                vdroit.write(str(254) + " ; ")
                vgauche.write(str(0) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time() - start < tau_plat:
                vdroit.write(str(254- 127 *(time()-start)/tau_plat) + " ; ")
                vgauche.write(str(127 *(time()-start)/tau_plat) + " ; ")
                sleep(0.01)
            vdroit.write(str(127))
            vgauche.write(str(127))

            return 0

        ### SI ON PIVOTE VERS LA DROITE ###
        else:

            while time() - start < tau_plat:
                vgauche.write(str(127 + 127 / wmax * (time() - start) * epsmax) + " ; ")
                vdroit.write(str(127 - 127 / wmax * (time() - start) * epsmax) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time() - start < (abs(angle) - 2 * r * epsmax * tau_plat * tau_plat / L) / wmax:
                vgauche.write(str(254) + " ; ")
                vdroit.write(str(0) + " ; ")
                sleep(0.01)
            vdroit.write("\n")
            vgauche.write("\n")

            start = time()

            while time() - start < tau_plat:
                vgauche.write(str(254 - 127 * (time() - start) / tau_plat) + " ; ")
                vdroit.write(str(127 * (time() - start) / tau_plat) + " ; ")
                sleep(0.01)
            vdroit.write(str(127))
            vgauche.write(str(127))

            return 0


rotation(-3.1416)
