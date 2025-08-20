import csv
import time
import os

def generate_primes_up_to(n):
    """
    Generates a list of primes up to a given number n using the Sieve of Eratosthenes.
    This list is used for efficient lookup during the analysis.
    """
    # Create a boolean list where is_prime[i] is True if i is potentially prime.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    # Iterate from 2 up to the square root of n.
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark all multiples of i as not prime.
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False
                
    # Return a list of all prime numbers found.
    return [i for i, is_p in enumerate(is_prime) if is_p]

def analyze_prime_offsets_with_filtering(num_primes_to_check=1_000_000):
    """
    Tests the seven specific offsets on the first 'num_primes_to_check' primes,
    grouping the analysis by the ending digit of the prime and filtering out
    multiples of 3 and 5.
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

    # Convert the list to a set for highly efficient O(1) lookups.
    prime_set = set(all_primes)
    
    # Get the first one million primes to be used for the analysis.
    primes_to_check = all_primes[:num_primes_to_check]
    
    # Initialize a nested dictionary to store results for each ending digit and offset.
    # New keys for filtering: 'multiples_of_3', 'multiples_of_5', 'not_multiples_of_3_or_5'
    results = {
        1: {k: {'total': 0, 'successful': 0, 'composites': 0, 'multiples_of_3': 0, 'multiples_of_5': 0, 'not_multiples_of_3_or_5': 0} for k in offsets_k},
        3: {k: {'total': 0, 'successful': 0, 'composites': 0, 'multiples_of_3': 0, 'multiples_of_5': 0, 'not_multiples_of_3_or_5': 0} for k in offsets_k},
        7: {k: {'total': 0, 'successful': 0, 'composites': 0, 'multiples_of_3': 0, 'multiples_of_5': 0, 'not_multiples_of_3_or_5': 0} for k in offsets_k},
        9: {k: {'total': 0, 'successful': 0, 'composites': 0, 'multiples_of_3': 0, 'multiples_of_5': 0, 'not_multiples_of_3_or_5': 0} for k in offsets_k}
    }

    print("\nAnalyzing prime offsets with filtering...")
    start_time = time.time()
    
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
            
            # Check for divisibility by 3 and 5
            is_multiple_of_3 = (candidate % 3 == 0) and (candidate != 3)
            is_multiple_of_5 = (candidate % 5 == 0) and (candidate != 5)

            if is_multiple_of_3:
                results[ending_digit][k]['multiples_of_3'] += 1
            if is_multiple_of_5:
                results[ending_digit][k]['multiples_of_5'] += 1

            # If the candidate is not a multiple of 3 or 5, check for primality.
            if not is_multiple_of_3 and not is_multiple_of_5:
                results[ending_digit][k]['not_multiples_of_3_or_5'] += 1
                
                # Check if the candidate is prime and update the successful/composite counts.
                if candidate > 1 and candidate in prime_set:
                    results[ending_digit][k]['successful'] += 1
                else:
                    results[ending_digit][k]['composites'] += 1
    
    end_time = time.time()
    print(f"Analysis complete. Time taken: {end_time - start_time:.2f} seconds.")

    # Calculate success rates for each entry based on the filtered data.
    for ending_digit, offset_data in results.items():
        for k, counts in offset_data.items():
            if counts['not_multiples_of_3_or_5'] > 0:
                success_rate = (counts['successful'] / counts['not_multiples_of_3_or_5']) * 100
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
                writer.writerow([
                    'Prime Ending',
                    'Offset',
                    'Total Primes',
                    'Successful Primes',
                    'Other Composites',
                    'Multiples of 3',
                    'Multiples of 5',
                    'Not a Multiple of 3 and/or 5',
                    'Success Rate (%)'
                ])
                
                # Iterate through each offset for the current ending digit.
                for offset in ordered_offsets:
                    offset_data = data[ending_digit][offset]
                    row_data = [
                        f'ending_{ending_digit}',
                        f'2p + {offset}' if offset > 0 else f'2p {offset}',
                        offset_data['total'],
                        offset_data['successful'],
                        offset_data['composites'],
                        offset_data['multiples_of_3'],
                        offset_data['multiples_of_5'],
                        offset_data['not_multiples_of_3_or_5'],
                        f"{offset_data['success_rate']:.4f}"
                    ]
                    writer.writerow(row_data)

        print(f"\nResults successfully saved to {filename}")
        print(f"File location: {os.path.abspath(filename)}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")

if __name__ == "__main__":
    results = analyze_prime_offsets_with_filtering()
    
    print("\n" + "="*50)
    
    while True:
        csv_filename = input("What would you like to name the output CSV file? (e.g., prime_analysis_filtered.csv): ")
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
