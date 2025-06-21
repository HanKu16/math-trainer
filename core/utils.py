# ... kod bez zmian, ale plik został przeniesiony do core/
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

GLOBAL_CONSTANT = "To jest globalna stała."