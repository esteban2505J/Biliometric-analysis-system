from algorithms._counting_sort import _counting_sort
import copy

def radix_sort(arr):
    # Solo funciona con enteros positivos
    if not all(isinstance(x, int) and x >= 0 for x in arr):
        raise TypeError("Radix sort solo funciona con enteros positivos")
    
    arr = copy.deepcopy(arr)
    max_val = max(arr) if arr else 0
    exp = 1
    
    # Aplicar counting sort para cada dígito
    while max_val // exp > 0:
        _counting_sort(arr, exp)
        exp *= 10
        
    return arr