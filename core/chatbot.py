from core.conversation import ConversationMemory
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider

class Chatbot:
    """Lógica central del Chatbot que gestiona la cascada de proveedores y memoria."""
    
    def __init__(self):
        self.memory = ConversationMemory()
        
        # Inicializamos y ordenamos la cascada de proveedores
        self.providers = [
            ("OpenAI", OpenAIProvider()),
            ("Anthropic", AnthropicProvider()),
            ("Google Gemini", GeminiProvider())
        ]

    def ask(self, user_text: str):
        # 1. Añadimos el nuevo mensaje a la memoria
        self.memory.add_user_message(user_text)
        messages = self.memory.get_history()
        
        # 2. Cascada de Fallback Automático
        for provider_name, provider in self.providers:
            try:
                full_response = ""
                print(f"[{provider_name}]: ", end="", flush=True)
                
                # Consumimos el stream de chunks
                for chunk in provider.stream_response(messages):
                    full_response += chunk
                    print(chunk, end="", flush=True)
                print()
                
                # Si terminamos con éxito, guardamos en memoria y salimos del bucle
                self.memory.add_assistant_message(full_response)
                return
            
            except Exception as e:
                # 3. Captura de errores (Límites de API, caídas, etc)
                print(f"\n[!] Fallo detectado en {provider_name} ({type(e).__name__}): {str(e)}")
                print(f"[*] Haciendo fallback al siguiente proveedor disponible...\n")
                
        # 4. Fallback final si todos los proveedores fallan
        respuesta_preconfigurada = "Lo siento, todos los servicios de Inteligencia Artificial están experimentando problemas en este momento. Por favor, revisa tu conexión o intenta más tarde."
        print(f"[Sistema]: {respuesta_preconfigurada}")
        self.memory.add_assistant_message(respuesta_preconfigurada)