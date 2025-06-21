import requests
from bs4 import BeautifulSoup
import time

'''
Работает  гита
'''

class six_degrees():
    def __init__(self, url_start, url_stop, rate_limit):
        self.url_start = url_start
        self.url_stop = url_stop
        self.rate_limit = rate_limit

    def get_wikipedia_links(self, url, base_url):
        """Получает все ссылки на другие статьи Википедии"""
        try:
            print(f"Загружаем страницу: {url}")  # Логирование загрузки страницы
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            links = set()
            for a in soup.select('div.mw-parser-output a[href^="/wiki/"]'):
                href = a.get('href')
                if ":" not in href:  # Исключаем специальные страницы (например, "File:", "Help:")
                    full_url = base_url + href
                    links.add(full_url)

            print(f"Найдено {len(links)} ссылок на странице: {url}")  # Логирование найденных ссылок
            return links
        except Exception as e:
            print(f"Ошибка при получении ссылок с {url}: {e}")
            return set()


    def find_first_path(self, start_url, target_url, rate_limit):
        """Находит путь между двумя URL-адресами"""
        visited = set()  # Множество для отслеживания посещенных страниц
        stack = [(start_url, [start_url])]  # Стек с текущим URL и путем до него
        requests_made = 0  # Счетчик выполненных запросов

        while stack:
            current_url, path = stack.pop()  # Извлекаем последний элемент из стека
            print(f"Обрабатываем URL: {current_url}, текущий путь: {' -> '.join(path)}")  # Логирование текущего шага

            # Проверяем, достигли ли целевого URL
            if current_url == target_url:
                print(f"Цель достигнута: {target_url}")  # Логирование достижения цели
                return path

            # Если глубина превышает 5, прекращаем поиск
            if len(path) > 5:
                print(f"Глубина поиска превышена для URL: {current_url}")  # Логирование превышения глубины
                continue

            # Получаем ссылки с текущей страницы
            if current_url not in visited:
                visited.add(current_url)
                links = self.get_wikipedia_links(current_url, base_url="https://en.wikipedia.org")
                requests_made += 1

                # Учитываем rate-limit
                if requests_made >= rate_limit:
                    print("Достигнут лимит запросов. Делаем паузу на 1 секунду.")  # Логирование rate-limit
                    time.sleep(1)  # Пауза для соблюдения лимита
                    requests_made = 0

                # Добавляем новые ссылки в стек
                for link in links:
                    if link not in visited:
                        print(f"Добавляем ссылку в стек: {link}")  # Логирование добавления ссылки
                        stack.append((link, path + [link]))

        print(f"Путь не найден за 5 шагов от {start_url} до {target_url}")  # Логирование неудачного поиска
        return None


    def save_path_to_file(self, path, filename):
        """Сохраняет путь в файл."""
        if path:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(" -> ".join(path))
            print(f"Путь сохранен в файл: {filename}")
        else:
            print(f"Путь не найден, файл {filename} не создан.")


    def main(self, url1, url2, rate_limit):
        """Основная функция для поиска первого пути и записи в файлы."""
        print("Поиск пути от url1 к url2")
        path1 = self.find_first_path(url1, url2, rate_limit)
        if path1:
            print(f"Путь от {url1} к {url2}:")
            print(" -> ".join(path1))
            self.save_path_to_file(path1, "from_url1_to_url2.txt")
        else:
            print(f"Путь от {url1} к {url2} не найден за 5 шагов.")

        print("Поиск пути от url2 к url1")
        path2 = self.find_first_path(url2, url1, rate_limit)
        if path2:
            print(f"Путь от {url2} к {url1}:")
            print(" -> ".join(path2))
            self.save_path_to_file(path2, "from_url2_to_url1.txt")
        else:
            print(f"Путь от {url2} к {url1} не найден за 5 шагов.")


# Входные данные
url1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
url2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
rate_limit = 10

z = six_degrees(url1, url2, rate_limit)
# Запуск скрипта
z.main(url1, url2, rate_limit)

print('Выполнено')