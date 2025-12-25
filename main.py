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


def arithmetic_eval(expression):
    i = 0

    def parse_expression():
        nonlocal i
        result = parse_term()
        while i < len(expression) and expression[i] in "+-":
            op = expression[i]
            i += 1
            right = parse_term()
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    def parse_term():
        nonlocal i
        result = parse_factor()
        while i < len(expression) and expression[i] in "*/":
            op = expression[i]
            i += 1
            right = parse_factor()
            if op == '*':
                result *= right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError
                result /= right
        return result

    def parse_factor():
        nonlocal i
        if i < len(expression) and expression[i] == '-':
            i += 1
            return -parse_factor()
        elif i < len(expression) and expression[i] == '+':
            i += 1
            return parse_factor()
        elif expression[i].isdigit() or expression[i] == '.':
            return parse_number()
        elif expression[i] == '(':
            i += 1
            result = parse_expression()
            if i < len(expression) and expression[i] == ')':
                i += 1
                return result
            else:
                raise ValueError("Несоответствие скобок")
        else:
            raise ValueError(f"Неожиданный символ: {expression[i]}")

    def parse_number():
        nonlocal i
        start = i
        if i < len(expression) and expression[i] == '.':
            i += 1
            if not expression[i].isdigit():
                raise ValueError("Некорректное число")
            while i < len(expression) and expression[i].isdigit():
                i += 1
            return float(expression[start:i])
        else:
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            return float(expression[start:i])

    try:
        value = parse_expression()
        if i != len(expression):
            raise ValueError("Лишние символы после выражения")
        return value
    except (ValueError, IndexError, ZeroDivisionError):
        raise


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

        result = arithmetic_eval(temp_expr)
        return result
    except ZeroDivisionError:
        return "Ошибка: Деление на ноль."
    except Exception as e:
        return f"Ошибка в выражении: {e}"


if __name__ == "__main__":
    expr = input().strip()
    result = evaluate_expression(expr)
    print(result)
