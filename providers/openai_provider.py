import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        # El SDK lee automáticamente de OPENAI_API_KEY si no se le pasa
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5" # Utilizable desde gpt-4o hasta gpt-5
        
    def stream_response(self, messages: list):
        """Usa la nueva API Responses en modo streaming."""
        stream = self.client.responses.create(
            model=self.model,
            input=messages,
            stream=True
        )
        
        for event in stream:
            # Extracción del delta de texto en la API Responses
            event_type = getattr(event, "type", "")
            if event_type == "response.output_text.delta":
                yield getattr(event, "output_text_delta", "")
            elif isinstance(event, dict) and event.get("type") == "response.output_text.delta":
                yield event.get("output_text_delta", "")