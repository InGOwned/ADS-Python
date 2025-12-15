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

def preorder_traversal(node):
    """Прямой обход (КЛП)"""
    if node is None:
        return []
    return [node.value] + preorder_traversal(node.left) + preorder_traversal(node.right)

def inorder_traversal(node):
    """Центральный обход (ЛКП)"""
    if node is None:
        return []
    return inorder_traversal(node.left) + [node.value] + inorder_traversal(node.right)

def postorder_traversal(node):
    """Концевой обход (ЛПК)"""
    if node is None:
        return []
    return postorder_traversal(node.left) + postorder_traversal(node.right) + [node.value]

def main():
    s = "8(3(1,6(4,7)),10(,14(13,)))"
    print(f"Линейно-скобочная запись: {s}")
    
    root = build_tree(s)
    
    print(f"Прямой обход (КЛП): {preorder_traversal(root)}")
    print(f"Центральный обход (ЛКП): {inorder_traversal(root)}")
    print(f"Концевой обход (ЛПК): {postorder_traversal(root)}")

if __name__ == "__main__":
    main()