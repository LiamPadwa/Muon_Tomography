#include <fstream>
#include <iostream>
#include <cstdlib>

/**
 * @brief Creates a binary .data file filled with random integer values.
 *
 * This function generates a specified number of random integer values 
 * and writes them to a binary file. The random number generator is seeded 
 * with a fixed value to ensure repeatability of the generated data. 
 *
 * @param filename The name of the output file to store the generated data.
 * @param numEntries The number of random integer entries to generate and write.
 */
void createDataFile(const std::string& filename, size_t numEntries) {
    // Open the file in binary mode for writing
    std::ofstream outFile(filename, std::ios::binary);
    
    // Check if the file was successfully opened
    if (!outFile) {
        std::cerr << "Error opening file for writing: " << filename << std::endl;
        return;
    }

    // Set a fixed seed for repeatable random number generation
    // Using a fixed seed ensures the output is the same every time the program runs.
    std::srand(42);  // Fixed seed for repeatable results

    // Generate random data and write to the file
    for (size_t i = 0; i < numEntries; ++i) {
        // Generate a random integer between 0 and 999
        int randomData = std::rand() % 1000;  // Random integer between 0 and 999
        
        // Write the generated integer to the binary file
        outFile.write(reinterpret_cast<char*>(&randomData), sizeof(randomData));
    }

    // Close the output file after writing is complete
    outFile.close();

    // Inform the user that the file has been successfully created
    std::cout << "File created successfully: " << filename << std::endl;
}

/**
 * @brief Main function to execute the file creation process.
 *
 * This function specifies the file name and number of entries to be generated,
 * then calls the createDataFile function to write the random data to the file.
 */
int main() {
    // Specify the name of the output file
    std::string filename = "sample_data_randomised.data";  // Name of the output file
    
    // Specify the number of random data entries to generate
    size_t numEntries = 100;  // Number of entries to write

    // Create the data file with random entries
    createDataFile(filename, numEntries);

    return 0;
}
