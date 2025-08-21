# The Seven Sisters: Prime Generation based on the Form $2p + k$

This repository contains the computational note, data, and Python scripts related to the paper, "The Seven Sisters: Prime Generation based on the Form $2p+k$." The project explores the effectiveness of a simple linear formula for generating new prime numbers.

### **About the Project**

The "Seven Sisters" are a set of seven specific offsets applied to a given prime $p$ in the form $2p+k$. Through an analysis of the first one million primes, the study demonstrates that this method is highly effective, with the collective offsets generating a unique prime 80.15% of the time.

Addtional findings include the dramatic increase in success rates for specific offsets (+1, -5, and +7) when composites divisible by 3 and 5 are filtered out which highlights the true effectiveness of these offsets. Furthermore, the results demonstrate the unique, and superior, performance of the $2p+7$ offset.  This research offers a glimpse into the underlying structure of prime number distribution and a practical method for primality production.

### **Repository Contents**

* `the_seven_sisters_note.pdf`: The complete computational note, which details the methodology, results, and discussion of the project. This is the paper we've been working on.

* `data/`: This directory contains the raw and processed data used for the analysis, including lists of primes and success counts.

* `src/`: This directory contains the Python scripts used to run the analysis, including the code for prime generation, offset application, and data processing.

### **Getting Started**

To replicate the analysis, clone this repository and run the Python scripts in the `src/` directory.

git clone https://github.com/allen-proxmire/seven-sisters.git
cd seven-sisters


### **Author**

This project was conducted by Allen Proxmire.

\*Unaffiliated

### **Citation**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16916095.svg)](https://doi.org/10.5281/zenodo.16916095)

### **Contact**

For any questions or feedback, please contact me
