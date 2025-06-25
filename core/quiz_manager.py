import importlib
import os
import json
import random
import sys


class QuizManager(object):
    """Zarządza ładowaniem, uruchamianiem quizów i ich danymi z pliku JSON."""

    # Zmiana ścieżek dostosowana do nowej struktury pakietów
    def __init__(self, quiz_dir="quizzes", quiz_data_file="../quizzes/quiz_data.json"):
        self.quiz_dir = quiz_dir
        # Ścieżka do quiz_data.json względem katalogu 'core'
        self.quiz_data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), quiz_data_file))
        self.available_quizzes = self._load_quiz_definitions()
        self.quiz_questions = self._load_quiz_questions()

    def _load_quiz_questions(self):
        """Prywatna metoda do ładowania pytań quizowych z pliku JSON."""
        questions_data = {}
        try:
            with open(self.quiz_data_file, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
        except FileNotFoundError:
            print(f"Błąd: Plik z danymi quizów '{self.quiz_data_file}' nie znaleziono.")
        except json.JSONDecodeError as e:
            print(f"Błąd parsowania pliku JSON '{self.quiz_data_file}': {e}")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania danych quizów: {e}")
        return questions_data

    def add_question_to_quiz(self, quiz_name, question_text, correct_answer):
        """
        Dodaje nowe pytanie do podanego quizu. Tworzy quiz, jeśli nie istnieje.
        """
        data = {}

        if os.path.exists(self.quiz_data_file):
            with open(self.quiz_data_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print("⚠️ Plik JSON był pusty lub uszkodzony. Tworzę nowy.")

        if quiz_name not in data:
            data[quiz_name] = []

        new_question = {
            "question": question_text,
            "answer": correct_answer
        }
        data[quiz_name].append(new_question)

        with open(self.quiz_data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"✅ Dodano pytanie do quizu '{quiz_name}'")
    def _load_quiz_definitions(self):
        """
        Prywatna metoda do ładowania klas quizów z katalogu quizzes.
        """
        quizzes = {}
        # Ścieżka do katalogu quizzes względem katalogu core
        quiz_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.quiz_dir))

        # Dodaj katalog quizzes do ścieżki sys.path TYLKO na czas ładowania definicji
        # To jest kluczowe, aby importlib.import_module mógł znaleźć pliki .py bezpośrednio
        # bez konieczności odwoływania się do 'math_trainer.quizzes' jako pełnego pakietu.
        # Jest to obejście dla dynamicznego importowania, gdy struktura pakietów jest złożona.
        if quiz_module_path not in sys.path:
            sys.path.insert(0, quiz_module_path)

        for filename in os.listdir(quiz_module_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(module_name)
                    for attr_name in dir(module):
                        attribute = getattr(module, attr_name)
                        if isinstance(attribute, type) and 'Quiz' in attr_name:
                            if hasattr(attribute, 'get_name') and callable(getattr(attribute, 'get_name')):
                                quiz_instance = attribute()
                                quizzes[quiz_instance.get_name()] = attribute
                            else:
                                print(
                                    f"Ostrzeżenie: Klasa {attr_name} w module {module_name} nie ma metody 'get_name'. Zostaje pominięta.")
                except Exception as e:
                    print(f"Błąd ładowania definicji quizu z pliku {filename}: {e}")

        if quiz_module_path in sys.path:
            sys.path.remove(quiz_module_path)
            importlib.invalidate_caches()

        return quizzes

    def list_quizzes(self):
        """Zwraca listę dostępnych nazw quizów na podstawie danych JSON."""
        return list(self.quiz_questions.keys())

    def get_quiz_instance_and_questions(self, quiz_name, num_questions=5):
        """
        Zwraca instancję wybranej klasy quizu i zestaw pytań dla niego.
        Pytania są pobierane z pliku JSON.
        """
        quiz_class = self.available_quizzes.get(quiz_name)
        if not quiz_class:
            raise ValueError(f"Definicja quizu '{quiz_name}' nie znaleziono w modułach Python.")

        quiz_instance = quiz_class()

        questions_for_quiz = self.quiz_questions.get(quiz_name)
        if not questions_for_quiz:
            raise ValueError(f"Brak pytań dla quizu '{quiz_name}' w pliku quiz_data.json.")

        if not isinstance(questions_for_quiz, list):
            raise TypeError(f"Oczekiwano listy pytań dla quizu '{quiz_name}', otrzymano {type(questions_for_quiz)}")

        # Wybierz losowe pytania, jeśli jest ich więcej niż num_questions
        if len(questions_for_quiz) > num_questions:
            selected_questions = random.sample(questions_for_quiz, num_questions)
        else:
            selected_questions = questions_for_quiz

        for q in selected_questions:
            if not isinstance(q, dict) or 'question' not in q or 'answer' not in q:
                raise ValueError(f"Nieprawidłowy format pytania w quiz_data.json dla quizu '{quiz_name}': {q}")

        return quiz_instance, selected_questions

    def run_quiz(self, quiz_instance, questions):
        """Przeprowadza quiz i zwraca liczbę poprawnych odpowiedzi."""
        if not hasattr(quiz_instance, 'check_answer') or not callable(getattr(quiz_instance, 'check_answer')):
            raise TypeError("Obiekt quizu musi mieć metodę 'check_answer(user_answer_str, correct_answer)'.")

        score = 0
        total_questions = len(questions)

        print(f"\n--- Rozpoczynam quiz: {quiz_instance.get_name()} ---")

        for i, q_data in enumerate(questions):
            question_str = q_data['question']
            correct_answer = q_data['answer']

            print(f"\nPytanie {i + 1}/{total_questions}: {question_str}")
            try:
                user_answer_str = input("Twoja odpowiedź: ").strip()

                is_correct = quiz_instance.check_answer(user_answer_str, correct_answer)

                if is_correct:
                    print("Poprawna odpowiedź!")
                    score += 1
                else:
                    print(f"Błędna odpowiedź. Prawidłowa odpowiedź to: {correct_answer}")
            except ValueError as e:
                print(f"Błąd wejścia: {e}. Spróbuj ponownie.")
            except ZeroDivisionError:
                print("Wystąpił błąd dzielenia przez zero. To pytanie zostało pominięte.")
            except Exception as e:
                print(f"Wystąpił nieoczekiwany błąd podczas quizu: {e}")

        print(f"\n--- Koniec quizu: {quiz_instance.get_name()} ---")
        print(f"Twój wynik: {score}/{total_questions}")
        return score, total_questions
