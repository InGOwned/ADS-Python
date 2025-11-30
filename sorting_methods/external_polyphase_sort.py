import heapq
import os
import tempfile

def split_file_to_runs(input_file, run_size, temp_dir):
    """
    Разбивает входной файл на отсортированные серии.
    """
    runs = []
    with open(input_file, 'r') as f:
        while True:
            # Читаем серию чисел
            run = []
            for _ in range(run_size):
                line = f.readline()
                if not line:
                    break
                try:
                    run.append(int(line.strip()))
                except ValueError:
                    continue  # пропускаем некорректные строки
            
            if not run:
                break
            
            # Сортируем серию и записываем во временный файл
            run.sort()
            run_file = tempfile.NamedTemporaryFile(mode='w+', dir=temp_dir, delete=False)
            for num in run:
                run_file.write(f"{num}\n")
            run_file.close()
            runs.append(run_file.name)
    
    return runs

def merge_runs(runs, output_file, temp_dir):
    """
    Слияние всех серий в один отсортированный файл с использованием многофазной сортировки.
    """
    # Временные файлы для многофазного слияния
    temp_files = [tempfile.NamedTemporaryFile(mode='w+', dir=temp_dir, delete=False) for _ in range(2)]
    temp_paths = [f.name for f in temp_files]
    
    current_runs = runs
    current_output = 0
    
    while len(current_runs) > 1:
        # Сливаем серии
        with open(temp_paths[current_output], 'w') as outfile:
            # Открываем все файлы серий
            run_files = [open(run, 'r') for run in current_runs]
            # Используем heapq для эффективного слияния
            heap = []
            for i, file in enumerate(run_files):
                line = file.readline()
                if line:
                    heapq.heappush(heap, (int(line.strip()), i))
            
            while heap:
                val, file_idx = heapq.heappop(heap)
                outfile.write(f"{val}\n")
                
                # Читаем следующее значение из соответствующего файла
                next_line = run_files[file_idx].readline()
                if next_line:
                    heapq.heappush(heap, (int(next_line.strip()), file_idx))
            
            # Закрываем файлы серий
            for f in run_files:
                f.close()
        
        # Удаляем предыдущие временные файлы
        for run in current_runs:
            os.unlink(run)
        
        # Меняем текущий выходной файл
        current_runs = [temp_paths[current_output]]
        current_output = 1 - current_output
    
    # Переименовываем финальный файл
    if current_runs:
        os.rename(current_runs[0], output_file)
    
    # Удаляем временные файлы
    for temp_file in temp_files:
        try:
            os.unlink(temp_file.name)
        except:
            pass

def external_polyphase_sort(input_file, output_file, run_size=1000):
    """
    Внешняя многофазная сортировка.
    
    Параметры:
    input_file: путь к входному файлу с числами (по одному числу на строку)
    output_file: путь к выходному файлу
    run_size: размер одной серии (количество чисел)
    """
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Шаг 1: Разбиение на отсортированные серии
        runs = split_file_to_runs(input_file, run_size, temp_dir)
        
        if not runs:
            # Пустой входной файл
            with open(output_file, 'w') as f:
                pass
            return
        
        # Шаг 2: Слияние серий
        merge_runs(runs, output_file, temp_dir)
        
    finally:
        # Очистка временной директории
        try:
            os.rmdir(temp_dir)
        except:
            pass

def create_test_file(filename, numbers):
    """Создает тестовый файл с числами"""
    with open(filename, 'w') as f:
        for num in numbers:
            f.write(f"{num}\n")

if __name__ == "__main__":
    # Создаем тестовый файл
    test_input = "test_input.txt"
    test_output = "sorted_output.txt"
    numbers = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42] * 100  # Большой массив для демонстрации
    create_test_file(test_input, numbers)
    
    print("Запуск внешней многофазной сортировки...")
    external_polyphase_sort(test_input, test_output, run_size=50)
    
    # Проверяем результат
    with open(test_output, 'r') as f:
        sorted_numbers = [int(line.strip()) for line in f.readlines()]
    
    print(f"Отсортировано {len(sorted_numbers)} чисел")
    print("Первые 10 чисел:", sorted_numbers[:10])
    print("Последние 10 чисел:", sorted_numbers[-10:])
    
    # Очищаем тестовые файлы
    os.unlink(test_input)
    # os.unlink(test_output)  # Раскомментировать, если не хотите сохранять результат
"""
Этот алгоритм реализует внешнюю многофазную сортировку, которая используется
для сортировки данных, которые не помещаются в оперативную память.

Принцип работы:
1. Разбиение входного файла на серии (runs) фиксированного размера
2. Сортировка каждой серии в памяти и запись во временные файлы
3. Постепенное слияние серий с использованием многофазного подхода

Особенности:
- Эффективно использует память
- Минимизирует количество операций ввода-вывода
- Подходит для очень больших объемов данных
- Использует кучу (heap) для эффективного слияния
"""