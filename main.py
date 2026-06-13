from dotenv import load_dotenv
from core.chatbot import Chatbot

def main():
    # Cargar variables de entorno (API keys de .env)
    load_dotenv()
    
    print("="*60)
    print("🤖 Chatbot Multi-Proveedor con Fallback Automático")
    print("🌐 Orden de prioridad: OpenAI -> Anthropic -> Google Gemini")
    print("Escribe '/salir' para terminar la sesión de chat.")
    print("="*60 + "\n")
    
    bot = Chatbot()
    
    while True:
        try:
            user_input = input("Tú: ")
            
            # Comando de salida limpio
            if user_input.strip().lower() == '/salir':
                print("Saliendo del chatbot. ¡Hasta pronto!")
                break
                
            # Ignorar entradas vacías
            if not user_input.strip():
                continue
                
            bot.ask(user_input)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nSaliendo del chatbot abruptamente. ¡Adiós!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()