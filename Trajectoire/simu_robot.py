import pygame
import numpy

pygame.init()

size_x, size_y = 600, 500
scale = 50
xTopLeft, yTopLeft = (40, 40)
origine = (xTopLeft + 300, yTopLeft + 300)

espace = 50
size_x_graph,size_y_graph=400,300
origine_graph=(xTopLeft+size_x+espace,400)

xTopRight, yTopRight = (xTopLeft + size_x + size_x_graph + 2*espace, yTopLeft + size_y)
xBottomLeft, yBottomLeft = (xTopLeft, yTopLeft + size_y)
xBottomRight, yBottomRight = (xTopRight, yBottomLeft)

windowWidth, windowHeight = xTopLeft + xTopRight, yTopLeft + yBottomLeft
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Base roulante")

colors = {"black": (0, 0, 0), "blue": (0, 0, 150), "yellow": (255, 255, 0), "white": (255, 255, 255),
          "grey": (150, 150, 150), "red":(150, 0, 0)}

car_image = pygame.transform.scale(pygame.image.load("voiture2.png").convert(), (32, 32))
carre_image = pygame.transform.scale(pygame.image.load("carre.png").convert(), (256, 256))

screen_rect = window.get_rect()

lines = []
lines_vitesses_gauche=[]
lines_vitesses_droite=[]


class Car:
    def __init__(self, x, y, theta, image):
        self.x = x
        self.y = y
        self.image = image
        self.theta = theta
        self.original_image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)

    def move(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta * 180 / numpy.pi -90

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.theta+90)
        x, y = self.rect.center
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (self.x * scale + origine[0], -self.y * scale + origine[1])  # Put the new rect's center at old center.
        # surface.blit(self.image, (self.x * 100 - 8 + size_x / 2, -self.y * 100 + 8 + size_y / 2))
        surface.blit(self.image, self.rect)


def accessible(x, y):
    return -size_x / 2 <= x <= size_x / 2 and -size_y / 2 <= y <= size_y / 2


