import unittest
import time
import random
import gc


class TestSortingPerformance(unittest.TestCase):
    """
    Testy wydajnościowe mierzące czas sortowania list o różnej wielkości.
    """

    def setUp(self):
        """
        Konfiguracja przed każdym testem.
        Wyłączamy garbage collector, aby uniknąć zakłóceń w pomiarach czasu
        przez niezwiązane z testem operacje sprzątania pamięci.
        """
        gc.disable()

    def tearDown(self):
        """
        Sprzątanie po każdym teście.
        Ponownie włączamy garbage collector.
        """
        gc.enable()

    def _generate_random_list(self, size):
        """Pomocnicza funkcja do generowania listy losowych liczb."""
        return [random.randint(0, size * 10) for _ in range(size)]

    def test_performance_sort_small_list(self):
        """
        Mierzy czas sortowania małej listy (np. 1000 elementów).
        """
        list_size = 1000
        data = self._generate_random_list(list_size)

        start_time = time.perf_counter()  # Używamy perf_counter dla większej precyzji
        data.sort()  # Testujemy wbudowaną metodę sortowania list
        end_time = time.time()

        duration = end_time - start_time
        print(f"\nCzas sortowania {list_size} elementów: {duration:.6f}s")
        # Asercja sprawdzająca, czy czas mieści się w oczekiwanym zakresie
        self.assertLess(duration, 2, f"Sortowanie {list_size} elementów trwa zbyt długo.")
        self.assertTrue(all(data[i] <= data[i + 1] for i in range(len(data) - 1)),
                        "Lista nie została posortowana poprawnie.")

    def test_performance_sort_medium_list(self):
        """
        Mierzy czas sortowania średniej listy (np. 100 000 elementów).
        """
        list_size = 100000
        data = self._generate_random_list(list_size)

        start_time = time.perf_counter()
        data.sort()
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"\nCzas sortowania {list_size} elementów: {duration:.6f}s")
        self.assertLess(duration, 0.05, f"Sortowanie {list_size} elementów trwa zbyt długo.")
        self.assertTrue(all(data[i] <= data[i + 1] for i in range(len(data) - 1)),
                        "Lista nie została posortowana poprawnie.")

    def test_performance_sort_large_list(self):
        """
        Mierzy czas sortowania dużej listy (np. 1 000 000 elementów).
        """
        list_size = 1000000
        data = self._generate_random_list(list_size)

        start_time = time.perf_counter()
        data.sort()
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"\nCzas sortowania {list_size} elementów: {duration:.6f}s")
        self.assertLess(duration, 0.5, f"Sortowanie {list_size} elementów trwa zbyt długo.")
        self.assertTrue(all(data[i] <= data[i + 1] for i in range(len(data) - 1)),
                        "Lista nie została posortowana poprawnie.")

# Aby uruchomić ten test z poziomu terminala:
# python -m unittest performance_sort_test.py