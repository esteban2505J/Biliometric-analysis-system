def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambia elementos
                swapped = True
        if not swapped:  # Si no hubo intercambios, la lista ya está ordenada
            break
    return arr