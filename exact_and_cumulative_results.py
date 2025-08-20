import csv
import time
import os

def generate_primes_up_to(n):
    """
    Generates a list of primes up to a given number n using the Sieve of Eratosthenes.
    The list of primes is used for efficient lookup during the analysis.
    """
    # Create a boolean list where is_prime[i] is True if i is potentially prime.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers.

    # Iterate from 2 up to the square root of n.
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark all multiples of i as not prime.
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False

    # Return a list of all prime numbers found.
    return [i for i, is_p in enumerate(is_prime) if is_p]

def analyze_prime_offsets(num_primes_to_check=1_000_000):
    """
    Tests the seven specific offsets on the first 'num_primes_to_check' primes.
    The offsets are defined by the formula 2p + k.
    """
    # Define the set of offsets to be tested.
    offsets_k = {1, 3, -3, -5, 7, 9, -9}
    
    # The 1,000,000th prime is 15,485,863. We need to check candidates up to 2p + 9.
    # The maximum value for p is 15,485,863, so the max candidate is 2 * 15,485,863 + 9 = 30,971,735.
    # We will generate primes up to a safe upper bound to ensure all candidates are covered.
    max_prime_needed = 31_000_000
    
    print(f"Generating primes up to {max_prime_needed:,}...")
    start_time = time.time()
    # Generate all primes up to the maximum needed value.
    all_primes = generate_primes_up_to(max_prime_needed)
    end_time = time.time()
    print(f"Done. Time taken: {end_time - start_time:.2f} seconds.")

    # Convert the list to a set for highly efficient O(1) lookups.
    prime_set = set(all_primes)
    
    # Get the first one million primes to be used for the analysis.
    primes_to_check = all_primes[:num_primes_to_check]
    
    # Initialize variables for the summary table.
    total_primes_produced = 0
    unique_primes_produced = set()
    
    # Initialize a dictionary to store the exact count of successful offsets.
    exact_success_counts = {i: 0 for i in range(len(offsets_k) + 1)}
    
    # Initialize a new dictionary to store counts for each individual offset.
    individual_offset_counts = {k: 0 for k in offsets_k}
    
    print("\nAnalyzing prime offsets...")
    start_time = time.time()
    
    # Iterate through the first one million primes.
    for p in primes_to_check:
        successful_offsets_count = 0
        produced_primes_for_p = set()
        
        # Check each of the seven offsets for the current prime p.
        for k in offsets_k:
            candidate = 2 * p + k
            # Check if the candidate is a positive number and is in our prime set.
            if candidate > 1 and candidate in prime_set:
                successful_offsets_count += 1
                produced_primes_for_p.add(candidate)
                # Increment the count for this specific individual offset.
                individual_offset_counts[k] += 1
        
        # Increment the counter for the number of successful offsets found for this prime.
        exact_success_counts[successful_offsets_count] += 1
        
        # Add to the total and unique counts for the summary table.
        total_primes_produced += len(produced_primes_for_p)
        unique_primes_produced.update(produced_primes_for_p)

    end_time = time.time()
    print(f"Analysis complete. Time taken: {end_time - start_time:.2f} seconds.")

    # Calculate the cumulative success counts for the third table.
    cumulative_success_counts = {}
    total_sum = 0
    # Iterate from the highest to the lowest count to sum up cumulatively.
    for i in range(len(offsets_k), -1, -1):
        total_sum += exact_success_counts[i]
        cumulative_success_counts[f'at least {i}'] = total_sum

    # Calculate the percentages for both distribution tables.
    for count in exact_success_counts:
        exact_success_counts[count] = (exact_success_counts[count], 
                                       (exact_success_counts[count] / num_primes_to_check) * 100)
    for key in cumulative_success_counts:
        cumulative_success_counts[key] = (cumulative_success_counts[key], 
                                          (cumulative_success_counts[key] / num_primes_to_check) * 100)
    
    # Calculate percentages for the individual offset success counts
    for k in individual_offset_counts:
        count = individual_offset_counts[k]
        individual_offset_counts[k] = (count, (count / num_primes_to_check) * 100)

    # Return a dictionary containing all the final results.
    results = {
        'Summary': {
            'Total primes considered': num_primes_to_check,
            'Total primes produced by offsets': total_primes_produced,
            'Unique primes produced by offsets': len(unique_primes_produced)
        },
        'Exact success count distribution': exact_success_counts,
        'Cumulative success count distribution': cumulative_success_counts,
        'Individual offset success counts': individual_offset_counts
    }
    
    return results

def save_to_csv(data, filename):
    """
    Saves the analysis results to a CSV file in a structured table format.
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the Summary table
            writer.writerow(['Summary', 'Value'])
            for key, value in data['Summary'].items():
                writer.writerow([key, value])
            writer.writerow([]) # Empty row for visual spacing in the CSV
            
            # Write the Exact success count distribution table
            writer.writerow(['Exact success count distribution', '', ''])
            writer.writerow(['Offsets Succeeded', 'Count', 'Percentage'])
            sorted_keys = sorted(data['Exact success count distribution'].keys())
            for key in sorted_keys:
                count, percentage = data['Exact success count distribution'][key]
                writer.writerow([key, count, f'{percentage:.4f}%'])
            writer.writerow([])
            
            # Write the Cumulative success count distribution table
            writer.writerow(['Cumulative success count distribution', '', ''])
            writer.writerow(['Offsets Succeeded', 'Count', 'Percentage'])
            # Sort the keys in descending order for the cumulative table.
            sorted_keys = sorted(data['Cumulative success count distribution'].keys(), 
                                 key=lambda x: int(x.split()[-1]), reverse=True)
            for key in sorted_keys:
                count, percentage = data['Cumulative success count distribution'][key]
                writer.writerow([key, count, f'{percentage:.4f}%'])
            writer.writerow([])

            # Write the new Individual offset success counts table
            writer.writerow(['Individual offset success counts', '', ''])
            writer.writerow(['Offset', 'Successes', 'Percentage'])
            # Sort the offsets for consistent output, e.g., from negative to positive.
            sorted_offsets = sorted(data['Individual offset success counts'].keys())
            for offset in sorted_offsets:
                count, percentage = data['Individual offset success counts'][offset]
                writer.writerow([f'2p+{offset}', count, f'{percentage:.4f}%'])
                
        print(f"\nResults successfully saved to {filename}")
        print(f"File location: {os.path.abspath(filename)}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")

if __name__ == "__main__":
    # Run the main analysis function.
    results = analyze_prime_offsets()
    
    print("\n" + "="*50)
    
    # Loop to ask the user for a filename and handle existing files.
    while True:
        csv_filename = input("What would you like to name the output CSV file? (e.g., prime_analysis.csv): ")
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
