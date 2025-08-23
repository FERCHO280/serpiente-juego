from turtle import Screen, Turtle
import time
import random
import json
import os

CONFIG = {
    "COLORES": {
        "FONDO_MENU": "black",
        "FONDO_JUEGO": "green",
        "CABEZA": "black",
        "CUERPO": "white",
        "COMIDA": "red",
        "TEXTO": "white",
        "TEXTO_SELECCIONADO": "yellow",
        "TEXTO_NORMAL": "gray"
    },
    "DIMENSIONES": {
        "ANCHO": 600,
        "ALTO": 600,
        "BORDE": 290
    },
    "VELOCIDAD": {
        "FACIL": 0.2,
        "NORMAL": 0.15,
        "DIFICIL": 0.1
    },
    "PUNTUACION_COMIDA": 10,
    "ARCHIVO_PUNTUACION": "puntuacion_maxima.json"
}

ESTADOS = {
    "MENU": "menu",
    "JUGANDO": "jugando",
    "GAME_OVER": "game_over"
}

OPCIONES_MENU = [
    {"texto": "Iniciar Juego", "accion": "iniciar_juego"},
    {"texto": "Dificultad: Normal", "valor": "normal", "accion": "cambiar_dificultad"},
    {"texto": "Salir", "accion": "salir"}
]

