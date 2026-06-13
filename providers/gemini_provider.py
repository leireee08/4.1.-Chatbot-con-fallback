import os
from google import genai

class GeminiProvider:
    def __init__(self):
        # Utiliza la nueva biblioteca google-genai
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-pro"
        
    def stream_response(self, messages: list):
        """Mapea el formato de mensajes al esperado por Gemini en modo streaming."""
        gemini_contents = []
        for m in messages:
            # Gemini requiere rol 'user' o 'model'
            role = "model" if m["role"] == "assistant" else "user"
            gemini_contents.append({"role": role, "parts": [{"text": m["content"]}]})
            
        response_stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=gemini_contents
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text