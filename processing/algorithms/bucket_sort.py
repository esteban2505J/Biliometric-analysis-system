def bucket_sort(arr):
    # Adaptamos para manejar strings y diferentes tipos
    if not arr:
        return arr
    
    if isinstance(arr[0], str):
        # Para strings, usamos orden lexicográfico
        max_val = max(arr, key=len)
        size = len(arr)
        buckets = [[] for _ in range(size)]
        
        for s in arr:
            # Distribuimos basados en la primera letra
            index = min(ord(s[0]) % size if s else 0, size - 1)
            buckets[index].append(s)
    else:
        # Para números
        if not all(isinstance(x, (int, float)) for x in arr):
            raise TypeError("Bucket sort requiere elementos numéricos")
            
        max_val = max(arr)
        min_val = min(arr)
        range_val = max(max_val - min_val, 1)  # Evitar división por cero
        size = len(arr)
        buckets = [[] for _ in range(size)]
        
        for num in arr:
            # Normalizar y distribuir en buckets
            index = min(int((num - min_val) / range_val * (size - 1)), size - 1)
            buckets[index].append(num)
    
    # Ordenar cada bucket y concatenar
    for bucket in buckets:
        bucket.sort()
    
    return [item for bucket in buckets for item in bucket]
