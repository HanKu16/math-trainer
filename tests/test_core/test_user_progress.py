import unittest
import os
import csv
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from math_trainer.core.user_progress import UserProgress


class TestUserProgress(unittest.TestCase):
    """Testy dla klasy UserProgress."""

    def setUp(self):
        """Konfiguracja przed każdym testem."""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'temp_test_data')
        self.test_data_file = os.path.join(self.test_data_dir, "test_results.csv")

        os.makedirs(self.test_data_dir, exist_ok=True)
        # Ścieżka do pliku results.csv musi być teraz względna do math_trainer/core/
        # więc z perspektywy test_user_progress.py (który jest w test_core)
        # to będzie ../../data/results.csv
        self.user_progress = UserProgress(
            data_file=os.path.relpath(self.test_data_file, os.path.dirname(os.path.abspath(__file__)) + "/../../core"))

        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        self.user_progress._ensure_file_exists()

    def tearDown(self):
        """Czyszczenie po każdym teście."""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.test_data_dir):
            os.rmdir(self.test_data_dir)

    def test_ensure_file_exists(self):
        """Testuje, czy plik CSV jest tworzony z nagłówkami."""
        self.assertTrue(os.path.exists(self.test_data_file))
        with open(self.test_data_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, ['Timestamp', 'Quiz', 'Score', 'TotalQuestions'])

    def test_save_results(self):
        """Testuje zapisywanie wyników do pliku."""
        quiz_name = "Test Quiz 1"
        score = 3
        total_questions = 5
        self.user_progress.save_results(quiz_name, score, total_questions)

        results = self.user_progress.load_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['Quiz'], quiz_name)
        self.assertEqual(results[0]['Score'], score)
        self.assertEqual(results[0]['TotalQuestions'], total_questions)
        self.assertIsInstance(results[0]['Timestamp'], str)

    def test_load_results_empty_file(self):
        """Testuje wczytywanie wyników z pustego pliku (tylko nagłówki)."""
        results = self.user_progress.load_results()
        self.assertEqual(len(results), 0)

    def test_load_results_multiple_entries(self):
        """Testuje wczytywanie wielu wpisów."""
        self.user_progress.save_results("Quiz A", 5, 10)
        self.user_progress.save_results("Quiz B", 8, 10)

        results = self.user_progress.load_results()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['Quiz'], "Quiz A")
        self.assertEqual(results[1]['Quiz'], "Quiz B")

    @patch('builtins.print')
    def test_analyze_progress_overall(self, mock_print):
        """Testuje ogólną analizę postępów."""
        self.user_progress.save_results("Quiz A", 5, 10)
        self.user_progress.save_results("Quiz B", 8, 10)

        self.user_progress.analyze_progress()

        mock_print.assert_any_call("Łączna liczba poprawnych odpowiedzi: 13")
        mock_print.assert_any_call("Łączna liczba pytań: 20")
        mock_print.assert_any_call("Ogólny procent poprawności: 65.00%")
        mock_print.assert_any_call("  Quiz A: 5/10 (50.00%)")
        mock_print.assert_any_call("  Quiz B: 8/10 (80.00%)")

    @patch('builtins.print')
    def test_analyze_progress_filtered_by_quiz(self, mock_print):
        """Testuje analizę postępów dla konkretnego quizu."""
        self.user_progress.save_results("Quiz A", 5, 10)
        self.user_progress.save_results("Quiz B", 8, 10)
        self.user_progress.save_results("Quiz A", 7, 10)

        self.user_progress.analyze_progress("Quiz A")

        mock_print.assert_any_call("\n--- Analiza postępów dla quizu: Quiz A ---")
        mock_print.assert_any_call("Łączna liczba poprawnych odpowiedzi: 12")
        mock_print.assert_any_call("Łączna liczba pytań: 20")
        mock_print.assert_any_call("Ogólny procent poprawności: 60.00%")
        self.assertNotIn("Quiz B", [call_args.args[0] for call_args in mock_print.call_args_list])

    @patch('builtins.print')
    def test_analyze_progress_no_results(self, mock_print):
        """Testuje analizę postępów, gdy brak wyników."""
        self.user_progress.analyze_progress()
        mock_print.assert_called_with("Brak danych do analizy.")

    @patch('builtins.print')
    def test_analyze_progress_filtered_no_matching_results(self, mock_print):
        """Testuje analizę postępów, gdy brak wyników dla filtru."""
        self.user_progress.save_results("Quiz A", 5, 10)

        self.user_progress.analyze_progress("NonExistent Quiz")
        mock_print.assert_called_with("Brak wyników dla quizu 'NonExistent Quiz'.")


if __name__ == '__main__':
    unittest.main()