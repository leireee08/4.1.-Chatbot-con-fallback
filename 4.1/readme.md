# Chatbot Resiliente Multi-Proveedor

Este proyecto es un chatbot en Python basado en consola que integra OpenAI, Anthropic Claude y Google Gemini. Presenta una arquitectura tolerante a fallos, lo que le permite realizar "fallback" si la API de un proveedor cae o agota sus cuotas.

## Cómo ejecutar

1. Instala las dependencias: `pip install -r requirements.txt`
2. Configura las claves de los proveedores en un archivo `.env`
3. Ejecuta el chatbot interactivo: `python main.py`
4. Teclea `/salir` cuando termines.