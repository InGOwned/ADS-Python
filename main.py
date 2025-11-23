def check_brackets(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def evaluate_expression(expression):
    if not check_brackets(expression):
        return "Ошибка: Неправильное количество или расположение скобок."

    if expression.endswith('='):
        expression = expression[:-1]
    else:
        return "Ошибка: Выражение должно заканчиваться знаком '='."

    try:
        temp_expr = expression.replace('=', '')
        parts = temp_expr.split('/')
        for i in range(1, len(parts)):
            part = parts[i].strip()
            if part.startswith('0'):
                if len(part) == 1 or not part[1].isdigit():
                    return "Ошибка: Деление на ноль."
            elif part[0].isdigit() and part.split()[0][0] == '0':
                num = ""
                for c in part:
                    if c.isdigit() or c == '.':
                        num += c
                    else:
                        break
                if num and float(num) == 0:
                    return "Ошибка: Деление на ноль."

        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "Ошибка: Деление на ноль."
    except Exception as e:
        return f"Ошибка в выражении: {e}"

if __name__ == "__main__":
    expr = input().strip()
    result = evaluate_expression(expr)
    print(result)