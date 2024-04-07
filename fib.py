# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNode:
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

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min_pointer = None

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        new_node = FibNode(val)
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

    def delete_min(self) -> None:
        # separate children to make separate trees
        for child in self.min_pointer.children:
            child.parent = None
            self.roots.append(child)
            child.flag = False
        self.min_pointer.children = None

        self.roots.remove(self.min_pointer)   # remove from root list

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


    def find_min(self) -> FibNode:
        return self.min_pointer

    def separate_node(self, node: FibNode) -> None:
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

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
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
