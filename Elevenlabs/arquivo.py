import numpy as np
import pyttsx3
import spacy
import os
import soundfile as sf

# Carrega o modelo de linguagem em português do spaCy
nlp = spacy.load("pt_core_news_sm")

# Inicializa o engine do pyttsx3
engine = pyttsx3.init()

# Define as configurações do engine
engine.setProperty('rate', 200) # Velocidade de reprodução

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
