def pigeonhole_sort(arr):
    # Solo funciona con enteros
    if not all(isinstance(x, int) for x in arr):
        raise TypeError("Pigeonhole sort solo funciona con enteros")
    
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    
    # Prevenir error de memoria con rangos muy grandes
    if size > 1000000:
        raise MemoryError("Rango demasiado grande para pigeonhole sort")
        
    holes = [[] for _ in range(size)]
    for x in arr:
        holes[x - min_val].append(x)
    return [x for hole in holes for x in hole]