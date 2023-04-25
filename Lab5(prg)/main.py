import io
import requests
import itertools

class Solution:

    def __init__(self):
        self.A = self.read_int_matrix('l5_a.txt')
        self.B = self.read_int_matrix('l5_b.txt')
        self.N = len(self.A)
        self.P = list(range(self.N))

    def match(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.A[i][j] != self.B[self.P[i]][self.P[j]]:
                    return False
        return True

    def solve(self):
        for p in itertools.permutations(self.P):
            self.P = list(p)
            if self.match():
                for i in range(self.N):
                    print('{{{}: {}}}; '.format(i + 1, self.P[i] + 1))
                break

    def read_int_matrix(self, path):
        with open(path) as f:
            lines = f.readlines()
        number_of_vertices = int(lines[0])
        matrix_lines = [line.strip().split() for line in lines[1:]]
        matrix = [[int(x) for x in row] for row in matrix_lines]
        return matrix

if __name__ == '__main__':
    Solution().solve()
