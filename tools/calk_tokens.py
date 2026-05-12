import tiktoken

def count_tokens(file_path, model="gpt-4"):
    """
    Считает количество токенов в текстовом файле для указанной модели.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        tokens = encoding.encode(text)
        return len(tokens)
    
    except FileNotFoundError:
        print(f"Ошибка: Файл по пути {file_path} не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

# --- ПРАВИЛЬНЫЕ НАСТРОЙКИ ДЛЯ ТВОЕЙ СТРУКТУРЫ ---
# Путь считается от корня проекта, так как запуск будет из корня
FILE_NAME = 'raw-text/490.txt' 
MODEL_NAME = 'gpt-4'

token_count = count_tokens(FILE_NAME, MODEL_NAME)

if token_count:
    print(f"Размер файла: {token_count} токенов")
    print(f"Примерно {token_count / 1000:.2f}K токенов")