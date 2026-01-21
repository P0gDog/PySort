import matplotlib.pyplot as plt
import time
import random
import threading
import queue

amout = int(input("Enter the amount of numbers to sort: "))


def visualize_all_sorts(arr, sort_funcs_titles):

    arrs = [arr.copy() for _ in sort_funcs_titles]
    plt.ion()
    fig, axes = plt.subplots(1, len(sort_funcs_titles), figsize=(5 * len(sort_funcs_titles), 5))
    if len(sort_funcs_titles) == 1:\
        axes = [axes]
    bars_list = []
    for ax, (sort_func, title) in zip(axes, sort_funcs_titles):
        bars = ax.bar(range(len(arr)), arr)
        ax.set_title(title)
        bars_list.append(bars)

    update_queues = [queue.Queue() for _ in sort_funcs_titles]
    done_flags = [False] * len(sort_funcs_titles)

    def make_update_bars(idx):
        def update_bars(highlight_indices=[]):
            update_queues[idx].put(list(highlight_indices))
            time.sleep(0.02) 
        return update_bars

    def sort_thread(sort_func, arr, update_bars, idx):
        sort_func(arr, update_bars)
        done_flags[idx] = True

    threads = []
    for idx, (sort_func, _) in enumerate(sort_funcs_titles):
        t = threading.Thread(target=sort_thread, args=(sort_func, arrs[idx], make_update_bars(idx), idx))
        threads.append(t)
        t.start()

    # Main thread
    while not all(done_flags) or any(not q.empty() for q in update_queues):
        for idx, q in enumerate(update_queues):
            while not q.empty():
                highlight_indices = q.get()
                for i, bar in enumerate(bars_list[idx]):
                    bar.set_color('b')
                    if i in highlight_indices:
                        bar.set_color('r')
                    bar.set_height(arrs[idx][i])
        plt.pause(0.001)

    for t in threads:
        t.join()

    plt.ioff()
    plt.show()

def bubble_sort(arr, update_bars):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            update_bars([j, j+1])
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                update_bars([j, j+1])
                

def random_sort(arr, update_bars):
    n = len(arr)
    while arr != sorted(arr):
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        arr[i], arr[j] = arr[j], arr[i]
        update_bars([i, j])

def insertion_sort(arr, update_bars):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            update_bars([j, j+1])
            j -= 1
        arr[j + 1] = key
        update_bars([j+1])

def selection_sort(arr, update_bars):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            update_bars([min_idx, j])
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        update_bars([i, min_idx])


if __name__ == "__main__":
    numbers = [random.randint(1, 50) for _ in range(amout)]
    sort_funcs_titles = [

        (bubble_sort, "Bubble Sort"),
        (insertion_sort, "Insertion Sort"),
        (selection_sort, "Selection Sort"),


    ]
    visualize_all_sorts(numbers, sort_funcs_titles)