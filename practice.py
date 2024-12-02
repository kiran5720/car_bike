# import heapq
# arr=[6, 7, 9, 4, 3, 5, 8, 10, 1]
# heapq.heapify(arr)
# print(arr)


# from collections import deque

# def bfs(root):
#     if not root:
#         return
#     queue = deque([root])  # Use a queue
#     while queue:
#         node = queue.popleft()  # Remove from front
#         print(node.value, end=" ")  # Visit the node
#         if node.left:
#             queue.append(node.left)  # Add left child to queue
#         if node.right:
#             queue.append(node.right)  # Add right child to queue

# Example Tree Structure
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    def __str__(self):
        return str(self.value)

a= Node(1)
b= Node(2)
c= Node(3)
d= Node(4)
e = Node(5)
f = Node(6)
g=Node(7)
h=Node(8)
a.left=b
a.right=c
b.left=d
b.right=e
d.left=f
d.right=g
c.left=h

print(f,"df")

def preorder(node):
    
    if not node:
        return
    print(node,"preorder")
    preorder(node.left)
    preorder(node.right)

preorder(a)

def inorder(node):
    
    if not node:
        return
    
    inorder(node.left)
    print(node,"inorder")
    inorder(node.right)

inorder(a)

def postorder(node):
    
    if not node:
        return
    
    postorder(node.left)
    postorder(node.right)
    print(node,"postorder")

postorder(a)
# print("BFS Traversal:")
# bfs(root.right)

def preorder_iterative(node):
    stk=[node]
    while stk:
        node=stk.pop()
        print(node,"preorder_iterative")
        if node.right:
            stk.append(node.right)
        if node.left:
            stk.append(node.left)
preorder_iterative(a)

from collections import deque
def in_order_bfs(node):
    q=deque()
    q.append(node)
    while q:
        node=q.popleft()
        print(node,"in_order_bfs")
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

in_order_bfs(a)


def find_target(node,target):
    if not node:
        return False
    if node.value==target:
        return True
    return find_target(node.left,target) or find_target(node.right,target)
print(find_target(a,13))