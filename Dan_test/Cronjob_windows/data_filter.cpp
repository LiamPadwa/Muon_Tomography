#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>

bool isValidField(int index) {
    static const std::unordered_set<int> validIndices = {
        1,2,3,4,
        5,6,7,8,9,10,11,12,13,
        14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
        78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,
        110,111,112,113,114,115,116,117,118,
        119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,
        183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,
        215,216,217,218,219,220,221,222,223,
        224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,
        288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,
        320,321,322,323,324,325,326,327,328,
        329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,
        393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424
    };
    return validIndices.count(index) > 0;
}

bool endsLine(int index) {
    static const std::unordered_set<int> newlines = {
        4, 13, 45, 109, 118, 150, 214, 223, 255, 319, 328, 360, 424
    };
    return newlines.count(index) > 0;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: ./data_filter input.data output.data\n";
        return 1;
    }

    std::ifstream infile(argv[1]);
    std::ofstream outfile(argv[2]);

    if (!infile.is_open() || !outfile.is_open()) {
        std::cerr << "Failed to open input or output file.\n";
        return 1;
    }

    std::string line;
    while (std::getline(infile, line)) {
        std::vector<std::string> fields;
        std::stringstream ss(line);
        std::string item;
        while (std::getline(ss, item, ';')) {
            fields.push_back(item);
        }

        if (fields.size() < 4) continue;

        try {
            int cluster = std::stoi(fields[3]);
            if (cluster != 4) continue;
        } catch (...) {
            continue; // Skip headers or malformed lines
        }

        outfile << "1234BBBB1234, \n";

        bool firstField = true;
        for (size_t i = 0; i < fields.size(); ++i) {
            int index = static_cast<int>(i + 1); // 1-based index
            if (isValidField(index)) {
                if (!firstField) {
                    outfile << ",";
                }
                outfile << fields[i];
                firstField = false;

                if (endsLine(index)) {
                    outfile << "\n";
                    firstField = true; // reset for new line
                }
            }
        }
    }

    infile.close();
    outfile.close();
    return 0;
}
