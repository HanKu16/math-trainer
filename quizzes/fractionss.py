from fractions import Fraction

class FractionsQuiz:
    """Klasa reprezentująca quiz z ułamków."""

    def __init__(self):
        pass # Pytania są teraz ładowane z JSON

    def get_name(self):
        return "Ułamki"

    def check_answer(self, user_answer_str, correct_answer):
        """
        Sprawdza odpowiedź użytkownika dla pytań o ułamki.
        user_answer_str: odpowiedź użytkownika jako string (np. "1/2")
        correct_answer: poprawna odpowiedź (z JSON, oczekujemy stringa "licznik/mianownik")
        """
        try:
            # Konwersja odpowiedzi użytkownika na obiekt Fraction
            user_fraction = Fraction(user_answer_str)
            # Konwersja poprawnej odpowiedzi na obiekt Fraction
            # Zakładamy, że correct_answer z JSON jest stringiem "licznik/mianownik"
            correct_fraction = Fraction(str(correct_answer)) # Upewniamy się, że to string

            return user_fraction == correct_fraction
        except ValueError:
            # Użytkownik wprowadził coś, co nie jest ułamkiem
            return False
        except Exception as e:
            print(f"Błąd podczas sprawdzania odpowiedzi: {e}")
            return False