class JuegoSerpiente:
    def __init__(self):
        self.pantalla = Screen()
        self.configurar_pantalla()
        
        self.segmentos = []
        self.comida = None
        self.mensaje = None
        self.puntuacion_turtle = None
        self.opciones_turtle = []
        
        self.estado = ESTADOS["MENU"]
        self.opcion_seleccionada = 0
        self.puntuacion = 0
        self.max_puntuacion = self.cargar_puntuacion_maxima()
        self.nivel_dificultad = CONFIG["VELOCIDAD"]["NORMAL"]
        
        self.inicializar_elementos()
        self.mostrar_menu()
        
    def configurar_pantalla(self):
        self.pantalla.setup(width=CONFIG["DIMENSIONES"]["ANCHO"], 
                           height=CONFIG["DIMENSIONES"]["ALTO"])
        self.pantalla.bgcolor(CONFIG["COLORES"]["FONDO_MENU"])
        self.pantalla.title("Juego de la Serpiente")
        self.pantalla.tracer(0)
        self.configurar_controles()
    
    def configurar_controles(self):
        self.pantalla.listen()
        # Controles para el juego
        self.pantalla.onkey(self.arriba, "Up")
        self.pantalla.onkey(self.abajo, "Down")
        self.pantalla.onkey(self.izquierda, "Left")
        self.pantalla.onkey(self.derecha, "Right")
        
        # Controles para el menú (espacio para bajar)
        self.pantalla.onkey(self.menu_siguiente, "space")
        self.pantalla.onkey(self.seleccionar_opcion, "Return")
        
        # Controles para reiniciar
        self.pantalla.onkey(self.reiniciar_si, "s")
        self.pantalla.onkey(self.reiniciar_si, "S")
        self.pantalla.onkey(self.reiniciar_no, "n")
        self.pantalla.onkey(self.reiniciar_no, "N")
    
    def inicializar_elementos(self):
        self.mensaje = self.crear_turtle(ocultar=True, color=CONFIG["COLORES"]["TEXTO"])
        
        self.puntuacion_turtle = self.crear_turtle(ocultar=True, color=CONFIG["COLORES"]["TEXTO"])
        self.puntuacion_turtle.goto(0, CONFIG["DIMENSIONES"]["BORDE"] - 20)
        
        for _ in range(len(OPCIONES_MENU)):
            self.opciones_turtle.append(self.crear_turtle(ocultar=True))
        
        self.comida = self.crear_turtle(forma="square", color=CONFIG["COLORES"]["COMIDA"], ocultar=True)
        self.comida.goto(self.generar_posicion_aleatoria())
    
    def crear_turtle(self, forma="circle", color="white", ocultar=False):
        turtle = Turtle(forma)
        turtle.color(color)
        turtle.penup()
        if ocultar:
            turtle.hideturtle()
        return turtle
    
    def generar_posicion_aleatoria(self):
        x = random.randint(-CONFIG["DIMENSIONES"]["BORDE"], CONFIG["DIMENSIONES"]["BORDE"])
        y = random.randint(-CONFIG["DIMENSIONES"]["BORDE"], CONFIG["DIMENSIONES"]["BORDE"])
        return (x, y)
    
    def cargar_puntuacion_maxima(self):
        try:
            if os.path.exists(CONFIG["ARCHIVO_PUNTUACION"]):
                with open(CONFIG["ARCHIVO_PUNTUACION"], 'r') as archivo:
                    datos = json.load(archivo)
                    return datos.get("max_puntuacion", 0)
        except:
            pass
        return 0
    
    def guardar_puntuacion_maxima(self):
        try:
            with open(CONFIG["ARCHIVO_PUNTUACION"], 'w') as archivo:
                json.dump({"max_puntuacion": self.max_puntuacion}, archivo)
        except:
            pass
    
    def arriba(self):
        if self.estado == ESTADOS["JUGANDO"] and self.segmentos[0].heading() != 270:
            self.segmentos[0].setheading(90)

    def abajo(self):
        if self.estado == ESTADOS["JUGANDO"] and self.segmentos[0].heading() != 90:
            self.segmentos[0].setheading(270)

    def izquierda(self):
        if self.estado == ESTADOS["JUGANDO"] and self.segmentos[0].heading() != 0:
            self.segmentos[0].setheading(180)

    def derecha(self):
        if self.estado == ESTADOS["JUGANDO"] and self.segmentos[0].heading() != 180:
            self.segmentos[0].setheading(0)
    
    def mostrar_menu(self):
        self.estado = ESTADOS["MENU"]
        self.pantalla.bgcolor(CONFIG["COLORES"]["FONDO_MENU"])
        self.ocultar_elementos_juego()
        
        self.mensaje.clear()
        self.mensaje.goto(0, 50)
        self.mensaje.write("SNAKE GAME", align="center", font=("Arial", 24, "bold"))
        
        self.opcion_seleccionada = 0
        self.dibujar_menu()
    
    def dibujar_menu(self):
        for i, opcion_turtle in enumerate(self.opciones_turtle):
            opcion_turtle.clear()
            
            color = (CONFIG["COLORES"]["TEXTO_SELECCIONADO"] 
                    if i == self.opcion_seleccionada 
                    else CONFIG["COLORES"]["TEXTO_NORMAL"])
            
            opcion_turtle.color(color)
            opcion_turtle.goto(0, -i * 30)
            opcion_turtle.write(OPCIONES_MENU[i]["texto"], align="center", font=("Arial", 18, "normal"))
    
    def menu_siguiente(self):
        if self.estado == ESTADOS["MENU"]:
            self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(OPCIONES_MENU)
            self.dibujar_menu()
    
    def seleccionar_opcion(self):
        if self.estado == ESTADOS["MENU"]:
            opcion = OPCIONES_MENU[self.opcion_seleccionada]
            accion = opcion["accion"]
            
            if accion == "iniciar_juego":
                self.iniciar_juego()
            elif accion == "cambiar_dificultad":
                self.cambiar_dificultad()
            elif accion == "salir":
                self.pantalla.bye()
    
    def cambiar_dificultad(self):
        dificultades = ["Fácil", "Normal", "Difícil"]
        velocidades = [CONFIG["VELOCIDAD"]["FACIL"], 
                      CONFIG["VELOCIDAD"]["NORMAL"], 
                      CONFIG["VELOCIDAD"]["DIFICIL"]]
        
        texto_actual = OPCIONES_MENU[1]["texto"]
        for i, dificultad in enumerate(dificultades):
            if f"Dificultad: {dificultad}" == texto_actual:
                siguiente = (i + 1) % len(dificultades)
                OPCIONES_MENU[1]["texto"] = f"Dificultad: {dificultades[siguiente]}"
                self.nivel_dificultad = velocidades[siguiente]
                break
        
        self.dibujar_menu()
    
    def iniciar_juego(self):
        self.estado = ESTADOS["JUGANDO"]
        self.pantalla.bgcolor(CONFIG["COLORES"]["FONDO_JUEGO"])
        self.limpiar_mensajes()
        self.reiniciar_serpiente()
        self.comida.showturtle()
        self.comida.goto(self.generar_posicion_aleatoria())
        self.puntuacion = 0
        self.actualizar_puntuacion()
    
    def reiniciar_serpiente(self):
        for segmento in self.segmentos:
            segmento.hideturtle()
        self.segmentos.clear()
        
        cabeza = self.crear_turtle(forma="circle", color=CONFIG["COLORES"]["CABEZA"])
        cabeza.goto(0, 0)
        self.segmentos.append(cabeza)
    
    def ocultar_elementos_juego(self):
        for segmento in self.segmentos:
            segmento.hideturtle()
        self.comida.hideturtle()
    
    def limpiar_mensajes(self):
        self.mensaje.clear()
        for opcion_turtle in self.opciones_turtle:
            opcion_turtle.clear()
    
    def actualizar_puntuacion(self):
        self.puntuacion_turtle.clear()
        self.puntuacion_turtle.write(
            f"Puntuación: {self.puntuacion}  Máxima: {self.max_puntuacion}", 
            align="center", font=("Arial", 16, "normal")
        )
    
    def mover_serpiente(self):
        for i in range(len(self.segmentos) - 1, 0, -1):
            x = self.segmentos[i - 1].xcor()
            y = self.segmentos[i - 1].ycor()
            self.segmentos[i].goto(x, y)
        
        self.segmentos[0].forward(20)
        
        if self.segmentos[0].distance(self.comida) < 15:
            self.comida.goto(self.generar_posicion_aleatoria())
            self.agregar_segmento()
            self.puntuacion += CONFIG["PUNTUACION_COMIDA"]
            self.actualizar_puntuacion()
        
        if (self.segmentos[0].xcor() > CONFIG["DIMENSIONES"]["BORDE"] or 
            self.segmentos[0].xcor() < -CONFIG["DIMENSIONES"]["BORDE"] or
            self.segmentos[0].ycor() > CONFIG["DIMENSIONES"]["BORDE"] or 
            self.segmentos[0].ycor() < -CONFIG["DIMENSIONES"]["BORDE"]):
            self.game_over()
        
        if len(self.segmentos) > 3:
            for segmento in self.segmentos[3:]:
                if self.segmentos[0].distance(segmento) < 10:
                    self.game_over()
                    break
    
    def agregar_segmento(self):
        if self.segmentos:
            ultimo_segmento = self.segmentos[-1]
            nuevo_segmento = self.crear_turtle(forma="circle", color=CONFIG["COLORES"]["CUERPO"])
            nuevo_segmento.goto(ultimo_segmento.xcor(), ultimo_segmento.ycor())
            self.segmentos.append(nuevo_segmento)
    
    def game_over(self):
        self.estado = ESTADOS["GAME_OVER"]
        
        if self.puntuacion > self.max_puntuacion:
            self.max_puntuacion = self.puntuacion
            self.guardar_puntuacion_maxima()
        
        self.mensaje.clear()
        self.mensaje.goto(0, 0)
        self.mensaje.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        
        self.mensaje.goto(0, -40)
        self.mensaje.write("¿Reiniciar? (S/N)", align="center", font=("Arial", 16, "normal"))
    
    def reiniciar_si(self):
        if self.estado == ESTADOS["GAME_OVER"]:
            self.iniciar_juego()
    
    def reiniciar_no(self):
        if self.estado == ESTADOS["GAME_OVER"]:
            self.mostrar_menu()
    
    def ejecutar(self):
        while True:
            self.pantalla.update()
            
            if self.estado == ESTADOS["JUGANDO"]:
                time.sleep(self.nivel_dificultad)
                self.mover_serpiente()

if __name__ == "__main__":
    juego = JuegoSerpiente()
    juego.ejecutar()
