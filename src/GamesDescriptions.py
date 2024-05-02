# Este archivo recoge los datos dentro del dataset
import openpyxl
import os
import nltk
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

# Obtiene la ruta absoluta del directorio actual
current_directory = os.path.dirname(__file__)

# Construye la ruta al archivo Excel en la carpeta 'dataset'
excel_file_path = os.path.join(current_directory, '..', 'dataset', 'games.xlsx')

# Carga el archivo Excel
wb = openpyxl.load_workbook(excel_file_path)

# Selecciona la hoja de trabajo
sheet = wb.active

# Obtiene el índice de la columna "About the game" si está presente
about_game_column_index = None
supported_languages_column_index = None

for cell in sheet[1]:  # Itera sobre la primera fila
    if cell.value == "About the game":
        about_game_column_index = cell.column
    elif cell.value == "Supported languages":
        supported_languages_column_index = cell.column

if about_game_column_index is not None and supported_languages_column_index is not None:
    # Lista para almacenar los datos
    gamesDescription = []

    # Itera sobre las filas y agrega los datos de la columna "About the game" a la lista
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Obtiene la cadena de idiomas de la celda
        supported_languages_str = row[supported_languages_column_index - 1]
        
        # Verifica si 'English' está en la lista de idiomas
        if supported_languages_str and 'English' in supported_languages_str:
            gamesDescription.append(row[about_game_column_index - 1])

    # Imprime los datos obtenidos
    print("Se han registrado un total de " + str(len(gamesDescription)) + " videojuegos")
else:
    print("No se encontró la columna 'About the game' o 'Supported languages' en el archivo Excel.")



# Ahora que ya tenemos las descripciones vamos a hacer un preprocesamiento para eliminar stopwords y demas

# Inicializa el lematizador y el stemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def remove_single_quotes(text):
    # Patrón para encontrar una comilla simple seguida de caracteres hasta el siguiente espacio
    pattern = r"'[^ ]*"
    
    # Reemplaza todas las ocurrencias del patrón con una cadena vacía
    text = re.sub(pattern, '', text)
    
    return text

def replaceText(text):

    text = text.replace('â€™', "'")
    text = text.replace('â€‹.', "")
    text = text.replace('â€‹', "")
    text = text.replace('â€“', "")
    text = text.replace('Â®', "")
    text = text.replace('â€¦', " ")
    text = text.replace('â€˜', "")
    text = text.replace('â„¢', "")
    text = text.replace('â€ ”', "")
    text = text.replace('â “', "")
    text = text.replace('.â€', "")
    text = text.replace('â€', "")
    text = text.replace('â€¢', "")
    text = text.replace('â€œ', "")
    text = text.replace('-', " ")
    text = text.replace('_', " ")
    text = text.replace('...', "")

    # Eliminar comillas simples seguidas de caracteres hasta el siguiente espacio
    text = remove_single_quotes(text)

    return text

def preprocess_text(text):

    replacedText = replaceText(text)

    # Tokenización
    tokens = word_tokenize(replacedText.lower())  # Convierte el texto a minúsculas y tokeniza

    # Eliminación de palabras vacías (stop words) y signos de puntuacion
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]

    # Lematización
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Derivación de palabras (stemming)
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]

    # Retorna el texto preprocesado como una cadena
    return ' '.join(stemmed_tokens)

gamesDescriptionPreprocessed = []

for description in gamesDescription:
    preprocessText = preprocess_text(description)
    gamesDescriptionPreprocessed.append(preprocessText)

# Por ultimo guardamos estas descripciones preprocesaas en un archivo de texto

# Construye la ruta al archivo de texto en la misma carpeta que el archivo Excel
preprocessed_file_path = os.path.join(current_directory, '..', 'dataset', 'DescripcionesPreprocesadas.txt')

# Guardar las descripciones preprocesadas en un archivo de texto en modo binario
with open(preprocessed_file_path, 'wb') as file:
    for preprocessed_description in gamesDescriptionPreprocessed:
        file.write((preprocessed_description + '\n').encode('utf-8'))


