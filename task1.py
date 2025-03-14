import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LABEL_SIZE = "Розмір масиву"
LABEL_RANDOMIZED = "Час (рандомізований)"
LABEL_DETERMINISTIC = "Час (детермінований)"
LABEL_RANDOMIZED_QS = "Рандомізований QuickSort"
LABEL_DETERMINISTIC_QS = "Детермінований QuickSort"

def quick_sort(arr, randomized=True):
    if len(arr) < 2:
        return arr
    pivot_index = random.randint(0, len(arr) - 1) if randomized else -1
    pivot = arr[pivot_index]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left, randomized) + middle + quick_sort(right, randomized)

def measure_time(sort_function, arr, iterations=5):
    times = []
    for _ in range(iterations):
        arr_copy = arr.copy()
        start_time = time.perf_counter()
        sort_function(arr_copy)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    return np.mean(times)

array_sizes = [10_000, 50_000, 100_000, 500_000]
results = []

for size in array_sizes:
    arr = [random.randint(0, 1_000_000) for _ in range(size)]
    randomized_time = measure_time(lambda x: quick_sort(x, randomized=True), arr)
    deterministic_time = measure_time(lambda x: quick_sort(x, randomized=False), arr)
    print(f"\n{LABEL_SIZE}: {size}")
    print(f"   {LABEL_RANDOMIZED_QS}: {randomized_time:.4f} секунд")
    print(f"   {LABEL_DETERMINISTIC_QS}: {deterministic_time:.4f} секунд")
    results.append((size, randomized_time, deterministic_time))

df = pd.DataFrame(results, columns=[LABEL_SIZE, LABEL_RANDOMIZED, LABEL_DETERMINISTIC])
if df[LABEL_RANDOMIZED].iloc[-1] < df[LABEL_DETERMINISTIC].iloc[-1]:
    print("\nВисновок: Рандомізований QuickSort працює трохи швидше на великих масивах.")
else:
    print("\nВисновок: Детермінований QuickSort працює швидше у цьому тесті, але може бути інший результат на вже відсортованих масивах.")

plt.figure(figsize=(10, 6))
plt.plot(df[LABEL_SIZE], df[LABEL_RANDOMIZED], marker='o', label=LABEL_RANDOMIZED_QS)
plt.plot(df[LABEL_SIZE], df[LABEL_DETERMINISTIC], marker='s', label=LABEL_DETERMINISTIC_QS)
plt.xlabel(LABEL_SIZE)
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння продуктивності QuickSort")
plt.legend()
plt.grid(True)
plt.show()
