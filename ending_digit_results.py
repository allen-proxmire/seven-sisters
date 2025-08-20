import csv
import time
import os

def generate_primes_up_to(n):
    """
    Generates a list of primes up to a given number n using the Sieve of Eratosthenes.
    This list is used for efficient lookup during the analysis.
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False
    return [i for i, is_p in enumerate(is_prime) if is_p]

def analyze_prime_offsets_by_ending_digit(num_primes_to_check=1_000_000):
    """
    Tests the seven specific offsets on the first 'num_primes_to_check' primes,
    grouping the analysis by the ending digit of the prime.
    """
    # Define the set of offsets to be tested.
    offsets_k = {1, 3, -3, -5, 7, 9, -9}
    
    # The 1,000,000th prime is 15,485,863. The max candidate is 2*15485863 + 9 = 30971735.
    max_prime_needed = 31_000_000
    
    print(f"Generating primes up to {max_prime_needed:,}...")
    start_time = time.time()
    all_primes = generate_primes_up_to(max_prime_needed)
    end_time = time.time()
    print(f"Done. Time taken: {end_time - start_time:.2f} seconds.")

    prime_set = set(all_primes)
    primes_to_check = all_primes[:num_primes_to_check]
    
    # Initialize a nested dictionary to store results for each ending digit and offset.
    results = {
        1: {k: {'total': 0, 'successful': 0, 'composites': 0} for k in offsets_k},
        3: {k: {'total': 0, 'successful': 0, 'composites': 0} for k in offsets_k},
        7: {k: {'total': 0, 'successful': 0, 'composites': 0} for k in offsets_k},
        9: {k: {'total': 0, 'successful': 0, 'composites': 0} for k in offsets_k}
    }

    print("\nAnalyzing prime offsets by ending digit...")
    start_time = time.time()
    
    # We will use a separate dictionary to hold total counts for each ending digit,
    # as not every prime is checked against every offset.
    ending_digit_counts = {1: 0, 3: 0, 7: 0, 9: 0}

    for p in primes_to_check:
        # We only consider primes ending in 1, 3, 7, or 9.
        # Primes 2 and 5 are not included in this analysis.
        if p == 2 or p == 5:
            continue
            
        ending_digit = p % 10
        
        # We check each offset for the prime p and increment the correct counts.
        for k in offsets_k:
            candidate = 2 * p + k
            
            # Update the total count for this specific prime ending and offset.
            results[ending_digit][k]['total'] += 1
            
            # Check if the candidate is prime and update the successful/composite counts.
            if candidate > 1 and candidate in prime_set:
                results[ending_digit][k]['successful'] += 1
            else:
                results[ending_digit][k]['composites'] += 1
    
    end_time = time.time()
    print(f"Analysis complete. Time taken: {end_time - start_time:.2f} seconds.")

    # Calculate success rates for each entry.
    for ending_digit, offset_data in results.items():
        for k, counts in offset_data.items():
            if counts['total'] > 0:
                success_rate = (counts['successful'] / counts['total']) * 100
                results[ending_digit][k]['success_rate'] = success_rate
            else:
                results[ending_digit][k]['success_rate'] = 0.0

    return results

def save_to_csv(data, filename):
    """
    Saves the analysis results to a CSV file in the specified table format.
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Define the order of the offsets for consistent output.
            ordered_offsets = sorted(data[1].keys())
            
            # Iterate through each prime ending digit to write the tables.
            for ending_digit in sorted(data.keys()):
                writer.writerow([])
                writer.writerow(['Prime Ending', 'Offset', 'Total Primes', 'Successful Primes', 'Other Composites', 'Success Rate (%)'])
                
                # Iterate through each offset for the current ending digit.
                for offset in ordered_offsets:
                    offset_data = data[ending_digit][offset]
                    row_data = [
                        f'ending_{ending_digit}',
                        f'2p + {offset}' if offset > 0 else f'2p {offset}',
                        offset_data['total'],
                        offset_data['successful'],
                        offset_data['composites'],
                        f"{offset_data['success_rate']:.4f}"
                    ]
                    writer.writerow(row_data)

        print(f"\nResults successfully saved to {filename}")
        print(f"File location: {os.path.abspath(filename)}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")

if __name__ == "__main__":
    results = analyze_prime_offsets_by_ending_digit()
    
    print("\n" + "="*50)
    
    while True:
        csv_filename = input("What would you like to name the output CSV file? (e.g., prime_analysis_by_digit.csv): ")
        if not csv_filename.endswith('.csv'):
            csv_filename += '.csv'
        if not os.path.exists(csv_filename):
            save_to_csv(results, csv_filename)
            break
        else:
            overwrite = input(f"File '{csv_filename}' already exists. Do you want to overwrite it? (y/n): ").lower()
            if overwrite == 'y':
                save_to_csv(results, csv_filename)
                break
            else:
                print("Please choose a different name.")