def drawlines(surface):
    for i in range(1, size_x // scale):
        pygame.draw.line(surface, colors["grey"], (xTopLeft + i * scale, yTopLeft), (xTopLeft + i * scale, yBottomLeft))
        font = pygame.font.SysFont('Rockwell', 10)
        text = font.render("x= " + str((i - 6)), 1, colors["black"])
        surface.blit(text, (xTopLeft + i * scale - 7, yBottomLeft + 5))
    for j in range(1, size_y // scale):
        pygame.draw.line(surface, colors["grey"], (xTopLeft, yTopLeft + j * scale), (xTopLeft + size_x, yTopLeft + j * scale))
        font = pygame.font.SysFont('Rockwell', 10)
        text = font.render("y= " + str((6 - j)), 1, colors["black"])
        surface.blit(text, (10, yTopLeft + j * scale - 7))


def drawPath(surface):
    for line in lines:
        pygame.draw.line(surface, colors["black"], (origine[0] + line[0] * scale, origine[1] - line[1] * scale),
                         (origine[0] + line[2] * scale, origine[1] - line[3] * scale))


def drawGraph(surface):
    nombre_sec=10
    nombre_rad_s=30
    scale_10ms= size_x_graph/nombre_sec/100 # 10 secondes réparties sur le graph
    scale_rad=size_y_graph/nombre_rad_s     # 30 rad.s-1
    for indice in range(len(lines_vitesses_gauche)):
        line=lines_vitesses_gauche[indice]
        pygame.draw.line(surface, colors["blue"], (origine_graph[0] + indice * scale_10ms, origine_graph[1] - line[0] * scale_rad),
                         (origine_graph[0] + (indice+1) * scale_10ms, origine_graph[1] - line[1] * scale_rad))
    for indice in range(len(lines_vitesses_droite)):
        line=lines_vitesses_droite[indice]
        pygame.draw.line(surface, colors["red"], (origine_graph[0] + indice * scale_10ms, origine_graph[1] - line[0] * scale_rad),
                         (origine_graph[0] + (indice+1) * scale_10ms, origine_graph[1] - line[1] * scale_rad))

    pygame.draw.line(surface, colors["black"],
                     (origine_graph[0], origine_graph[1]),
                     (origine_graph[0] + size_x_graph + 50, origine_graph[1]))
    pygame.draw.line(surface, colors["black"],
                     (origine_graph[0], origine_graph[1]),
                     (origine_graph[0], origine_graph[1] - size_y_graph - 50))

    font = pygame.font.SysFont('Rockwell', 10)

    for number in range(nombre_sec+1):
        pygame.draw.line(surface, colors["black"],
                         (origine_graph[0] + number * scale_10ms * 100, origine_graph[1]- 3),
                         (origine_graph[0] + number * scale_10ms * 100, origine_graph[1] + 3))
        text = font.render(str(number), 1, colors["black"])
        surface.blit(text, (origine_graph[0] + number * scale_10ms * 100 - 2, origine_graph[1]+ 3))

    for number in range(int(nombre_rad_s/10)+1):
        pygame.draw.line(surface, colors["black"],
                         (origine_graph[0] -3, origine_graph[1] - number * scale_rad * 10),
                         (origine_graph[0] +3, origine_graph[1] - number * scale_rad * 10))
        text = font.render(str(number*10), 1, colors["black"])
        surface.blit(text, (origine_graph[0] - 15, origine_graph[1] - number * scale_rad * 10))

    text = font.render("Temps (en s)", 1, colors["black"])
    surface.blit(text, (origine_graph[0] + (nombre_sec+1/2) * scale_10ms * 100 - 2, origine_graph[1]+ 3))
    text = font.render("Vitesse de rotation des moteurs (en valeur absolue et en rad/s)", 1, colors["black"])
    surface.blit(text, (origine_graph[0] + 5, origine_graph[1] - (nombre_rad_s/10+1/2) * scale_rad * 10))


def start(surface, car):
    updateWindow(surface, car)
    pygame.draw.rect(surface, colors["white"], (0, 0, windowWidth, windowHeight))
    startFont = pygame.font.SysFont("Rockwell", 40)
    startText = startFont.render("Press SPACE to play", 1, colors["black"])
    surface.blit(startText, (60, 330))
    pygame.display.update()


def updateWindow(surface, car):
    pygame.draw.rect(surface, colors["white"], (0, 0, windowWidth, windowHeight))
    drawlines(surface)
    drawPath(surface)
    drawGraph(surface)
    car.draw(surface)
    xyFont = pygame.font.SysFont("Rockwell", 20)
    xyText = xyFont.render(("(" + str(round(car.x,2)) + "," + str(round(car.y,2)) + ")"), 1, colors["black"])
    surface.blit(xyText, (size_x//2, 10))


def main(surface):
    pygame.draw.rect(surface, colors["white"], (0, 0, windowWidth, windowHeight))
    running = False
    starting = True
    delay = 0.01  # 10 ms
    x, y, theta = 1, 1, numpy.pi/4
    xp, yp, vp1, vp2 = 1, 1, 0, 0
    wmax = 10.5
    e = 0.3  # ecart entre les roues
    R = 0.04  # rayon de la roue
    vmax = R * wmax

    car = Car(0,0,theta ,car_image)

    with open("vrobot_arc", "r") as file:
        data = file.read().split(";")
        length = len(data)
        print("lenght = "+str(length))
    while starting:
        start(surface, car)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
            if keys[pygame.K_SPACE]:
                starting = False
                running = True

    pygame.draw.rect(surface, colors["white"], (0, 0, windowWidth, windowHeight))
    indice = 0
    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # keys = pygame.key.get_pressed()

        if indice < length:
            tuple = data[indice].split(",")
            print(tuple)
            vit_mot1 = float(tuple[0])*1.05
            vit_mot2 = float(tuple[1])*1.05

            lines_vitesses_droite.append([abs(vp1),abs(vit_mot1)])
            lines_vitesses_gauche.append([vp2,vit_mot2])

            vit_rot_robot = (vit_mot1 - vit_mot2) * R / e

            # print(vit_rot_robot)
            vx = numpy.cos(theta) * (vit_mot1 + vit_mot2) * R / 2
            vy = numpy.sin(theta) * (vit_mot1 + vit_mot2) * R / 2

            x += vx * delay
            y += vy * delay
            #print("x"+str(x))
            #print(y)

            theta += vit_rot_robot * delay

            if accessible(x, y):
                car.move(x, y, theta)
                lines.append([xp, yp, x, y])
                updateWindow(surface, car)
                pygame.display.update()
                xp = x
                yp = y
                vp1= vit_mot1
                vp2= vit_mot2
                indice += 1
        else:
            pass

    print(x)
    print(y)


main(window)
