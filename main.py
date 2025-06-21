from core.quiz_manager import QuizManager
from core.user_progress import UserProgress
from core.utils import get_positive_integer_input



def main():
    """Główna funkcja aplikacji Trener Matematyczny."""
    quiz_manager = QuizManager()
    user_progress = UserProgress()

    while True:
        print("\n--- Trener Matematyczny ---")
        print("1. Rozpocznij quiz")
        print("2. Sprawdź postępy")
        print("3. Wyjdź")

        choice = input("Wybierz opcję: ")

        if choice == '1':
            available_quizzes = quiz_manager.list_quizzes()
            if not available_quizzes:
                print("Brak dostępnych quizów. Sprawdź plik 'quizzes/quiz_data.json'.")
                continue

            print("\nDostępne quizy:")
            for i, quiz_name in enumerate(available_quizzes):
                print(f"{i + 1}. {quiz_name}")

            while True:
                try:
                    quiz_choice_str = input("Wybierz numer quizu: ")
                    quiz_index = int(quiz_choice_str) - 1
                    if 0 <= quiz_index < len(available_quizzes):
                        selected_quiz_name = available_quizzes[quiz_index]
                        break
                    else:
                        print("Nieprawidłowy numer quizu. Spróbuj ponownie.")
                except ValueError:
                    print("Nieprawidłowy format. Wprowadź liczbę.")

            num_questions = get_positive_integer_input("Ile pytań w quizie? ")

            try:
                quiz_instance, questions_data = quiz_manager.get_quiz_instance_and_questions(selected_quiz_name,
                                                                                             num_questions)
                score, total_questions = quiz_manager.run_quiz(quiz_instance, questions_data)
                user_progress.save_results(selected_quiz_name, score, total_questions)
            except ValueError as e:
                print(f"Błąd: {e}")
            except TypeError as e:
                print(f"Błąd konfiguracji quizu lub danych: {e}")
            except Exception as e:
                print(f"Wystąpił nieoczekiwany błąd: {e}")

        elif choice == '2':
            print("\n--- Analiza Postępów ---")
            print("1. Pokaż ogólne postępy (tekstowo)")
            print("2. Pokaż postępy dla konkretnego quizu (tekstowo)")
            print("3. Wygeneruj wykres ogólnych postępów")
            print("4. Wygeneruj wykres postępów dla konkretnego quizu")

            analysis_choice = input("Wybierz opcję analizy: ")

            if analysis_choice == '1':
                user_progress.analyze_progress(visualize=False)
            elif analysis_choice == '2':
                available_quizzes = quiz_manager.list_quizzes()
                if not available_quizzes:
                    print("Brak dostępnych quizów do analizy.")
                    continue

                print("\nDostępne quizy do analizy:")
                for i, quiz_name in enumerate(available_quizzes):
                    print(f"{i + 1}. {quiz_name}")

                while True:
                    try:
                        quiz_choice_str = input("Wybierz numer quizu do analizy: ")
                        quiz_index = int(quiz_choice_str) - 1
                        if 0 <= quiz_index < len(available_quizzes):
                            selected_quiz_name = available_quizzes[quiz_index]
                            user_progress.analyze_progress(selected_quiz_name, visualize=False)
                            break
                        else:
                            print("Nieprawidłowy numer quizu. Spróbuj ponownie.")
                    except ValueError:
                        print("Nieprawidłowy format. Wprowadź liczbę.")
            elif analysis_choice == '3':
                user_progress.analyze_progress(visualize=True)
            elif analysis_choice == '4':
                available_quizzes = quiz_manager.list_quizzes()
                if not available_quizzes:
                    print("Brak dostępnych quizów do analizy.")
                    continue

                print("\nDostępne quizy do analizy:")
                for i, quiz_name in enumerate(available_quizzes):
                    print(f"{i + 1}. {quiz_name}")

                while True:
                    try:
                        quiz_choice_str = input("Wybierz numer quizu do wizualizacji: ")
                        quiz_index = int(quiz_choice_str) - 1
                        if 0 <= quiz_index < len(available_quizzes):
                            selected_quiz_name = available_quizzes[quiz_index]
                            user_progress.analyze_progress(selected_quiz_name, visualize=True)
                            break
                        else:
                            print("Nieprawidłowy numer quizu. Spróbuj ponownie.")
                    except ValueError:
                        print("Nieprawidłowy format. Wprowadź liczbę.")
            else:
                print("Nieprawidłowa opcja analizy.")

        elif choice == '3':
            print("Dziękujemy za skorzystanie z Trenera Matematycznego!")
            break
        else:
            print("Nieprawidłowa opcja. Wybierz ponownie.")


if __name__ == "__main__":
    main()