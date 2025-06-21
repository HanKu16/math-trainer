import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from math_trainer.core.visualization import plot_progress


class TestVisualization(unittest.TestCase):
    """Testy dla modułu visualization."""

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.tight_layout')
    def test_plot_progress_overall(self, mock_tight_layout, mock_xticks, mock_grid, mock_ylabel, mock_xlabel,
                                   mock_title, mock_plot, mock_figure, mock_show):
        """Testuje generowanie ogólnego wykresu postępów."""
        results = [
            {'Timestamp': '2023-01-01 10:00:00', 'Quiz': 'Quiz A', 'Score': 5, 'TotalQuestions': 10},
            {'Timestamp': '2023-01-02 11:00:00', 'Quiz': 'Quiz B', 'Score': 8, 'TotalQuestions': 10},
            {'Timestamp': '2023-01-03 12:00:00', 'Quiz': 'Quiz A', 'Score': 7, 'TotalQuestions': 10}
        ]

        plot_progress(results)

        mock_figure.assert_called_once_with(figsize=(10, 6))
        mock_plot.assert_called_once()
        mock_title.assert_called_once_with('Ogólne postępy w quizach')
        mock_xlabel.assert_called_once_with('Data i czas')
        mock_ylabel.assert_called_once_with('Procent poprawnych odpowiedzi (%)')
        mock_grid.assert_called_once_with(True)
        mock_xticks.assert_called_once_with(rotation=45)
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()

        dates_arg = mock_plot.call_args[0][0]
        percentages_arg = mock_plot.call_args[0][1]

        self.assertEqual(len(dates_arg), 3)
        self.assertEqual(len(percentages_arg), 3)
        self.assertAlmostEqual(percentages_arg[0], 50.0)
        self.assertAlmostEqual(percentages_arg[1], 80.0)
        self.assertAlmostEqual(percentages_arg[2], 70.0)

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.tight_layout')
    def test_plot_progress_filtered(self, mock_tight_layout, mock_xticks, mock_grid, mock_ylabel, mock_xlabel,
                                    mock_title, mock_plot, mock_figure, mock_show):
        """Testuje generowanie wykresu dla konkretnego quizu."""
        results = [
            {'Timestamp': '2023-01-01 10:00:00', 'Quiz': 'Quiz A', 'Score': 5, 'TotalQuestions': 10},
            {'Timestamp': '2023-01-03 12:00:00', 'Quiz': 'Quiz A', 'Score': 7, 'TotalQuestions': 10}
        ]

        plot_progress(results, quiz_name="Quiz A")

        mock_title.assert_called_once_with('Postępy w quizie: Quiz A')

        dates_arg = mock_plot.call_args[0][0]
        percentages_arg = mock_plot.call_args[0][1]
        self.assertEqual(len(dates_arg), 2)
        self.assertEqual(len(percentages_arg), 2)
        self.assertAlmostEqual(percentages_arg[0], 50.0)
        self.assertAlmostEqual(percentages_arg[1], 70.0)

    @patch('builtins.print')
    @patch('matplotlib.pyplot.show')
    def test_plot_progress_no_results(self, mock_show, mock_print):
        """Testuje, czy funkcja obsługuje brak danych do wykresu."""
        plot_progress([])
        mock_print.assert_called_once_with("Brak danych do wygenerowania wykresu.")
        mock_show.assert_not_called()

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.plot')
    def test_plot_progress_zero_total_questions(self, mock_plot, mock_show):
        """Testuje, czy funkcja obsługuje wyniki z zerową liczbą pytań."""
        results = [
            {'Timestamp': '2023-01-01 10:00:00', 'Quiz': 'Quiz C', 'Score': 0, 'TotalQuestions': 0},
            {'Timestamp': '2023-01-02 11:00:00', 'Quiz': 'Quiz C', 'Score': 5, 'TotalQuestions': 10}
        ]
        plot_progress(results, quiz_name="Quiz C")

        percentages_arg = mock_plot.call_args[0][1]
        self.assertAlmostEqual(percentages_arg[0], 0.0)
        self.assertAlmostEqual(percentages_arg[1], 50.0)
        mock_show.assert_called_once()


if __name__ == '__main__':
    unittest.main()