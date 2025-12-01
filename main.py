def check_brackets(s):
    stack = []
    brackets = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != brackets[char]:
                return False
            stack.pop()
    
    return len(stack) == 0

def main():
    print("Введите строку:")
    user_input = input().strip()
    
    if check_brackets(user_input):
        print("Строка существует")
    else:
        print("Строка не существует")

if __name__ == "__main__":
    main()