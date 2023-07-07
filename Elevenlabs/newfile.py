import pyttsx3
import spacy
import os
import soundfile as sf
import numpy as np

# Carrega o modelo de linguagem em português do spaCy
nlp = spacy.load("pt_core_news_sm")

# Inicializa o engine do pyttsx3
engine = pyttsx3.init()

""" RATE """
rate = engine.getProperty('rate')  # Obtém a taxa de fala atual
print(rate)  # Imprime a taxa de fala atual
engine.setProperty('rate', 200)  # Define uma nova taxa de fala

""" VOLUME """
volume = engine.getProperty('volume')  # Obtém o nível de volume atual
print(volume)  # Imprime o nível de volume atual
engine.setProperty('volume', 0.8)  # Define um novo nível de volume

""" VOICE """
voices = engine.getProperty('voices')  # Obtém as vozes disponíveis
# engine.setProperty('voice', voices[0].id)  # Altera para a voz masculina (índice 0)
engine.setProperty('voice', voices[0].id)  # Altera para a voz feminina (índice 0)

# Define a pausa após a pontuação
engine.setProperty('phrasebreak', '.5s')

# Arquivo de texto
text_file = 'C:/Workspace/Texto/texto.txt'

# Verifica se o arquivo de texto existe
if not os.path.isfile(text_file):
    print(f"Arquivo de texto não encontrado: {text_file}")
    exit()

# Obtém o diretório do arquivo de texto
output_dir = os.path.dirname(text_file)

# Abre o arquivo de texto
with open(text_file, 'r', encoding='utf-8') as file:
    text = file.read()

# Processa o texto com o spaCy
doc = nlp(text)

# Lista para armazenar as sentenças
sentences = []

# Loop pelas sentenças do texto
for i, sent in enumerate(doc.sents):
    # Imprime a sentença
    print(sent.text)

    # Adiciona a sentença à lista
    sentences.append(sent.text)

    # Reproduz a sentença em áudio
    audio_file = os.path.join(output_dir, f"{i}.wav")
    engine.save_to_file(sent.text, audio_file)
    engine.runAndWait()

# Combine os arquivos de áudio das sentenças
combined_audio = None
for i, sentence in enumerate(sentences):
    audio_file = os.path.join(output_dir, f"{i}.wav")
    if os.path.exists(audio_file):
        audio_data, sample_rate = sf.read(audio_file)
        if combined_audio is None:
            combined_audio = audio_data
        else:
            combined_audio = np.concatenate((combined_audio, audio_data))
        os.remove(audio_file)

# Salva o áudio combinado em um arquivo WAV
output_file = os.path.join(output_dir, "output.wav")
sf.write(output_file, combined_audio, sample_rate, format="WAV")
