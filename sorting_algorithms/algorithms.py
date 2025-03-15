import heapq
from sortedcontainers import SortedList

# Implementación de los algoritmos de ordenamiento

def tim_sort(arr):
    return sorted(arr)

def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def tree_sort(arr):
    sorted_list = SortedList(arr)
    return list(sorted_list)

def pigeonhole_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [0] * size

    for x in arr:
        holes[x - min_val] += 1

    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + min_val
            i += 1
    return arr

def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    max_val = max(arr)
    min_val = min(arr)
    bucket_range = (max_val - min_val) / len(arr) + 1
    buckets = [[] for _ in range(len(arr))]

    for i in range(len(arr)):
        index = int((arr[i] - min_val) / bucket_range)
        buckets[index].append(arr[i])

    for i in range(len(buckets)):
        buckets[i] = sorted(buckets[i])

    result = []
    for i in range(len(buckets)):
        result.extend(buckets[i])

    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def heap_sort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]

def bitonic_sort(arr):
    def compare_and_swap(arr, i, j, dir):
        if (dir == 1 and arr[i] > arr[j]) or (dir == 0 and arr[i] < arr[j]):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, cnt, dir):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, dir)
            bitonic_merge(arr, low, k, dir)
            bitonic_merge(arr, low + k, k, dir)

    def bitonic_sort_recursive(arr, low, cnt, dir):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_recursive(arr, low, k, 1)
            bitonic_sort_recursive(arr, low + k, k, 0)
            bitonic_merge(arr, low, cnt, dir)

    bitonic_sort_recursive(arr, 0, len(arr), 1)
    return arr

def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

def binary_insertion_sort(arr):
    def binary_search(arr, val, start, end):
        if start == end:
            if arr[start] > val:
                return start
            else:
                return start + 1
        if start > end:
            return start

        mid = (start + end) // 2
        if arr[mid] < val:
            return binary_search(arr, val, mid + 1, end)
        elif arr[mid] > val:
            return binary_search(arr, val, start, mid - 1)
        else:
            return mid

    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]
    return arr

def radix_sort(arr):
    RADIX = 10
    maxLength = False
    tmp, placement = -1, 1

    while not maxLength:
        maxLength = True
        buckets = [[] for _ in range(RADIX)]

        for i in arr:
            tmp = i // placement
            buckets[tmp % RADIX].append(i)
            if maxLength and tmp > 0:
                maxLength = False

        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                arr[a] = i
                a += 1

        placement *= RADIX
    return arr