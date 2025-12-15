def hash_function(key, table_size):
    return sum(ord(char) for char in str(key)) % table_size

def insert_with_collision(table, key, value):
    index = hash_function(key, len(table))
    while table[index] is not None:
        index = (index + 1) % len(table)  # Linear probing
    table[index] = (key, value)

def create_hash_table_with_collision(data, table_size):
    table = [None] * table_size
    for key, value in data.items():
        insert_with_collision(table, key, value)
    return table

def write_table_to_file(table, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for index, item in enumerate(table):
            if item is not None:
                f.write(f'{index}: {item}\n')
            else:
                f.write(f'{index}: None\n')

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
    hash_table = create_hash_table_with_collision(data, table_size)
    write_table_to_file(hash_table, "hash_table_collision.txt")

if __name__ == "__main__":
    main()