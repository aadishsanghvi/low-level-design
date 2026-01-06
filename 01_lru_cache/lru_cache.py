"""
LRU Cache Implementation
========================
A cache that evicts the Least Recently Used item when capacity is reached.

Key Insight:
- HashMap gives O(1) lookup
- Doubly Linked List gives O(1) removal/insertion at any position
- Combine both: HashMap stores key -> node reference, DLL maintains order

Time Complexity: O(1) for both get() and put()
Space Complexity: O(capacity)
"""

class Node:
    """Doubly Linked List Node"""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache using HashMap + Doubly Linked List
    
    Design:
    - HashMap: key -> Node (for O(1) access)
    - DLL: Head = Most Recently Used, Tail = Least Recently Used
    
    On get(key):
        1. If exists, move node to head, return value
        2. If not exists, return -1
    
    On put(key, value):
        1. If exists, update value, move to head
        2. If not exists:
           - Create new node, add to head
           - If over capacity, remove tail node
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # Dummy head and tail for easier edge case handling
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_head(self, node: Node) -> None:
        """Add node right after head (most recent position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node) -> None:
        """Remove node from its current position"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _move_to_head(self, node: Node) -> None:
        """Move existing node to head (mark as recently used)"""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_tail(self) -> Node:
        """Remove and return the least recently used node"""
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node
    
    def get(self, key: int) -> int:
        """
        Get value by key.
        Returns -1 if key doesn't exist.
        Moves accessed item to front (most recently used).
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)  # Mark as recently used
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update key-value pair.
        If over capacity, evicts least recently used item.
        """
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Insert new
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            if len(self.cache) > self.capacity:
                # Evict LRU
                lru = self._remove_tail()
                del self.cache[lru.key]
    
    def __repr__(self) -> str:
        """Show cache contents from MRU to LRU"""
        items = []
        curr = self.head.next
        while curr != self.tail:
            items.append(f"{curr.key}:{curr.value}")
            curr = curr.next
        return f"LRUCache([{', '.join(items)}])"


# ============== DEMO ==============
if __name__ == "__main__":
    print("=== LRU Cache Demo ===\n")
    
    # Create cache with capacity 3
    cache = LRUCache(3)
    
    # Add items
    cache.put(1, 100)
    cache.put(2, 200)
    cache.put(3, 300)
    print(f"After adding 1,2,3: {cache}")
    
    # Access item 1 (moves to front)
    val = cache.get(1)
    print(f"Get key=1: {val}")
    print(f"After get(1): {cache}")
    
    # Add item 4 (should evict key=2, the LRU)
    cache.put(4, 400)
    print(f"After adding 4: {cache}")
    
    # Try to get evicted key
    val = cache.get(2)
    print(f"Get key=2 (evicted): {val}")
    
    # Update existing key
    cache.put(1, 111)
    print(f"After updating 1: {cache}")
    
    print("\n✓ All operations completed!")
