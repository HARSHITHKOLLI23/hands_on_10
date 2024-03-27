class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class HashTable:
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * initial_capacity
        self.load_factor = 0.75
        self.shrink_factor = 0.25

    def hash(self, key):
        A = 0.6180339887  # A random real number 
        return int(self.capacity * ((key * A) % 1))

    def resize(self, grow):
        new_capacity = self.capacity * 2 if grow else self.capacity // 2
        new_table = [None] * new_capacity

        # Rehash all elements
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                index = self.hash(current.key)
                if new_table[index] is None:
                    new_table[index] = current
                    current.prev = None
                    current.next = None
                else:
                    current.next = new_table[index]
                    new_table[index].prev = current
                    new_table[index] = current
                    current.prev = None
                current = current.next

        self.table = new_table
        self.capacity = new_capacity

    def insert(self, key, value):
        index = self.hash(key)
        new_node = Node(key, value)

        # If slot is empty
        if self.table[index] is None:
            self.table[index] = new_node
        else:  # Collision occurred, add to the chain
            new_node.next = self.table[index]
            self.table[index].prev = new_node
            self.table[index] = new_node

        self.size += 1

        # Resize if load factor exceeds 0.75
        if self.size / self.capacity > self.load_factor:
            self.resize(True)

    def remove(self, key):
        index = self.hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.table[index] = current.next
                if current.next:
                    current.next.prev = current.prev
                del current
                self.size -= 1

                # Resize if load factor falls below 0.25
                if self.size / self.capacity < self.shrink_factor:
                    self.resize(False)

                return
            current = current.next

    def get(self, key):
        index = self.hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return -1  # Key not found

    def display(self):
        for i in range(self.capacity):
            current = self.table[i]
            print(f"[{i}]: ", end="")
            while current:
                print(f"({current.key}, {current.value})", end=" ")
                current = current.next
            print()

# Test the HashTable implementation with different input values
hashTable = HashTable()

# Insert some elements
print("Inserting key-value pairs:")
hashTable.insert(101, 10)
hashTable.insert(202, 20)
hashTable.insert(303, 30)
hashTable.insert(404, 170)
hashTable.insert(505, 330)
hashTable.insert(606, 650)

print("HashTable after insertions:")
hashTable.display()

# Remove an element
hashTable.remove(202)
print("HashTable after removal:")
hashTable.display()

# Get value for a key
print("Value for key 303:", hashTable.get(303))

