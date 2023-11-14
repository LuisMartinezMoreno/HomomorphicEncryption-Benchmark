from numpy.polynomial import Polynomial
import numpy as np
# First we set the parameters
M = 0
N = M //2

# We set xi, which will be used in our computations
xi = None

def sigma_inverse(b: np.array) -> Polynomial:
    """Encodes the vector b in a polynomial using an M-th root of unity."""
    M = len(b)*2
    xi = np.exp(2 * np.pi * 1j / M)
    # First we create the Vandermonde matrix
    A = vandermonde(xi, M)
    

    # Then we solve the system
    coeffs = np.linalg.solve(A, b)

    # Finally we output the polynomial
    p = Polynomial(coeffs)
    print(coeffs)
    return p

def sigma(p: Polynomial) -> np.array:
    """Decodes a polynomial by applying it to the M-th roots of unity."""

    outputs = []
    N = M //2

    # We simply apply the polynomial on the roots
    for i in range(N):
        root = xi ** (2 * i + 1)
        output = p(root)
        outputs.append(output)
    print("------------------")
    print(np.array(outputs))
    return np.array(outputs)

def execute(result, printing:bool):
    resultado = sigma_inverse (result)
    sigma(resultado)
    
@staticmethod
def vandermonde(xi: np.complex128, M: int) -> np.array:
    """Computes the Vandermonde matrix from a m-th root of unity."""
        
    N = M //2
    matrix = []
        # We will generate each row of the matrix
    for i in range(N):
        # For each row we select a different root
        root = xi ** (2 * i + 1)
        row = []

        # Then we store its powers
        for j in range(N):
            row.append(root ** j)
        matrix.append(row)
    return matrix
