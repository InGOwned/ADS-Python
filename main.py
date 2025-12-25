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


def manual_calculate(expression):
    """
    Вручную вычисляет выражение без использования eval().
    """
    # Убираем пробелы
    i = 0
    cleaned = ""
    while i < len(expression):
        if expression[i] != ' ':
            cleaned += expression[i]
        i += 1
    
    expression = cleaned
    
    # Парсим и вычисляем с учетом приоритета операций
    def parse_expression(expr):
        # Сначала обрабатываем скобки
        while '(' in expr:
            start = -1
            for i in range(len(expr)):
                if expr[i] == '(':
                    start = i
                elif expr[i] == ')':
                    inner = expr[start+1:i]
                    result = parse_expression(inner)
                    expr = expr[:start] + str(result) + expr[i+1:]
                    break
        
        while '*' in expr or '/' in expr:
            for i in range(len(expr)):
                if expr[i] == '*' or expr[i] == '/':
                    # Левый операнд
                    left_end = i - 1
                    while left_end >= 0 and (expr[left_end].isdigit() or expr[left_end] == '.'):
                        left_end -= 1
                    left_start = left_end + 1
                    left_num = float(expr[left_start:i])
                    
                    # Правый операнд
                    right_start = i + 1
                    right_end = right_start
                    while right_end < len(expr) and (expr[right_end].isdigit() or expr[right_end] == '.'):
                        right_end += 1
                    right_num = float(expr[right_start:right_end])
                    
                    # Выполняем операцию
                    if expr[i] == '*':
                        result = left_num * right_num
                    else:
                        if right_num == 0:
                            raise ZeroDivisionError("division by zero")
                        result = left_num / right_num
                    
                    expr = expr[:left_start] + str(result) + expr[right_end:]
                    break
        
        while '+' in expr or '-' in expr:
            for i in range(1, len(expr)):
                if expr[i] == '+' or expr[i] == '-':
                    # Левый операнд
                    left_end = i - 1
                    while left_end >= 0 and (expr[left_end].isdigit() or expr[left_end] == '.'):
                        left_end -= 1
                    left_start = left_end + 1
                    left_num = float(expr[left_start:i])
                    
                    # Правый операнд
                    right_start = i + 1
                    right_end = right_start
                    while right_end < len(expr) and (expr[right_end].isdigit() or expr[right_end] == '.'):
                        right_end += 1
                    right_num = float(expr[right_start:right_end])
                    
                    # Выполняем операцию
                    if expr[i] == '+':
                        result = left_num + right_num
                    else:
                        result = left_num - right_num
                    
                    expr = expr[:left_start] + str(result) + expr[right_end:]
                    break
        
        return float(expr)
    
    return parse_expression(expression)


def evaluate_expression(expression):
    if not check_brackets(expression):
        return "Ошибка: Неправильное количество или расположение скобок."

    if expression.endswith('='):
        expression = expression[:-1]
    else:
        return "Ошибка: Выражение должно заканчиваться знаком '='."

    try:
        result = manual_calculate(expression)
        return result
    except ZeroDivisionError:
        return "Ошибка: Деление на ноль."
    except Exception as e:
        return f"Ошибка в выражении: {e}"


if __name__ == "__main__":
    expr = input().strip()
    result = evaluate_expression(expr)
    print(result)
