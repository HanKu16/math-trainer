import matplotlib.pyplot as plt
from datetime import datetime
import os


def plot_progress(results, quiz_name=None):
    """
    Generuje wykres postępów użytkownika.
    results: lista słowników wyników
    quiz_name: nazwa quizu, jeśli wizualizujemy konkretny quiz
    """
    if not results:
        print("Brak danych do wygenerowania wykresu.")
        return

    dates = []
    percentages = []

    sorted_results = sorted(results, key=lambda x: datetime.strptime(x['Timestamp'], "%Y-%m-%d %H:%M:%S"))

    for res in sorted_results:
        date_obj = datetime.strptime(res['Timestamp'], "%Y-%m-%d %H:%M:%S")
        dates.append(date_obj)

        score = res['Score']
        total = res['TotalQuestions']

        if total > 0:
            percentages.append((score / total) * 100)
        else:
            percentages.append(0)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, percentages, marker='o', linestyle='-')

    if quiz_name:
        plt.title(f'Postępy w quizie: {quiz_name}')
    else:
        plt.title('Ogólne postępy w quizach')

    plt.xlabel('Data i czas')
    plt.ylabel('Procent poprawnych odpowiedzi (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()


    path_to_plot = '../data/plot.png'
    output_dir = os.path.dirname(path_to_plot)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Utworzono katalog: {output_dir}")

    try:
        plt.savefig(path_to_plot)
    except Exception as e:
        pass

    plt.show()