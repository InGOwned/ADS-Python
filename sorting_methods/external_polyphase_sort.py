import heapq
import os
import tempfile
import shutil


def split_file_to_runs(input_file, run_size, temp_dir):
    """
    Разбивает входной файл на отсортированные серии.
    """
    runs = []
    with open(input_file, 'r') as f:
        while True:
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
            
            run.sort()
            run_file = tempfile.NamedTemporaryFile(mode='w+', dir=temp_dir, delete=False, suffix='.tmp')
            for num in run:
                run_file.write(f"{num}\n")
            run_file.close()
            runs.append(run_file.name)
    
    return runs


def merge_runs(runs, output_file, temp_dir):
    """
    Слияние всех серий в один отсортированный файл с использованием многофазной сортировки.
    """
    # Временные файлы для промежуточных итераций
    temp_files = [
        os.path.join(temp_dir, f"temp_{i}.txt") 
        for i in range(2)
    ]
    
    current_runs = runs
    current_output = 0
    
    while len(current_runs) > 1:
        with open(temp_files[current_output], 'w') as outfile:
            run_files = [open(run, 'r') for run in current_runs]
            heap = []
            
            for i, file in enumerate(run_files):
                line = file.readline()
                if line:
                    try:
                        heapq.heappush(heap, (int(line.strip()), i))
                    except ValueError:
                        pass
            
            while heap:
                val, file_idx = heapq.heappop(heap)
                outfile.write(f"{val}\n")
                
                next_line = run_files[file_idx].readline()
                if next_line:
                    try:
                        heapq.heappush(heap, (int(next_line.strip()), file_idx))
                    except ValueError:
                        pass
            
            for f in run_files:
                f.close()
        
        # Удаляем исходные серии
        for run in current_runs:
            try:
                os.unlink(run)
            except:
                pass
        
        current_runs = [temp_files[current_output]]
        current_output = 1 - current_output
    
    # Копируем финальный результат вместо переименования (более надежно)
    if current_runs:
        try:
            with open(current_runs[0], 'r') as src:
                with open(output_file, 'w') as dst:
                    dst.write(src.read())
        except Exception as e:
            print(f"Ошибка при копировании результата: {e}")
            raise
    
    # Удаляем оставшиеся временные файлы
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except:
            pass


def external_polyphase_sort(input_file, output_file, run_size=1000):
    """
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
            with open(output_file, 'w') as f:
                pass
            return
        
        # Шаг 2: Слияние серий
        merge_runs(runs, output_file, temp_dir)
        
    finally:
        # Удаляем всю временную директорию рекурсивно
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Предупреждение: не удалось удалить временную папку: {e}")


def create_test_file(filename, numbers):
    """Создает тестовый файл с числами"""
    with open(filename, 'w') as f:
        for num in numbers:
            f.write(f"{num}\n")


if __name__ == "__main__":
    # Создаем тестовый файл
    test_input = "test_input.txt"
    test_output = "sorted_output.txt"
    numbers = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42] * 100 
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
    # os.unlink(test_output)
