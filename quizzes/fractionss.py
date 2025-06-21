from fractions import Fraction

class FractionsQuiz:
    """Klasa reprezentująca quiz z ułamków."""

    def __init__(self):
        pass

    def get_name(self):
        return "Ułamki"

    def check_answer(self, user_answer_str, correct_answer):
        """
        Sprawdza odpowiedź użytkownika dla pytań o ułamki.
        user_answer_str: odpowiedź użytkownika jako string (np. "1/2")
        correct_answer: poprawna odpowiedź (z JSON, oczekujemy stringa "licznik/mianownik")
        """
        try:
            user_fraction = Fraction(user_answer_str)
            # Zakładamy, że correct_answer z JSON jest stringiem "licznik/mianownik"
            correct_fraction = Fraction(str(correct_answer))
            return user_fraction == correct_fraction
        except ValueError:
            return False
        except Exception as e:
            print(f"Błąd podczas sprawdzania odpowiedzi: {e}")
            return False