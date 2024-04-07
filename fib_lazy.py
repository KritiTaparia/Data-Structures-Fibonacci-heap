# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNodeLazy:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNodeLazy):
        return self.val == other.val

class FibHeapLazy:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min_pointer = None

    def get_roots(self) -> list:
        return self.roots

    def print_roots(self):
        print([root.val for root in self.roots])

    def insert(self, val: int) -> FibNodeLazy:
        new_node = FibNodeLazy(val)
        self.roots.append(new_node)
        if self.min_pointer is not None:
            if val < self.min_pointer.val:
                self.min_pointer = new_node
        else:
            self.min_pointer = new_node
        return new_node
    
    def join(self, child, parent):
        parent.children.append(child)
        child.parent = parent
        return parent
    
    def separate_node(self, node: FibNodeLazy) -> None:
        copy_parent = node.parent
        
        node.parent = None
        node.flag = False
        if self.min_pointer.val > node.val:
            self.min_pointer = node
        
        if copy_parent is not None:
            copy_parent.children.remove(node)
            self.roots.append(node)
            if copy_parent.flag:
                self.separate_node(copy_parent)
            else:
                copy_parent.flag = True

    def separate_children(self, node, roots):
        # print(node.val if node else None)
        # if not node.flag:
        #     roots.append(node)
        #     return
        for child in node.children:
            child.parent = None
            if child.flag:
                self.separate_children(child, roots)
            else:
                roots.append(child)

    def find_min_lazy(self) -> FibNodeLazy:
        if self.min_pointer.flag == False:
            return self.min_pointer

        new_roots = []
        for x in self.roots:
            if x.flag:   # vacant node
                self.separate_children(x, new_roots)
            else:
                new_roots.append(x)
        self.roots = new_roots[::]

        fib_hash_map = {}
        for x in self.roots:
            degree = len(x.children)
            while fib_hash_map.get(degree) is not None:
                y = fib_hash_map[degree]
                del fib_hash_map[degree]
                # print(x.val if x is not None else x, y.val if y is not None else y, 'join me')
                if x.val > y.val:
                    x = self.join(x, y)
                else:
                    x = self.join(y, x)
                degree += 1
            fib_hash_map[degree] = x
        
        # update root list
        self.roots = []
        for x in fib_hash_map.values():
            if x is not None:
                self.roots.append(x)

        # finding min again
        self.min_pointer = None
        for x in self.roots:
            if self.min_pointer is not None:
                if x.val < self.min_pointer.val:
                    self.min_pointer = x
            else:
                self.min_pointer = x

        return self.min_pointer

    def delete_min_lazy(self) -> None:
        if self.min_pointer.flag:
            self.min_pointer = self.find_min_lazy()
        self.min_pointer.flag = True
        self.min_pointer.val = float('inf')

    def decrease_priority(self, node: FibNodeLazy, new_val: int) -> None:
        node.val = new_val
        if self.min_pointer.val > node.val:
            self.min_pointer = node

        # sceanrio 1 - after decreasing priority, still greater than parent - do nothing
        # scenario 2 - make new tree, mark parent
        if node.parent is not None and node.val < node.parent.val:
            # make a separate tree
            self.separate_node(node)

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
