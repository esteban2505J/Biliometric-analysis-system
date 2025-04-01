import copy

def quick_sort(arr):
    arr = copy.deepcopy(arr)
    
    def _quick_sort(arr, low, high):
        if low < high:
            pivot_idx = _partition(arr, low, high)
            _quick_sort(arr, low, pivot_idx - 1)
            _quick_sort(arr, pivot_idx + 1, high)
        return arr
    
    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    if not arr:
        return arr
    return _quick_sort(arr, 0, len(arr) - 1)
