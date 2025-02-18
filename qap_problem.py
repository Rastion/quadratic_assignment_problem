from qubots.base_problem import BaseProblem
import random, os

class QuadraticAssignmentProblem(BaseProblem):
    """
    This class implements the Quadratic Assignment Problem (QAP).
    
    The instance file must have the following format:
      - The first integer is n, the number of facilities/locations.
      - The next n*n integers represent the distance matrix A (row-major order).
      - The next n*n integers represent the flow matrix B (row-major order).

    A valid solution is a permutation list `p` of length n,
    where p[i] is the facility assigned to location i.
    The objective is to minimize:
         sum_{i=0}^{n-1} sum_{j=0}^{n-1} A[i][j] * B[p[i]][p[j]]
    """
    
    def __init__(self, instance_file):
        self.instance_file = instance_file
        self._load_instance(instance_file)

    def _load_instance(self, filename):

        # Resolve relative path with respect to this module’s directory.
        if not os.path.isabs(filename):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir, filename)


        with open(filename, "r") as f:
            # Read all integers from the file
            data = list(map(int, f.read().split()))
        it = iter(data)
        self.n = next(it)
        # Read the distance matrix A
        self.A = [[next(it) for _ in range(self.n)] for _ in range(self.n)]
        # Read the flow matrix B
        self.B = [[next(it) for _ in range(self.n)] for _ in range(self.n)]

    def evaluate_solution(self, solution) -> float:
        """
        Given a candidate solution (a permutation of 0,...,n-1),
        compute and return the objective value.
        """
        if len(solution) != self.n:
            raise ValueError("Solution length must be equal to n (number of facilities).")
        cost = 0
        for i in range(self.n):
            for j in range(self.n):
                cost += self.A[i][j] * self.B[solution[i]][solution[j]]
        return cost

    def random_solution(self):
        """
        Generate a random permutation of facilities.
        """
        sol = list(range(self.n))
        random.shuffle(sol)
        return sol

    # Optionally, if you plan to use a quantum routine that expects a QUBO,
    # you could implement a transformation here. Otherwise, you can leave it unimplemented.
    def get_qubo(self):
        raise NotImplementedError("QUBO transformation is not implemented for QAP.")
