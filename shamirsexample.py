import random, math

# Function to calculate the value of y
# y = poly[0] + x * poly[1] + x^2 * poly[2] + ...

def calculate_y(x, poly):
    y = 0
    temp = 1
    
    for coeff in poly:
        y = y + (coeff * temp)
        temp = temp * x
        
    return y

# Function to perform the secret sharing algorithm
# and encode the given secret

def secret_sharing(S, N, K):
    # a list to store the polynomial coeffs.
    # of degree k - 1
    poly = [0] * K
    
    # poly[0] is the secret
    poly [0] = S
    
    # randomly choose k - 1 nonzero numbers
    for j in range(1, K):
        p = 0
        while p == 0:
            p = random.randint(0, 996)
        poly[j] = p
    
    # generate n pointers from the polynomial
    points = []
    for j in range(1, N + 1):
        x = j
        y = calculate_y(x, poly)
        points.append((x,y))
    return points

class Fraction:
    def __init__(self, n, d):
        self.num = n
        self.den = d
        self.reduce_fraction()
        
    def reduce_fraction(self):
        gcd = math.gcd(self.num, self.den)
        self.num //= gcd
        self.den //= gcd

        # keep denominator positive
        if self.den < 0:
            self.num = -self.num
            self.den = -self.den
    
    def __mul__(self, other):
        return Fraction(self.num * other.num, self.den * other.den)
    
    def __add__ (self, other):
        return Fraction(
            self.num * other.den + self.den * other.num,
            self.den * other.den)
    
# Function to generate the secret back from the given points
# using lagrange basis polynomial

def generate_secret(x, y, M):
    ans = Fraction(0, 1)
    
    for i in range(M):
        l = Fraction(y[i], 1)
        
        for j in range(M):
            if i != j:
                temp = Fraction(-x[j], x[i] - x[j])
                l = l * temp
        ans = ans + l
    return ans.num

# Function to encode and decode the secret

def operations(S, N, K):
    points = secret_sharing(S, N, K)
    
    print(f"Secret is split into {N} parts -")
    for point in points:
        print(point[0], point[1])
        
    print(f"Secret can be generated from any of {K} parts")
    
    # input any M points from these to get back the secret code
    # can be dynamic
    M = 2
    
    # M can be greater than or equal to threshold
    # this example uses the threshold
    if M < K:
        print(f"points are less than threshold {K} points required")
        return 
    x = [points[i][0] for i in range(M)]
    y = [points[i][1] for i in range(M)]
    
    print("secret code is:", generate_secret(x, y, M))
    
# driver code
if __name__ == "__main__":
    
    # change these values to change the example
    # S is the secret
    # N is the amount of parts the secret is split into
    # K is the minimum parts needed to reconstruct the secret
    S = 65
    N = 4
    K = 2
    
    operations(S, N, K)
