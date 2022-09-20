# Laura Belizón Merchán (100452273)
# Jorge Lázaro Ruiz (100452172)

from math import ceil, floor
from slist import SList, SNode


class SList2(SList):

    # Auxiliary function
    def getAtNode(self, index) -> SNode or None:
        """Returns the node in the position n."""

        if index not in range(0, len(self)):
            print("Error: Index is out of bounds.")
            return None
        else:
            nodeIt = self._head
            i = 0
            while nodeIt and i < index:
                nodeIt = nodeIt.next
                i += 1

        # nodeIt is now at the index position
        return nodeIt

    # Function 1
    def sumLastN(self, n) -> int or None:
        """Takes an integer n as input and returns the sum of the last n nodes of the calling list."""

        if self.isEmpty():
            print("List is empty.")
            return 0

        if n < 0:
            return None

        if n > self._size:
            n = self._size

        node = self.getAtNode(self._size - n)  # Get the node of the first element we have to add
        result = 0  # Initialize sum as 0

        if node:  # We check that getAtNode has worked correctly
            while node is not None:  # Keep adding until we reach the last node (included)
                result += node.elem
                node = node.next

            return result

    # Function 2
    def insertMiddle(self, elem) -> None:
        """Inserts the element e in the middle of the calling list."""

        if self._size <= 1:
            self.addLast(elem)  # If the list is empty or contains a single element, insertMiddle works like addLast
        else:
            node = self.getAtNode(ceil(self._size / 2) - 1)  # Using ceil helps us avoid distinguishing odd/even cases

            if node:  # We check that getAtNode has worked correctly
                nextnode = node.next
                node.next = SNode(elem, nextnode)
                node.next.next = nextnode
                self._size += 1

    # Function 3
    def insertList(self, inputList, start, end) -> None:
        """Removes all elements from the calling list between the start and end positions and inserts the elements
        from the inputList instead."""

        # Check if parameters are correct:
        if start < 0:
            print("Error: Start position must be a nonnegative number.")
            return None

        if start > end:
            print("Error: Start position must be smaller than end position.")
            return None

        if end >= len(self):
            print("Error: End position is out of bounds.")
            return None

        # Get to the node directly before the start position
        if start == 0:
            startprev = self._head
            end -= 1
        else:
            startprev = self.getAtNode(start - 1)

        node = startprev  # Save a reference

        # Advance to the node directly after end and save its reference as "node"
        for x in range(start - 1, end + 1):
            node = node.next

        # Change the next reference to the head of the inputList (therefore, we insert the inputList)
        startprev.next = inputList._head
        nodeInput = startprev.next

        # Get to the end of the inputList
        while nodeInput.next:
            nodeInput = nodeInput.next

        # Change the next reference to the node after end
        nodeInput.next = node

        # In case we deleted the head
        if start == 0:
            self._head = self._head.next

        # Finally, we need to recalculate the self._size
        self._size = self._size - (end + 1 - (start - 1)) + inputList._size

        return None

    # Function 4
    def reverseK(self, k) -> None:
        """Inverts the list in groups of k elements."""

        # Check for errors and special cases:
        if self.isEmpty():
            print("List is empty.")
            return None

        if k <= 0:
            print("Error: Groups must have a positive number of elements.")
            return None

        if k == 1:
            return None

        if k > self._size:
            k = self._size

        # Main algorithm
        prevnode = None
        node = self._head
        for group in range(0, floor(self._size / k)):
            starting_node = node  # This will be the last node after reversing

            for x in range(0, k):
                # Invert the .next references
                nextnode = node.next
                node.next = prevnode

                # Advance the node references
                prevnode = node

                # But if this is not the first group...
                if group != 0 and x == k - 1:
                    # ...before continuing to the next group, we want to reattach the list to the left
                    old_starting_node.next = node
                    # This line is locked behind an if statement that ensures old_starting_node has been declared

                node = nextnode

            if group == 0:  # Update head if the group we just reversed was the first group
                self._head = prevnode

            starting_node.next = nextnode  # Reattach to the right with next part of the list
            node = nextnode  # And continue from there

            old_starting_node = starting_node  # Saving this node will be useful when we need to reattach from the right

        # When there aren't enough remaining elements to form a new group, we simply reverse the rest
        prevnode = None
        while node:
            # Invert the .next references
            nextnode = node.next
            node.next = prevnode

            # Advance the node references
            prevnode = node
            node = nextnode
        starting_node.next = prevnode  # Reattach to the left

        return None

    # Function 5
    def maximumPair(self) -> int or None:
        """Returns the maximum value of the sum of equidistant elements in a list."""

        if self.isEmpty():
            print("List is empty.")
            return None
        elif self._size == 1:
            return self._head.elem
            # If there is only one element in the list, its value is considered the maximum

        # Split our list into two halves
        left = SList2()
        right = SList2()

        node = self._head
        for x in range(0, ceil(len(self) / 2)):  # ceil helps us avoid distinguishing between odd/even cases
            left.addLast(node.elem)  # Left half of the list (includes middle node if it exists)
            node = node.next

        while node:
            right.addLast(node.elem)  # Right half of the list
            node = node.next

        # In order to add up equidistant elements, we use reverseK to reverse the right list
        right.reverseK(len(right))

        # And if the list was odd, we also add a 0 that will be added to our middle node
        if len(self) % 2 == 1:
            right.addLast(0)

        # Now we can iterate through our two halves and add elements up
        leftnode = left._head
        rightnode = right._head
        sum = 0

        while leftnode:  # We could also iterate with rightnode as both have the same number of elements
            # A simple "find maximum" algorithm
            if leftnode.elem + rightnode.elem > sum:
                sum = leftnode.elem + rightnode.elem

            leftnode = leftnode.next
            rightnode = rightnode.next

        return sum
