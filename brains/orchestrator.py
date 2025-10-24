# brains/orchestrator.py

from transformers import pipeline

class Orchestrator:
    """
    El Orquestador sintetiza respuestas de múltiples cerebros, considerando el contexto
    de la conversación para generar una respuesta final coherente y personalizada.
    """

    def __init__(self, model_name: str):
        self.generator = pipeline('text2text-generation', model=model_name)
        self.system_prompt = (
            "Eres Helpie, un asistente experto en primeros auxilios, amigable, profesional y gentil. "
            "Tu misión es enseñar y reforzar conocimientos, nunca reemplazar a un profesional médico. "
            "Tus respuestas se basan en guías de OPS, Cruz Roja, AHA y otras autoridades. "
            "A continuación, recibirás el historial de conversación y la información de los cerebros especialistas. "
            "Tu tarea es sintetizar esto en una respuesta clara, precisa y empática. "
            "Si el usuario hace una pregunta de seguimiento, úsala para dar una respuesta más específica. "
            "Mantén un tono de seguridad y siempre incluye un recordatorio de que tu ayuda es educativa. "
            "Responde en el siguiente formato: "
            "'[Saludo amigable y contextual]. [Respuesta sintetizada]. [Recordatorio de seguridad y descargo de responsabilidad].'"
        )

    def synthesize(self, brain_responses: list[str], conversation_history: list[tuple[str, str]] = None) -> str:
        """
        Combina las respuestas de los cerebros y el historial en una sola respuesta final.
        """
        if not brain_responses:
            return "Lo siento, no he podido procesar tu solicitud en este momento."

        # Construir el contexto de la conversación
        history_text = ""
        if conversation_history:
            history_text = "\n--- HISTORIAL DE CONVERSACIÓN ---\n"
            for i, (user, bot) in enumerate(conversation_history[-2:]): # Usar las últimas 2 interacciones
                history_text += f"Turno {i+1}:\nUsuario: {user}\nHelpie: {bot}\n"
            history_text += "\n"

        # Unir todas las respuestas de los cerebros
        context = "\n\n--- INFORMACIÓN DE LOS CEREBROS ESPECIALISTAS ---\n".join(brain_responses)
        
        # Crear el prompt completo para el modelo
        full_prompt = (
            f"{self.system_prompt}\n\n"
            f"{history_text}"
            f"INFORMACIÓN A SINTETIZAR:\n{context}\n\n"
            f"RESPUESTA SINTETIZADA:"
        )

        # Generar la respuesta
        result = self.generator(full_prompt, max_length=512, num_beams=4, early_stopping=True)
        final_response = result[0]['generated_text']
        
        return final_response.strip()
