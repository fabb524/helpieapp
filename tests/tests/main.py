# main.py

# ... (imports anteriores) ...
from config import CHROMA_DB_PATH
import os

def main():
    """
    Función principal que ejecuta la aplicación Helpie Enterprise.
    """
    print("🚀 Inicializando Helpie Enterprise, tu asistente de primeros auxilios con IA...")

    # Verificar si la base de datos vectorial existe
    if not os.path.exists(CHROMA_DB_PATH):
        print("⚠️ La base de datos vectorial no se encuentra.")
        print("Por favor, ejecuta primero 'python setup_knowledge_base.py' para crearla.")
        return

    # 1. Inicializar todos los componentes
    supervisor = Supervisor()
    orchestrator = Orchestrator(model_name=ORCHESTRATOR_MODEL_NAME)
    brains = { ... } # (Inicialización de cerebros igual que antes)

    print("✅ Todos los sistemas listos. ¡Hola! Soy Helpie, tu asistente de primeros auxilios.")
    print("Puedes preguntarme sobre emergencias, heridas, apoyo emocional, o pedir que analice una foto.")
    print("Escribe 'salir' para terminar la conversación.")
    print("-" * 50)

    # 2. Inicializar el historial de conversación
    conversation_history = []

    while True:
        try:
            # 1. El usuario hace una pregunta
            user_query = input("Tú: ")

            if user_query.lower() in ['salir', 'exit', 'adios']:
                print("Helpie: Cuídate mucho. ¡Recuerda siempre estar preparado!")
                break

            # ... (lógica de enrutamiento y procesamiento de cerebros igual que antes) ...
            # La única diferencia es que pasamos el historial al orquestador.

            processed_query, source_lang = brains['c6_language'].detect_and_translate_to_english(user_query)
            selected_brains = supervisor.route(processed_query)
            
            print(f"\n[DEBUG] Consulta procesada: '{processed_query}' | Idioma: '{source_lang}' | Cerebros: {selected_brains}\n")

            brain_responses = []
            # ... (bucle de procesamiento de cerebros igual que antes) ...
            for brain_name in selected_brains:
                if brain_name == 'c6_language': continue
                if brain_name == 'c4_media':
                    # ... (lógica de archivo igual que antes) ...
                    file_path = input("Ruta del archivo: ")
                    if os.path.exists(file_path):
                        response = brains[brain_name].process(file_path)
                        brain_responses.append(response)
                    else:
                        brain_responses.append("No encontré el archivo.")
                else:
                    response = brains[brain_name].process(processed_query)
                    brain_responses.append(response)
            
            # 4. El orquestador junta las respuestas, ahora con contexto
            if brain_responses:
                final_response_en = orchestrator.synthesize(brain_responses, conversation_history)
                final_response = brains['c6_language'].translate_from_english(final_response_en, source_lang)
                
                print("\nHelpie: " + final_response + "\n")
                
                # 5. Actualizar el historial de conversación
                conversation_history.append((user_query, final_response))
                # Limitar el historial para no sobrecargar el prompt
                if len(conversation_history) > 5:
                    conversation_history.pop(0)
            else:
                print("\nHelpie: Lo siento, no he podido entender tu pregunta. ¿Podrías reformularla?\n")

            print("-" * 50)

        except KeyboardInterrupt:
            print("\nHelpie: ¡Hasta pronto! Mantente seguro.")
            break
        except Exception as e:
            print(f"\nHa ocurrido un error inesperado: {e}")
            print("Helpie: Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
