class ConversationMemory:
    """Clase encargada de gestionar el historial de la conversación en memoria."""
    
    def __init__(self):
        self.history = []

    def add_user_message(self, text: str):
        self.history.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        self.history.append({"role": "assistant", "content": text})

    def get_history(self) -> list:
        return self.history