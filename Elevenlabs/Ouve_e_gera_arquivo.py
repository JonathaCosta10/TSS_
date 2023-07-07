import speech_recognition as sr
import nltk
from textblob import TextBlob
import string

nltk.download('punkt','wordnet','stopwords')
#nltk.download('wordnet')
#nltk.download('stopwords')

# Cria uma instância do Recognizer
r = sr.Recognizer()

# Realiza o pré-processamento do texto
def pre_process_text(text):
    # Transforma o texto em minúsculo
    text = text.lower()
    # Remove pontuações
    text = "".join([char for char in text if char not in string.punctuation])
    # Realiza a tokenização
    tokens = nltk.word_tokenize(text)
    # Realiza a lematização
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Remove stopwords
    stopwords = nltk.corpus.stopwords.words('portuguese')
    tokens = [token for token in tokens if token not in stopwords]
    # Retorna o texto pré-processado
    return " ".join(tokens)

# Realiza a análise de sentimento do texto
def analyze_text(text):
    # Realiza o pré-processamento do texto
    text = pre_process_text(text)
    # Cria um objeto TextBlob com o texto pré-processado
    blob = TextBlob(text)
    # Retorna a polaridade e a subjetividade do texto
    return blob.sentiment

# Grava o texto em um arquivo
def save_text(text):
    with open('texto.txt', 'w') as file:
        file.write(text)

# Captura a entrada de voz do usuário
with sr.Microphone() as source:
    print("Diga algo...")
    audio = r.listen(source)

# Realiza a conversão do áudio para texto
try:
    text = r.recognize_google(audio, language='pt-BR') # Altere o idioma de acordo com sua necessidade
    print("Você disse: ", text)
    # Realiza a análise de sentimento do texto
    sentiment = analyze_text(text)
    print("Polaridade: {0}, Subjetividade: {1}".format(sentiment.polarity, sentiment.subjectivity))
    # Grava o texto em um arquivo
    save_text(text)
except sr.UnknownValueError:
    print("Não foi possível reconhecer a fala")
except sr.RequestError as e:
    print("Não foi possível realizar a requisição para o serviço de reconhecimento de fala: {0}".format(e))
