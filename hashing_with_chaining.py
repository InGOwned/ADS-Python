def hash_function(key, table_size):
    return sum(ord(char) for char in str(key)) % table_size

def insert_with_chaining(table, key, value):
    index = hash_function(key, len(table))
    table[index].append((key, value))

def create_hash_table_with_chaining(data, table_size):
    table = [[] for _ in range(table_size)]
    for key, value in data.items():
        insert_with_chaining(table, key, value)
    return table

def write_table_to_file(table, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for index, items in enumerate(table):
            if items:
                f.write(f'{index}: {items}\n')
            else:
                f.write(f'{index}: []\n')

def main():
    # Example data
    data = {
        "apple": 1,
        "banana": 2,
        "orange": 3,
        "grape": 4,
        "peach": 5
    }
    table_size = 10
    hash_table = create_hash_table_with_chaining(data, table_size)
    write_table_to_file(hash_table, "hash_table_chaining.txt")

if __name__ == "__main__":
    main()