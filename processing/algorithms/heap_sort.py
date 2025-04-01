import heapq
import copy

def heap_sort(arr):
    if not all(isinstance(x, (int, float, str)) for x in arr):
        # Heapq puede fallar con comparaciones incompatibles
        return sorted(arr)
    
    arr = copy.deepcopy(arr)
    result = []
    heapq.heapify(arr)
    while arr:
        result.append(heapq.heappop(arr))
    return result
