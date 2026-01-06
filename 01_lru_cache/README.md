# LRU Cache

## Problem
Design a cache that evicts the **Least Recently Used** item when capacity is reached.

**Required Operations (both O(1)):**
- `get(key)` - Return value if exists, else -1
- `put(key, value)` - Insert/update, evict LRU if over capacity

## Intuition

The challenge is achieving O(1) for both lookup AND maintaining order.

| Data Structure | Lookup | Insert/Delete | Order Tracking |
|----------------|--------|---------------|----------------|
| Array          | O(n)   | O(n)          | ✓              |
| HashMap        | O(1)   | O(1)          | ✗              |
| Linked List    | O(n)   | O(1)*         | ✓              |

**Solution:** Combine HashMap + Doubly Linked List
- HashMap: `key → node_reference` (O(1) lookup)
- DLL: Maintains access order (O(1) move/remove with node reference)

## Key Design Decisions

### Why Doubly Linked List (not Singly)?
To remove a node in O(1), we need access to its predecessor. DLL gives us `node.prev`.

### Why Dummy Head/Tail?
Eliminates null checks when inserting/removing at boundaries.

```
[HEAD] <-> [Node1] <-> [Node2] <-> [TAIL]
  ↑                                  ↑
dummy                              dummy
```

### Why Store Key in Node?
When evicting, we need to remove from both DLL and HashMap. The node holds the key for HashMap deletion.

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| HashMap + DLL | O(1) operations, optimal | Extra memory for pointers |
| OrderedDict (Python) | Simple code | Language-specific |
| Array + Timestamp | Simple structure | O(n) eviction |

## Common Interview Follow-ups

1. **Thread-safe version?** - Add locks around operations
2. **TTL support?** - Store timestamp, check on access (see kv_store_ttl)
3. **Multiple eviction policies?** - Strategy pattern for LRU/LFU/FIFO
