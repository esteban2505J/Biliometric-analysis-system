import copy

def binary_insertion_sort(arr):
    arr = copy.deepcopy(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i - 1
        
        # Encuentra la posición correcta con búsqueda binaria
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1
        
        # Mueve todos los elementos mayores a la derecha
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        
        arr[left] = key
    return arr