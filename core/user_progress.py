import csv
from datetime import datetime
import os
from core.visualization import plot_progress


class UserProgress:
    """Zarządza zapisywaniem, odczytywaniem i analizowaniem postępów użytkownika."""

    def __init__(self, data_file="../data/results.csv"):
        # Ścieżka do results.csv względem katalogu 'core'
        self.__data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), data_file))
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Prywatna metoda upewniająca się, że plik CSV istnieje i ma nagłówki."""
        os.makedirs(os.path.dirname(self.__data_file), exist_ok=True)
        try:
            with open(self.__data_file, 'x', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Quiz', 'Score', 'TotalQuestions'])
        except FileExistsError:
            pass
        except Exception as e:
            print(f"Błąd podczas tworzenia pliku wyników: {e}")

    def save_results(self, quiz_name, score, total_questions):
        """Zapisuje wyniki quizu do pliku CSV."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.__data_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, quiz_name, score, total_questions])
            print("Wyniki zapisane pomyślnie.")
        except IOError as e:
            print(f"Błąd zapisu do pliku: {e}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas zapisu wyników: {e}")

    def load_results(self):
        """Wczytuje wszystkie wyniki z pliku CSV."""
        results = []
        try:
            with open(self.__data_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Pominięcie nagłówka
                for row in reader:
                    if len(row) == 4:
                        try:
                            results.append({
                                'Timestamp': row[0],
                                'Quiz': row[1],
                                'Score': int(row[2]),
                                'TotalQuestions': int(row[3])
                            })
                        except ValueError as ve:
                            print(f"Ostrzeżenie: Nieprawidłowy format danych w wierszu CSV: {row}. Błąd: {ve}")
                            continue
        except FileNotFoundError:
            print("Brak pliku wyników. Rozpocznij quizy, aby go utworzyć.")
        except Exception as e:
            print(f"Błąd podczas wczytywania wyników: {e}")
        return results

    def analyze_progress(self, quiz_name=None, visualize=False):
        """
        Analizuje postępy użytkownika, opcjonalnie filtrując po nazwie quizu.
        Wykorzystuje programowanie funkcyjne (filter, lambda) oraz wizualizację.
        """
        all_results = self.load_results()

        if not all_results:
            print("Brak danych do analizy.")
            return

        if quiz_name:
            filtered_results = list(filter(lambda r: r['Quiz'] == quiz_name, all_results))
            if not filtered_results:
                print(f"Brak wyników dla quizu '{quiz_name}'.")
                return
            results_to_analyze = filtered_results
            print(f"\n--- Analiza postępów dla quizu: {quiz_name} ---")
        else:
            results_to_analyze = all_results
            print("\n--- Analiza ogólnych postępów ---")

        total_score = sum(result['Score'] for result in results_to_analyze)
        total_questions = sum(result['TotalQuestions'] for result in results_to_analyze)

        if total_questions == 0:
            print("Brak pytań do analizy.")
            return

        overall_percentage = (total_score / total_questions) * 100
        print(f"Łączna liczba poprawnych odpowiedzi: {total_score}")
        print(f"Łączna liczba pytań: {total_questions}")
        print(f"Ogólny procent poprawności: {overall_percentage:.2f}%")

        scores_only = list(map(lambda r: r['Score'], results_to_analyze))
        if scores_only:
            max_score = max(scores_only)
            min_score = min(scores_only)
            print(f"Najlepszy wynik w quizie: {max_score}")
            print(f"Najgorszy wynik w quizie: {min_score}")

        if not quiz_name:
            quiz_summary = {}
            for result in all_results:
                q_name = result['Quiz']
                if q_name not in quiz_summary:
                    quiz_summary[q_name] = {'total_score': 0, 'total_questions': 0}
                quiz_summary[q_name]['total_score'] += result['Score']
                quiz_summary[q_name]['total_questions'] += result['TotalQuestions']

            print("\nWyniki per quiz:")
            for q_name, data in quiz_summary.items():
                if data['total_questions'] > 0:
                    percentage = (data['total_score'] / data['total_questions']) * 100
                    print(f"  {q_name}: {data['total_score']}/{data['total_questions']} ({percentage:.2f}%)")
                else:
                    print(f"  {q_name}: Brak pytań do analizy.")

        if visualize:
            print("Generowanie wykresu postępów...")
            plot_progress(results_to_analyze, quiz_name)