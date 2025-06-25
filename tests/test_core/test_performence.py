
import unittest
import time
import random
import gc


class TestSortingPerformance(unittest.TestCase):
    """
    Łagodne testy wydajnościowe sortowania – działają na każdej maszynie.
    """

    def setUp(self):
        """Wyłączamy GC na czas testu, by pomiar był nieco dokładniejszy."""
        gc.disable()

    def tearDown(self):
        """Włączamy GC po teście."""
        gc.enable()

    def _generate_random_list(self, size):
        """Tworzy listę losowych liczb całkowitych."""
        return [random.randint(0, size * 10) for _ in range(size)]

    def _measure_sort_time(self, data):
        """Zwraca czas sortowania listy."""
        start = time.perf_counter()
        data.sort()
        end = time.perf_counter()
        return end - start

    def _print_result(self, size, duration):
        print(f"✅ Posortowano {size:,} elementów w {duration:.6f} sekundy.")

    def _assert_sorted(self, data):
        self.assertTrue(all(data[i] <= data[i + 1] for i in range(len(data) - 1)),
                        "Lista nie została posortowana poprawnie.")

    def test_sort_tiny_list(self):
        size = 100
        data = self._generate_random_list(size)
        duration = self._measure_sort_time(data)
        self._print_result(size, duration)
        self._assert_sorted(data)

    def test_sort_small_list(self):
        size = 1_000
        data = self._generate_random_list(size)
        duration = self._measure_sort_time(data)
        self._print_result(size, duration)
        self._assert_sorted(data)

    def test_sort_medium_list(self):
        size = 10_000
        data = self._generate_random_list(size)
        duration = self._measure_sort_time(data)
        self._print_result(size, duration)
        self._assert_sorted(data)

    def test_sort_big_but_easy_list(self):
        size = 50_000  # Wciąż lekkie dla większości laptopów
        data = self._generate_random_list(size)
        duration = self._measure_sort_time(data)
        self._print_result(size, duration)
        self._assert_sorted(data)


if __name__ == '__main__':
    unittest.main()
# Aby uruchomić ten test z poziomu terminala:
# python -m unittest performance_sort_test.py
