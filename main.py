class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_tree(s):
    """
    Построение бинарного дерева из линейно-скобочной записи.
    Пример: "8(3(1,6(4,7)),10(,14(13,)))"
    """
    if not s:
        return None

    # Извлечение значения узла
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] == '-'):
        i += 1
    value = int(s[:i])
    node = TreeNode(value)

    # Если скобок нет, узел без потомков
    if i >= len(s) or s[i] != '(':
        return node

    # Поиск соответствующих скобок для левого и правого поддеревьев
    balance = 0
    j = i + 1  # Пропускаем первую '('
    while j < len(s):
        if s[j] == '(':
            balance += 1
        elif s[j] == ')':
            balance -= 1
            if balance == -1:
                break
        elif s[j] == ',' and balance == 0:
            # Нашли разделитель на нулевом уровне
            left_str = s[i+1:j]  # между '(' и ','
            right_str = s[j+1:-1]  # между ',' и ')'
            node.left = build_tree(left_str)
            node.right = build_tree(right_str)
            return node
        j += 1

    # Если разделитель не найден, оба поддерева пусты или только правое
    left_str = s[i+1:j]
    right_str = ""
    node.left = build_tree(left_str)
    node.right = build_tree(right_str)
    return node

def preorder_traversal_recursive(node):
    """Рекурсивный прямой обход (КЛП)"""
    if node is None:
        return []
    return [node.value] + preorder_traversal_recursive(node.left) + preorder_traversal_recursive(node.right)

def preorder_traversal_iterative(root):
    """Нерекурсивный прямой обход с использованием стека"""
    if root is None:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        # Извлекаем верхний элемент из стека
        node = stack.pop()
        result.append(node.value)
        
        # Сначала добавляем правое поддерево, затем левое (так как стек работает по принципу LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

def main():
    s = "8(3(1,6(4,7)),10(,14(13,)))"
    print(f"Линейно-скобочная запись: {s}")
    
    root = build_tree(s)
    
    print(f"Рекурсивный прямой обход (КЛП): {preorder_traversal_recursive(root)}")
    print(f"Нерекурсивный прямой обход (КЛП): {preorder_traversal_iterative(root)}")

if __name__ == "__main__":
    main()