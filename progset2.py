def matrix(m1, m2):

    r1 = len(m1)
    c1 = len(m1[0])
    r2 = len(m2)
    c2 = len(m2[0])

    if c1 != r2:
        raise ValueError("Matrices cannot be multiplied")

    m = [[0 for _ in range(c2)] for _ in range(r1)]

    for i in range(r1):
        for j in range(c2):
            for k in range(r2):
                result[i][j] += m1[i][k] * m2[k][j]

    return m

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
                result[i][j] += m1[i][k] * m2[k][j]

    return m

def strassen(m1, m2):

    r1 = len(m1)
    c1 = len(m1[0])
    r2 = len(m2)
    c2 = len(m2[0])
    if r2 != r1 or c1 != r1 or c2 != r1:
        raise ValueError("Matrices must be square and dimensions must match")
    
    half = r1 // 2

    # Base case: if the matrix is 1x1, compute and return the product.
    if r1 == 1:
        return [[m1[0][0] * m2[0][0]]]

    # Split each matrix into four submatrices.

    a, b, c, d = split(m1, half)
    e, f, g, h = split(m2, half)

    p1 = strassen(a, subtract(f, h))
    p2 = strassen(add(a, b), h)
    p3 = strassen(add(c, d), e)
    p4 = strassen(d, subtract(g, e))
    p5 = strassen(add(a, d), add(e, g))
    p6 = strassen(subtract(b, d), add(g, h))
    p7 = strassen(subtract(a, c), add(e, f))

    top_left = add(subtract(add(p5, p4), p2), p6)
    top_right = add(p1, p2)
    bottom_left = add(p3, p4)
    bottom_right = subtract(subtract(add(p5, p1), p3), p7)

    m = [[0 for _ in range(r1)] for _ in range(r1)]
    for i in range(half):
        for j in range(half):
            m[i][j] = top_left[i][j]
            m[i][j + half] = top_right[i][j]
            m[i + half][j] = bottom_left[i][j]
            m[i + half][j + half] = bottom_right[i][j]

    return m

def split(m, half):
    return [row[:half] for row in m[:half]], [row[half:] for row in m[:half]], [row[:half] for row in m[half:]], [row[half:] for row in m[half:]]

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