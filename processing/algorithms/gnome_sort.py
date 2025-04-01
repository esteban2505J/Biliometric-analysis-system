import copy

def gnome_sort(arr):
    arr = copy.deepcopy(arr)
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr