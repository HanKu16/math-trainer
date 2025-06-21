class BasicArithmeticQuiz:
    """Klasa reprezentująca quiz z podstawowej arytmetyki."""

    def __init__(self):
        pass # Pytania są teraz ładowane z JSON

    def get_name(self):
        return "Podstawowa Arytmetyka"

    def check_answer(self, user_answer_str, correct_answer):
        """
        Sprawdza odpowiedź użytkownika dla pytań arytmetycznych.
        user_answer_str: odpowiedź użytkownika jako string
        correct_answer: poprawna odpowiedź (z JSON, może być int/float)
        """
        try:
            if isinstance(correct_answer, float):
                user_answer = float(user_answer_str)
                # Porównanie z tolerancją dla floatów
                return abs(user_answer - correct_answer) < 1e-6
            elif isinstance(correct_answer, int):
                user_answer = int(user_answer_str)
                return user_answer == correct_answer
            else:
                # Fallback, jeśli typ z JSON jest nieoczekiwany
                return user_answer_str == str(correct_answer)
        except ValueError:
            # Użytkownik wprowadził coś, co nie jest liczbą
            return False
        except Exception as e:
            # Ogólna obsługa błędów, np. ZeroDivisionError jeśli w jakiś sposób dojdzie do eval(1/0)
            print(f"Błąd podczas sprawdzania odpowiedzi: {e}")
            return False