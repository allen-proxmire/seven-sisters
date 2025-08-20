import time
import math
import csv
from collections import defaultdict

def generate_primes_up_to(n):
    """
    Generates all prime numbers up to a given number n using the Sieve of Eratosthenes.
    Returns a list of primes.
    """
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            for multiple in range(i * i, n + 1, i):
                sieve[multiple] = False
    
    primes = []
    for i in range(2, n + 1):
        if sieve[i]:
            primes.append(i)
    return primes

def get_first_n_primes(n):
    """
    Generates the first n prime numbers.
    This is more efficient than generating all primes up to a number
    and then slicing the list.
    """
    primes = []
    # Start with a reasonable upper bound based on the Prime Number Theorem.
    # The nth prime is approximately n * ln(n)
    limit = int(n * (math.log(n) + math.log(math.log(n))))
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, limit + 1):
        if sieve[i]:
            primes.append(i)
            if len(primes) >= n:
                break
            for multiple in range(i*i, limit + 1, i):
                sieve[multiple] = False
                
    return primes[:n]

def get_smallest_prime_factor(n, prime_list):
    """
    Finds the smallest prime factor of a composite number using the pre-generated
    list of primes for efficient trial division.
    """
    for p in prime_list:
        if p * p > n:
            break
        if n % p == 0:
            return p
    # If no prime factor is found, the number is likely prime itself,
    # or the factor is larger than our largest prime in the list.
    # For this script's purpose, we can assume it's prime if not found.
    return None

# --- Main script execution ---

# 1. Define the number of primes to test.
NUM_PRIMES_TO_CHECK = 1_000_000

# 2. Define the offsets to test.
OFFSETS = [1, 3, -3, -5, 7, 9, -9]
OFFSET_LABELS = {1: "2p+1", 3: "2p+3", -3: "2p-3", -5: "2p-5", 7: "2p+7", 9: "2p+9", -9: "2p-9"}

print(f"Generating the first {NUM_PRIMES_TO_CHECK:,} primes...")
start_time = time.time()
primes_to_check = get_first_n_primes(NUM_PRIMES_TO_CHECK)
end_time = time.time()
print(f"Done. Time taken: {end_time - start_time:.2f} seconds.")

# Find the maximum possible candidate value to create an efficient prime set for lookup
max_prime_to_check = primes_to_check[-1]
max_candidate = 2 * max_prime_to_check + max(OFFSETS)
print(f"Largest prime considered: {max_prime_to_check:,}")
print(f"Generating primes up to {max_candidate:,} for efficient lookup...")
start_time = time.time()
all_primes_for_lookup = generate_primes_up_to(max_candidate)
prime_set = set(all_primes_for_lookup)
end_time = time.time()
print(f"Done. Time taken: {end_time - start_time:.2f} seconds.")
print("-" * 50)

# 3. Analyze each prime and its offset results.
smallest_prime_factor_counts = defaultdict(int)
prime_success_counts = defaultdict(int)
total_tests = 0

print("Analyzing prime offsets...")
start_time = time.time()
for p in primes_to_check:
    for offset in OFFSETS:
        total_tests += 1
        q = 2 * p + offset
        
        # We need to make sure the candidate is within our prime set range
        if q > max_candidate or q <= 1:
            continue
            
        if q in prime_set:
            prime_success_counts[offset] += 1
        else:
            factor = get_smallest_prime_factor(q, all_primes_for_lookup)
            if factor:
                smallest_prime_factor_counts[factor] += 1
end_time = time.time()
print(f"Analysis complete. Time taken: {end_time - start_time:.2f} seconds.")
print("-" * 50)

# 4. Write the final report to a CSV file.
file_name = input("Please enter a name for the CSV file (e.g., 'analysis_results.csv'): ")
if not file_name.endswith(".csv"):
    file_name += ".csv"
print(f"Writing results to '{file_name}'...")

with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(["Analysis of Smallest Prime Factors of Failed Tests", "Value"])
    writer.writerow(["Total tests performed", total_tests])
    writer.writerow(["Total successful prime generations", sum(prime_success_counts.values())])
    writer.writerow([])
    
    writer.writerow(["Smallest Prime Factors Causing Failure", "Count", "Percentage of Failures"])
    total_failures = total_tests - sum(prime_success_counts.values())
    
    # Sort the factors to present the data clearly
    sorted_factors = sorted(smallest_prime_factor_counts.keys())
    
    for factor in sorted_factors:
        count = smallest_prime_factor_counts[factor]
        percentage = (count / total_failures) * 100 if total_failures > 0 else 0
        writer.writerow([factor, count, f"{percentage:.2f}%"])
    
print("Analysis CSV file has been created successfully.")
