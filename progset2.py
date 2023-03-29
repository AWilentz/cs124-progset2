import sys
import numpy as np

def matrix(m1, m2):

    r1 = len(m1)
    c1 = len(m1[0])
    r2 = len(m2)
    c2 = len(m2[0])

    if c1 != r2:
        raise ValueError("Dimensions must match")

    m = [[0 for _ in range(c2)] for _ in range(r1)]

    for i in range(r1):
        for j in range(c2):
            for k in range(r2):
                m[i][j] += m1[i][k] * m2[k][j]

    return m

def strassen(m1, m2, n0):

    r1 = len(m1)
    c1 = len(m1[0])
    r2 = len(m2)
    c2 = len(m2[0])

    padded = False

    n = r1

    if r2 != r1 or c1 != r1 or c2 != r1:
        raise ValueError("Matrices must be square and dimensions must match")
    
    if n <= n0:
        return matrix(m1, m2)
    
    if n == 1:
        return [[m1[0][0] * [0][0]]]
    
    if not power_of_two(n):
        n_ = n
        n = 1<<(n-1).bit_length()
        padded = True
        m1 = np.vstack((m1, [[0 for _ in range(n_)] for _ in range(n-n_)]))  
        m1 = np.hstack((m1, np.transpose([[0 for _ in range(n)] for _ in range(n-n_)])))
        m2 = np.vstack((m2, [[0 for _ in range(n_)] for _ in range(n-n_)]))  
        m2 = np.hstack((m2, np.transpose([[0 for _ in range(n)] for _ in range(n-n_)])))
    
    half = n // 2

    a, b, c, d = split(m1, half)
    e, f, g, h = split(m2, half)

    p1 = strassen(a, subtract(f, h), n0)
    p2 = strassen(add(a, b), h, n0)
    p3 = strassen(add(c, d), e, n0)
    p4 = strassen(d, subtract(g, e), n0)
    p5 = strassen(add(a, d), add(e, h), n0)
    p6 = strassen(subtract(b, d), add(g, h), n0)
    p7 = strassen(subtract(a, c), add(e, f), n0)

    top_left = add(subtract(add(p5, p4), p2), p6)
    top_right = add(p1, p2)
    bottom_left = add(p3, p4)
    bottom_right = subtract(subtract(add(p5, p1), p3), p7)

    m = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(half):
        for j in range(half):
            m[i][j] = top_left[i][j]
            m[i][j + half] = top_right[i][j]
            m[i + half][j] = bottom_left[i][j]
            m[i + half][j + half] = bottom_right[i][j]

    if padded:
        m = [[m[i][j] for j in range(n_)] for i in range(n_)]

    return m

def power_of_two(n):
    if (n & n-1 == 0 and n > 0):
        return True
    return False

def split(m, half):
    return [r[:half] for r in m[:half]], [r[half:] for r in m[:half]], [r[:half] for r in m[half:]], [r[half:] for r in m[half:]]

def add(m1, m2):
    m = [[0 for _ in range(len(m1[0]))] for _ in range(len(m1))]

    for i in range(len(m1)):
        for j in range(len(m1[0])):
            m[i][j] = m1[i][j] + m2[i][j]

    return m

def subtract(m1, m2):
    m = [[0 for _ in range(len(m1[0]))] for _ in range(len(m1))]

    for i in range(len(m1)):
        for j in range(len(m1[0])):
            m[i][j] = m1[i][j] - m2[i][j]

    return m

m1 = [[1, 2, 3], 
      [3, 4, 5], 
      [6, 7, 9]]

m2 = [[3, 4, 5], 
      [1, 2, 3], 
      [6, 7, 9]]

# print(strassen(m1, m2, 1))

def count_triangles(m):
    A3 = strassen(m, strassen(m, m, 20), 20)

    trace = np.trace(A3)

    triangles = trace / 6

    return triangles

def random_graph(n, p):
    m = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            r = np.random.rand()
            if r <= p:
                m[i][j] = 1
                m[j][i] = 1
    return m

# for p in [.01, .02, .03, .04, .05]:
#     print(count_triangles(random_graph(1024, p)))

if len(sys.argv) != 4:
    raise TypeError("Incorrect number of arguments")

if int(sys.argv[1]) != 0:
    raise ValueError("Invalid flag")

dim = int(sys.argv[2])

a = [[0 for _ in range(dim)] for _ in range(dim)]
b = [[0 for _ in range(dim)] for _ in range(dim)]

f = open(sys.argv[3], 'r')

for i in range(dim):
    for j in range(dim):
        a[i][j] = int(f.readline().strip())

for i in range(dim):
    for j in range(dim):
        b[i][j] = int(f.readline().strip())

c = strassen(a, b, 1)

for i in range(dim):
    print(c[i][i])