from turtle import Screen, Turtle
import time
import random

segmentos = []

# Funciones para mover la serpiente
def arriba():
    if segmento_cabeza.heading() != 270:
        segmento_cabeza.setheading(90)

def abajo():
    if segmento_cabeza.heading() != 90:
        segmento_cabeza.setheading(270)

def izquierda():
    if segmento_cabeza.heading() != 0:
        segmento_cabeza.setheading(180)

def derecha():
    if segmento_cabeza.heading() != 180:
        segmento_cabeza.setheading(0)

# Configuración de la pantalla
pantalla = Screen()
pantalla.setup(width=600, height=600)
pantalla.bgcolor("green")
pantalla.title("Juego de la Serpiente")
pantalla.tracer(0)

# Crear la cabeza de la serpiente
segmento_cabeza = Turtle("triangle")
segmento_cabeza.color("black")
segmento_cabeza.penup()
segmentos.append(segmento_cabeza)

# Crear la comida
comida = Turtle('circle')
comida.color("red")
comida.penup()
comida.goto(random.randint(-280, 280), random.randint(-280, 280))

# Turtle para mostrar mensaje de Game Over
mensaje = Turtle()
mensaje.hideturtle()
mensaje.color("black")
mensaje.penup()

# Asignar controles
pantalla.listen()
pantalla.onkey(arriba, "Up")
pantalla.onkey(abajo, "Down")
pantalla.onkey(izquierda, "Left")
pantalla.onkey(derecha, "Right")

# Variable de control del juego
juego_activo = True

# Bucle principal
while juego_activo:
    pantalla.update()
    time.sleep(0.20)

    # Mover el cuerpo de la serpiente
    for i in range(len(segmentos) - 1, 0, -1):
        x = segmentos[i - 1].xcor()
        y = segmentos[i - 1].ycor()
        segmentos[i].goto(x, y)

    segmento_cabeza.forward(20)

    # Detectar colisión con comida
    if segmento_cabeza.distance(comida) < 15:
        comida.goto(random.randint(-280, 280), random.randint(-280, 280))
        nuevo_segmento = Turtle("square")
        nuevo_segmento.color("white")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)

    # Detectar colisión con paredes
    if (segmento_cabeza.xcor() > 290 or segmento_cabeza.xcor() < -290 or
        segmento_cabeza.ycor() > 290 or segmento_cabeza.ycor() < -290):
        mensaje.goto(0, 0)
        mensaje.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        juego_activo = False
        continue  # Saltar comprobación de colisión con cuerpo

    # Detectar colisión con el cuerpo
    for segmento in segmentos[1:]:
        if segmento_cabeza.distance(segmento) < 10:
            mensaje.goto(0, 0)
            mensaje.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
            juego_activo = False
            break

pantalla.exitonclick()
