import unittest
import os
import sys
import json
import importlib
from unittest.mock import patch

# Ważne: Ta linia dodaje główny katalog 'math_trainer' do sys.path,
# aby importy takie jak 'math_trainer.core' działały,
# gdy testy są uruchamiane przez PyCharm lub unittest bezpośrednio.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Importujemy z pełnymi ścieżkami pakietowymi
from math_trainer.core.quiz_manager import QuizManager

class TestQuizManager(unittest.TestCase):
    """Testy dla klasy QuizManager."""

    def setUp(self):
        """Konfiguracja przed każdym testem."""
        # Definiowanie ścieżek do tymczasowego środowiska testowego
        # temp_test_env zostanie utworzone w katalogu, z którego uruchamiasz testy (np. tests/test_core/)
        self.test_root_dir = os.path.join(os.path.dirname(__file__), 'temp_test_env')
        self.test_quiz_dir = os.path.join(self.test_root_dir, "quizzes")
        self.test_data_file = os.path.join(self.test_quiz_dir, "test_quiz_data.json")
        # self.test_core_dir nie jest bezpośrednio potrzebny, ponieważ quiz_manager.py jest importowany
        # i jego ścieżki są względne do jego własnego położenia, nie do położenia testu.

        # Tworzenie tymczasowych katalogów
        os.makedirs(self.test_quiz_dir, exist_ok=True)

        # Tworzenie tymczasowego pliku quiz_data.json
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "Test Quiz Arytmetyka": [
                    {"question": "1+1?", "answer": 2},
                    {"question": "2*2?", "answer": 4}
                ],
                "Test Quiz Potęgi": [
                    {"question": "2^2?", "answer": 4}
                ]
            }, f)

        # Tworzenie tymczasowych modułów quizów (w pakiecie quizzes)
        # Te pliki muszą mieć __init__.py, aby były traktowane jako pakiet
        with open(os.path.join(self.test_quiz_dir, "test_arithmetic.py"), 'w', encoding='utf-8') as f:
            f.write("""
class TestArithmeticQuiz:
    def get_name(self): return "Test Quiz Arytmetyka"
    def check_answer(self, user_ans, correct_ans):
        try: return int(user_ans) == correct_ans
        except ValueError: return False
""")
        with open(os.path.join(self.test_quiz_dir, "test_powers.py"), 'w', encoding='utf-8') as f:
            f.write("""
class TestPowersQuiz:
    def get_name(self): return "Test Quiz Potęgi"
    def check_answer(self, user_ans, correct_ans):
        try: return int(user_ans) == correct_ans
        except ValueError: return False
""")
        # Utwórz dummy __init__.py w test_quiz_dir, aby był pakietem
        with open(os.path.join(self.test_quiz_dir, "__init__.py"), 'w') as f:
            f.write("")

        # WAŻNE: Dodajemy tymczasowy katalog quizzes do sys.path
        # QuizManager dynamicznie importuje moduły z tego katalogu.
        # Jest to konieczne, aby importlib.import_module mógł je znaleźć.
        if self.test_quiz_dir not in sys.path:
            sys.path.insert(0, self.test_quiz_dir)
            importlib.invalidate_caches() # Wymusza ponowne skanowanie ścieżek

        # Inicjalizacja QuizManager z absolutnymi ścieżkami do tymczasowych katalogów
        # QuizManager_init() oczekuje, że quiz_dir to ścieżka do folderu z quizami,
        # a quiz_data_file to ścieżka do pliku JSON.
        self.quiz_manager = QuizManager(
            quiz_dir=self.test_quiz_dir,
            quiz_data_file=self.test_data_file
        )

    def tearDown(self):
        """Czyszczenie po każdym teście."""
        # Usuwanie tymczasowych plików i katalogów
        # Usuwamy test_root_dir i wszystko w środku
        for root, dirs, files in os.walk(self.test_root_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        if os.path.exists(self.test_root_dir): # Dodatkowe sprawdzenie, czy katalog istnieje
            os.rmdir(self.test_root_dir)

        # Przywracanie sys.path: usuń ścieżkę do tymczasowego katalogu quizów
        if self.test_quiz_dir in sys.path:
            sys.path.remove(self.test_quiz_dir)
        # Usuń również główny katalog 'math_trainer' dodany na początku pliku
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        if project_root in sys.path:
            sys.path.remove(project_root)

        importlib.invalidate_caches() # Ważne po modyfikacji sys.path


    def test_load_quiz_definitions(self):
        """Testuje, czy definicje klas quizów są poprawnie ładowane."""
        # Sprawdzamy, czy nasze tymczasowe klasy zostały załadowane
        self.assertIn("Test Quiz Arytmetyka", self.quiz_manager.available_quizzes)
        self.assertIn("Test Quiz Potęgi", self.quiz_manager.available_quizzes)
        # Należy sprawdzić konkretne typy, które są oczekiwane z testowych plików
        # Sprawdzamy, czy załadowane obiekty są typami (klasami)
        self.assertTrue(isinstance(self.quiz_manager.available_quizzes["Test Quiz Arytmetyka"], type))
        self.assertTrue(isinstance(self.quiz_manager.available_quizzes["Test Quiz Potęgi"], type))


    def test_load_quiz_questions(self):
        """Testuje, czy pytania są poprawnie ładowane z JSON."""
        self.assertIn("Test Quiz Arytmetyka", self.quiz_manager.quiz_questions)
        self.assertEqual(len(self.quiz_manager.quiz_questions["Test Quiz Arytmetyka"]), 2)
        self.assertIn("Test Quiz Potęgi", self.quiz_manager.quiz_questions)
        self.assertEqual(len(self.quiz_manager.quiz_questions["Test Quiz Potęgi"]), 1)

    def test_list_quizzes(self):
        """Testuje, czy lista dostępnych quizów jest poprawnie zwracana (na podstawie JSON)."""
        quizzes = self.quiz_manager.list_quizzes()
        self.assertIsInstance(quizzes, list)
        self.assertIn("Test Quiz Arytmetyka", quizzes)
        self.assertIn("Test Quiz Potęgi", quizzes)
        self.assertEqual(len(quizzes), 2)

    def test_get_quiz_instance_and_questions_existing(self):
        """Testuje pobieranie instancji quizu i pytań."""
        quiz_instance, questions = self.quiz_manager.get_quiz_instance_and_questions("Test Quiz Arytmetyka",
                                                                                     num_questions=1)
        # Klasa quizu pochodzi z dynamicznego importu
        self.assertTrue(hasattr(quiz_instance, 'get_name'))
        self.assertEqual(quiz_instance.get_name(), "Test Quiz Arytmetyka")
        self.assertEqual(len(questions), 1)
        self.assertIsInstance(questions[0], dict)
        self.assertIn("question", questions[0])
        self.assertIn("answer", questions[0])


    def test_get_quiz_instance_and_questions_non_existing_def(self):
        """Testuje pobieranie quizu, dla którego brak definicji klasy."""
        # Tworzymy tymczasowy QuizManager z pominięciem jednego z testowych quizów w definicjach
        # aby zasymulować brak definicji.
        temp_quiz_manager = QuizManager(
            quiz_dir=self.test_quiz_dir,
            quiz_data_file=self.test_data_file
        )
        # Usuń z available_quizzes ten quiz, którego brak chcemy zasymulować
        temp_quiz_manager.available_quizzes = {k: v for k, v in temp_quiz_manager.available_quizzes.items() if
                                               k != "Test Quiz Arytmetyka"}

        with self.assertRaises(ValueError) as cm:
            temp_quiz_manager.get_quiz_instance_and_questions("Test Quiz Arytmetyka")
        self.assertIn("Definicja quizu 'Test Quiz Arytmetyka' nie znaleziono", str(cm.exception))


    def test_get_quiz_instance_and_questions_non_existing_data(self):
        """Testuje pobieranie quizu, dla którego brak danych w JSON."""
        # Tworzymy tymczasowy QuizManager z pustymi pytaniami, aby zasymulować brak danych.
        temp_quiz_manager = QuizManager(
            quiz_dir=self.test_quiz_dir,
            quiz_data_file=self.test_data_file
        )
        temp_quiz_manager.quiz_questions = {} # Usuń wszystkie pytania
        with self.assertRaises(ValueError) as cm:
            temp_quiz_manager.get_quiz_instance_and_questions("Test Quiz Arytmetyka")
        self.assertIn("Brak pytań dla quizu 'Test Quiz Arytmetyka' w pliku quiz_data.json.", str(cm.exception))

    @patch('builtins.input', side_effect=['2', '4'])
    @patch('builtins.print')
    def test_run_quiz_correct_answers(self, mock_print, mock_input):
        """Testuje run_quiz z poprawnymi odpowiedziami."""

        # Używamy prostego mocka zamiast rzeczywistej klasy, aby nie zależeć od dynamicznego importu
        # w kontekście tego konkretnego testu run_quiz
        class MockQuiz:
            def get_name(self):
                return "Mock Quiz"
            def check_answer(self, user_answer_str, correct_answer):
                try:
                    return int(user_answer_str) == correct_answer
                except ValueError:
                    return False

        mock_quiz_instance = MockQuiz()
        questions = [
            {"question": "1+1?", "answer": 2},
            {"question": "2*2?", "answer": 4}
        ]

        score, total = self.quiz_manager.run_quiz(mock_quiz_instance, questions)
        self.assertEqual(score, 2)
        self.assertEqual(total, 2)
        mock_print.assert_any_call("Poprawna odpowiedź!")

    @patch('builtins.input', side_effect=['0', '0'])
    @patch('builtins.print')
    def test_run_quiz_incorrect_answers(self, mock_print, mock_input):
        """Testuje run_quiz z błędnymi odpowiedziami."""
        class MockQuiz:
            def get_name(self): return "Mock Quiz"
            def check_answer(self, user_answer_str, correct_answer):
                try: return int(user_answer_str) == correct_answer
                except ValueError: return False

        mock_quiz_instance = MockQuiz()
        questions = [
            {"question": "1+1?", "answer": 2},
            {"question": "2*2?", "answer": 4}
        ]

        score, total = self.quiz_manager.run_quiz(mock_quiz_instance, questions)
        self.assertEqual(score, 0)
        self.assertEqual(total, 2)
        mock_print.assert_any_call("Błędna odpowiedź. Prawidłowa odpowiedź to: 2")

    @patch('builtins.input', side_effect=['abc', 'def'])
    @patch('builtins.print')
    def test_run_quiz_value_error(self, mock_print, mock_input):
        """Testuje run_quiz z ValueError od użytkownika."""
        class MockQuiz:
            def get_name(self): return "Mock Quiz"
            def check_answer(self, user_answer_str, correct_answer):
                # Symulujemy, że check_answer rzuca ValueError przy niepoprawnym wejściu
                raise ValueError("Niepoprawny format")

        mock_quiz_instance = MockQuiz()
        questions = [
            {"question": "1+1?", "answer": 2},
            {"question": "2*2?", "answer": 4}
        ]

        score, total = self.quiz_manager.run_quiz(mock_quiz_instance, questions)
        self.assertEqual(score, 0)
        self.assertEqual(total, 2)
        mock_print.assert_any_call("Błąd wejścia: Niepoprawny format. Spróbuj ponownie.")


if __name__ == '__main__':
    unittest.main()