from functools import reduce


def get_positive_integer_input(prompt):
    """Pobiera od użytkownika dodatnią liczbę całkowitą."""
    while True:
        try:
            value_str = input(prompt)
            value = int(value_str)
            if value <= 0:
                print("Wprowadź liczbę większą od zera.")
            else:
                return value
        except ValueError:
            print("Nieprawidłowy format. Wprowadź liczbę całkowitą.")

def format_percentage(value, total):
    """Formatuje procentowy wynik."""
    if total == 0:
        return "0.00%"
    percentage = (value / total) * 100
    return f"{percentage:.2f}%"

def clean_string(input_string):
    """Usuwa białe znaki z początku i końca stringa oraz zmienia na małe litery."""
    return input_string.strip().lower()

def filter_positive_numbers(numbers):
    """
    Filtruje listę liczb, zwracając tylko liczby dodatnie.
    Wykorzystuje funkcję filter() i lambda.
    """
    return list(filter(lambda x: x > 0, numbers))

def square_numbers(numbers: list[int]):
    """
    Przekształca listę liczb, zwracając listę ich kwadratów.
    Wykorzystuje funkcję map() i lambda.
    """
    return list(map(lambda x: x * x, numbers))

def format_progress_data(progress_records):
    """
    Formatuje dane o postępach w bardziej czytelny sposób.
    Wykorzystuje funkcję map() i lambda do tworzenia stringów.
    Zakłada, że progress_records to lista słowników np.
    [{"quiz_name": "Arytmetyka", "score": 8, "total": 10}]
    """
    return list(map(lambda record: f"Quiz: {record['quiz_name']}, Wynik: "
                                   f"{record['score']}/{record['total']}", progress_records))

def calculate_average_score(scores):
    """
    Oblicza średnią z listy wyników.
    Prosty przykład, który mógłby być częścią bardziej złożonej analizy.
    """
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def multiply_numbers_reduce(numbers):
    """
    Oblicza iloczyn wszystkich liczb w liście przy użyciu funkcji reduce().
    Jest to przykład operacji 'redukcji' listy do pojedynczej wartości.
    """
    if not numbers:
        return 1
    return reduce(lambda x, y: x * y, numbers)


def factorial_recursive(n):
    """
    Oblicza silnię liczby naturalnej n w sposób rekurencyjny.
    Jest to klasyczny przykład funkcji rekurencyjnej.
    Warunek bazowy: silnia 0 i 1 wynosi 1.
    Krok rekurencyjny: n! = n * (n-1)!
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Liczba musi być nieujemną liczbą całkowitą.")
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)


def apply_operation_to_list(numbers, operation_func):
    """
    Przyjmuje listę liczb i funkcję operacji jako parametr.
    Aplikuje tę operację do każdego elementu listy, zwracając nową listę wyników.
    Jest to przykład funkcji wyższego rzędu.
    """
    if not callable(operation_func):
        raise TypeError("Parametr 'operation_func' musi być funkcją.")
    return list(map(operation_func, numbers))


def read_file(path):
    file = None
    try:
        print(f"Otwieram plik: {path}")
        file = open(path, 'r', encoding='utf-8')
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"Błąd: Plik {path} nie istnieje!")
        return None
    except PermissionError:
        print(f"Błąd: Brak uprawnień do odczytu pliku {path}!")
        return None
    except UnicodeDecodeError:
        print("Błąd: Problem z kodowaniem pliku (użyj innego kodowania)")
        return None
    except Exception as e:
        print(f"Niespodziewany błąd: {type(e).__name__}: {e}")
        return None
    finally:
        if file is not None:
            print("Zamykam plik...")
            file.close()


def string_operations(text, pattern="Python", replacement="Java", number=3.14159):
    # Basic string operations
    print(f"\nOriginal text: '{text}'")
    print(f"Length: {len(text)} chars")
    print(f"Uppercase: {text.upper()}")
    print(f"Lowercase: {text.lower()}")

    # Searching
    print(f"\nPattern '{pattern}' found at index: {text.find(pattern)}")

    # Slicing and splitting
    print(f"\nFirst 5 chars: '{text[:5]}'")


GLOBAL_CONSTANT = "To jest globalna stała."
unique_numbers = {1, 5, 9}
answers = (3, 1, 2)