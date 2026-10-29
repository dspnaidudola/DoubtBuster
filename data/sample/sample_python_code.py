# Sample Python Code with a Recursion Doubt
# Problem: Compute nth Fibonacci number recursively

def fibonacci(n: int) -> int:
    # Base cases
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    # Recursive step
    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__":
    print("Fibonacci(6) is:", fibonacci(6))
