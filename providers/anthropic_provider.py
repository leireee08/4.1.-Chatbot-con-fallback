import os
from anthropic import Anthropic

class AnthropicProvider:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-7-sonnet-latest"
        
    def stream_response(self, messages: list):
        """Usa la API de Messages en modo streaming."""
        # Claude espera únicamente los roles 'user' o 'assistant'. 
        anthropic_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
        
        with self.client.messages.stream(
            max_tokens=2048,
            messages=anthropic_messages,
            model=self.model,
        ) as stream:
            for text in stream.text_stream:
                yield text