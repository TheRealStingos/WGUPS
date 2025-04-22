# Creates Hash Table Class
class HashTable:
    def __init__(self, initial_capacity=8):
        self.table = []
        self.size = 0
        self.capacity = initial_capacity
        self.load_factor_threshold = 0.95 # resize when 95% full

        for i in range(initial_capacity):
            self.table.append([])

    # calculate current load factor - O(1)
    def _calculate_load_factor(self):
        return self.size / self.capacity

    # resize table function 0(n)
    def _resize(self, new_size):
        # save old table
        old_table = self.table

        # create new table with expanded capacity
        self.capacity = new_size
        self.table = []
        for i in range(new_size):
            self.table.append([])
        # reset size for rebuild
        self.size = 0
        # rehash all existing items into new table
        for bucket in old_table:
            for key, value in bucket:
                self.add_without_resize(key, value)

    # add method that doesn't trigger resizing - O(n)
    def add_without_resize(self, key, value):
        bucket = hash(key) % self.capacity
        bucket_table = self.table[bucket]

        for kv in bucket_table:
            if kv[0] == key:
                kv[1] = value
                return True

        key_value = [key, value]
        bucket_table.append(key_value)
        self.size += 1
        return True

    # Inserts into hash map - O(n)
    # Citing WGU code repository W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py
    def add(self, key, value):
        if self._calculate_load_factor() >= self.load_factor_threshold:
            self._resize(self.capacity * 2)

        bucket = hash(key) % self.capacity
        bucket_table = self.table[bucket]

        #update key if existing key is found in bucket
        for kv in bucket_table: # Time complexity - 0(N)
            if kv[0] == key:
                kv[1] = value
                return True

        key_value = [key, value]
        bucket_table.append(key_value)
        self.size += 1
        return True

    # Lookup values in the hash table - O(n)
    def lookup(self, key):
        # Calculate bucket index for the key
        bucket_index = hash(key) % self.capacity
        bucket = self.table[bucket_index]
        for pair in bucket:
            if key == pair[0]:
                return pair[1]
        return None

    # method to remove items from hash table - O(n)
    def remove(self, key):
        slot = hash(key) % self.capacity
        bucket = self.table[slot]

        # enumerate through the bucket to get both index and key-value pair
        for i, pair in enumerate(bucket):
            # check if we found the key we want to remove
            if pair[0] == key:
                # removes the entire key-value pair
                bucket.pop(i)
                self.size -= 1

                # check if we need to shrink the table
                if self.size > 0 and self._calculate_load_factor() < .25:
                    self._resize(max(8,self.capacity // 2))
                # return true to indicated successful removal
                return True
        # indicate if key isn't found to user
        return False

    def __len__(self):
        return self.size