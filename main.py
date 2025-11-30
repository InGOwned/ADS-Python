def generate_numbers(x):
    result = []
    k = 0
    while 3**k <= x:
        l = 0
        while 3**k * 5**l <= x:
            m = 0
            while 3**k * 5**l * 7**m <= x:
                num = 3**k * 5**l * 7**m
                result.append(num)
                m += 1
            l += 1
        k += 1


    result = sorted(set(result))

    # Фильтруем
    return [num for num in result if 1 <= num <= x]

if __name__ == "__main__":
    x = int(input().strip())
    numbers = generate_numbers(x)
    print(" ".join(map(str, numbers)))