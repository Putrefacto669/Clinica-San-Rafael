# asistente_voz.py
import pyttsx3
import threading

class AsistenteVoz:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.configurar_voz()
        self.hablando = False
        
    def configurar_voz(self):
        """Configurar propiedades de la voz"""
        voices = self.engine.getProperty('voices')
        
        # Intentar usar voz en español si está disponible
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
            elif 'english' in voice.name.lower() and 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
        
        self.engine.setProperty('rate', 150)    # Velocidad de habla
        self.engine.setProperty('volume', 0.8)  # Volumen (0.0 a 1.0)
    
    def hablar(self, texto):
        """Reproducir texto en voz (en hilo separado)"""
        def hablar_hilo():
            try:
                self.hablando = True
                self.engine.say(texto)
                self.engine.runAndWait()
                self.hablando = False
            except Exception as e:
                print(f"Error en síntesis de voz: {e}")
                self.hablando = False
        
        if not self.hablando:
            threading.Thread(target=hablar_hilo, daemon=True).start()

# Crear instancia global del asistente de voz
asistente_voz = AsistenteVoz()
