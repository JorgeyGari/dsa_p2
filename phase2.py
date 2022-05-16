# CODE BY: Laura Belizón Merchán and Jorge Lázaro Ruiz
# USAGE OF THIS CODE IS STRICTLY FOR REFERENCE ONLY, DO NOT COPY

# File "bst" provided by the professors
from bst import BinaryNode
from bst import BinarySearchTree


def left_rotation(node) -> BinaryNode:
    """ performs a left rotation on the subtree of the given node"""
    temp = node.right  # Store the right child
    temp2 = temp.left  # Store the right-left grandchild (in case it exists)

    temp.left = node  # Downgrade the root to right-left grandchild
    node.right = temp2  # Upgrade the right-left grandchild (if it exists) to right child

    return temp  # Return the new root


def right_rotation(node) -> BinaryNode:
    """ performs a right rotation on the subtree of the given node"""
    temp = node.left  # Store the left child
    temp2 = temp.right  # Store the left-right grandchild (in case it exists)

    temp.right = node  # Downgrade the root to left-right grandchild
    node.left = temp2  # Upgrade the left right grandchild (if it exists) to right child

    return temp  # Return the new root


class AVLTree(BinarySearchTree):

    # Override insert method from base class to keep it as AVL
    def insert(self, elem: object) -> None:
        """inserts a new node, with key and element elem"""
        self._root = self._insert(self._root, elem)

    def _insert(self, node: BinaryNode, elem: object) -> BinaryNode:
        """gets a node, searches the place to insert a new node with element e (using super()._insert),  and then,
        the function has to balance the node returned by the function super.()_insert"""
        node = super()._insert(node, elem)
        node = self._rebalance(node)
        return node

    # Override remove method from base class to keep it as AVL
    def remove(self, elem: object) -> None:
        self._root = self._remove(self._root, elem)

    def _remove(self, node: BinaryNode, elem: object) -> BinaryNode:
        """ gets a node, searches the node with element elem in the subtree that hangs down node , and
        then remove this node (using super()._remove). After this, the function has to balance the node returned by
        the function super()._remove"""
        node = super()._remove(node, elem)
        node = self._rebalance(node)
        return node

    def _rebalance(self, node: BinaryNode) -> BinaryNode:
        """ gets node and balances it"""
        b = self.check_balance(node)

        if b > 1 and node.left.left:  # Case where we have a heavier right subtree and a left-left grandchild
            return right_rotation(node)  # We just need to perform a simple right rotation

        if b < -1 and node.right.right:  # Case where we have a heavier left subtree and a right-right grandchild
            return left_rotation(node)  # We just need to perform a simple left rotation

        if b > 1 and node.left.right:  # Case where we have a heavier right subtree and a left-right grandchild
            node.left = left_rotation(node.left)  # Double rotation: first rotate left child to the left...
            return right_rotation(node)  # ...and after that we can perform a simple right rotation

        if b < -1 and node.right.left:  # Case where we have a heavier left subtree
            node.right = right_rotation(node.right)  # Double rotation: first rotate right child to the right...
            return left_rotation(node)  # ...and after that we can perform a simple left rotation

        return node  # Return the root of the subtree

    def check_balance(self, node) -> int:
        """ returns the height difference between the left and right subtrees of the given node
        (positive value if left is longer; negative value if right is longer)"""
        if not node:
            return 0  # In case the given node is deleted

        return self._height(node.left) - self._height(node.right)
