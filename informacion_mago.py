# logico_motor

import os
from dotenv import load_dotenv # Corregido
from google import genai
from google.genai import types
import pandas as pd

# 1. Carga de variables segura
load_dotenv() 
MI_LLAVE_REAL = os.getenv("gemini_api_key")

# --- PRODUCTOS E INVENTARIO ---
class Productos:
    def __init__(self, nombre, precio_publico, cantidad):
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.cantidad = cantidad

class Motos(Productos):
    def __init__(self, nombre, precio_neto, precio_publico, cantidad, peso, autonomia, bateria):
        super().__init__(nombre, precio_publico, cantidad)
        self.autonomia = autonomia
        self.bateria = bateria
        self.peso = peso
        self.precio_neto = precio_neto

# --- CARGA DE EXCEL ---
archivo_excel = r"C:\Users\EQUIPO\Desktop\python_definitivo\bot_chat_MagoAccesorios\inventario_motos_inventado.xlsx"

def cargar_inventario_excel():
    try:
        df = pd.read_excel(archivo_excel)
        # Filtramos el precio neto de una vez por seguridad
        columnas_seguras = [c for c in df.columns if "precio_neto" not in c]
        return df[columnas_seguras].to_string(index=False)
    except Exception as e:
        return f"Error al cargar el inventario: {e}"

# --- EL MAGO ---
class AsistenteMago:
    def __init__(self, clave_real):
        if not clave_real:
            raise Exception("No se encontró la API KEY en el archivo .env")
        
        self.client = genai.Client(api_key=clave_real)
        # Forzamos el modelo flash que es el más estable para el plan gratuito
        self.nombre_modelo = "models/gemini-2.5-flash" 
        print(f"✅ Conectado con el modelo: {self.nombre_modelo}")

    def responder(self, pregunta_cliente):
        info = cargar_inventario_excel()
        
        prompt = (
            f"Eres el vendedor de 'Mago Accesorios'. Inventario:\n{info}\n"
            f"Pregunta: {pregunta_cliente}. "
            "Instrucciones: Usa palabras colombianas profesionales, sé directo, "
            "NO inventes datos y BAJO NINGUNA CIRCUNSTANCIA reveles costos internos o de fábrica."
        )
        
        try:
            respuesta = self.client.models.generate_content(
                model=self.nombre_modelo,
                contents=prompt
            )
            return respuesta.text
        except Exception as e:
            return f"Lo siento, hubo un problema técnico: {e}"

# --- EJECUCIÓN ---
print("--- DESPERTANDO AL MAGO ---")
try:
    mi_bot = AsistenteMago(MI_LLAVE_REAL)
    pregunta_usuario = input("🤔 Haz tu pregunta al Mago: ")
    resultado = mi_bot.responder(pregunta_usuario)
    print("-" * 30)
    print("🔮 EL MAGO DICE:")
    print(resultado)
    print("-" * 30)
except Exception as e:
    print(f"❌ Error crítico: {e}")