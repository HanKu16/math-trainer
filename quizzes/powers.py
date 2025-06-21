import random

class PowersQuiz:
    """Klasa reprezentująca quiz z potęg."""

    def __init__(self):
        pass # Pytania są teraz ładowane z JSON

    def get_name(self):
        return "Potęgi"

    def check_answer(self, user_answer_str, correct_answer):
        """
        Sprawdza odpowiedź użytkownika dla pytań o potęgi.
        user_answer_str: odpowiedź użytkownika jako string
        correct_answer: poprawna odpowiedź (z JSON, int)
        """
        try:
            user_answer = int(user_answer_str)
            return user_answer == correct_answer
        except ValueError:
            # Użytkownik wprowadził coś, co nie jest liczbą
            return False
        except Exception as e:
            print(f"Błąd podczas sprawdzania odpowiedzi: {e}")
            return False