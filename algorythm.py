import numpy as np

X = np.array([[ 0.61, 0.71, -0.05],
                [ -1.03, -2.05,  0.87],
                [ 2.5, -3.12,  5.03]])
Y = np.array([[1.], [2.], [2.]])

A = np.concatenate((X, Y), axis=1)

def solve_sistem(X,Y):
    A = np.concatenate((X, Y), axis=1)
    # Приведение матрицы к треугольному виду
    for i in range(len(A)):
        amax = A[i][i]
        for j in range(i+1, len(A)):
            if A[j][i]>amax:
                amax = A[j][i]
                l = j

        a = np.array(A[i])
        b = np.array(A[l])
        A[i] = b
        A[l] = a

    for i in range(len(A)):
        A[i] = A[i] / A[i][i]
        for k in range(len(A)):
            if k!=i:
                A[k] = A[k] - A[k][i]*A[i]
    return A[0:3,3]

if __name__ == '__main__':
    X = np.array([[ 0.61, 0.71, -0.05],
                    [ -1.03, -2.05,  0.87],
                    [ 2.5, -3.12,  5.03]])
    Y = np.array([[-0.16], [0.5], [0.95]])
    print(solve_sistem(X,Y))
# A = np.array([A[i] for i in range(len(A)-1, -1, -1)])
# print(A)
#
# print()
# for i in range(len(A)):
#     # print(A[i][i-1])
#     # A[i] = A[i] / A[i][i]
#     print(A)
#
#     for k in range(len(A)):
#         A[k] = A[k] - A[k][i]*A[i+1]
#
# print(A)
