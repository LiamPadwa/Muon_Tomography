#include <fstream>
#include <iostream>
#include <cstring>

// Define buffer size as a global constant
const size_t BUFFER_SIZE = 4096; // 4KB read buffer

/**
 * @brief Compares two binary files for exact equality.
 *
 * This function reads both files in chunks (buffers) and compares the contents
 * byte-by-byte. It is designed for efficiency when working with large files.
 *
 * @param file1 Path to the first file (e.g., the reference/original file).
 * @param file2 Path to the second file (e.g., the new file to verify).
 * @return true if the files are identical in size and content, false otherwise.
 */
bool compareFiles(const std::string& file1, const std::string& file2) {
    // Open both files in binary mode
    std::ifstream f1(file1, std::ios::binary);
    std::ifstream f2(file2, std::ios::binary);

    // Check if either file failed to open
    if (!f1 || !f2) {
        std::cerr << "Error opening one or both files.\n";
        return false;
    }

    // Allocate buffers on the stack
    char buffer1[BUFFER_SIZE];
    char buffer2[BUFFER_SIZE];

    // Read and compare both files chunk by chunk
    while (f1 && f2) {
        f1.read(buffer1, BUFFER_SIZE);
        f2.read(buffer2, BUFFER_SIZE);

        // Check if the number of bytes read differs or content differs
        if (f1.gcount() != f2.gcount() ||
            std::memcmp(buffer1, buffer2, f1.gcount()) != 0) {
            return false;
        }
    }

    // Ensure both files reached EOF (same length)
    return f1.eof() && f2.eof();
}

/**
 * @brief Main function to compare a reference file with a user-specified file.
 *
 * Usage:
 *     ./compare_files path/to/new_file.data
 *
 * The reference file path is hardcoded in `defaultPath`.
 */
int main(int argc, char* argv[]) {
    // Default reference file (update this path to your actual original file)
    const std::string defaultPath = "/Users/liam/Documents/Muon_tomography/Dan_test/windows_linux_comp/linux_154_validation.data";

    // Ensure the user provided a path to the new file
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <path_to_new_file>\n";
        return 1;
    }

    std::string newFilePath = argv[1];

    // Compare the files and report the result
    bool identical = compareFiles(defaultPath, newFilePath);
    if (identical) {
        std::cout << "Files are identical.\n";
    } else {
        std::cout << "Files are different.\n";
    }

    return 0;
}
