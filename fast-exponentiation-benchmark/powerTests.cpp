#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>
#define NOMINMAX
#include <windows.h>
#include <psapi.h>
#include <cstdlib>

double power(double base, long long exponent)
{
    if (exponent == 0)
        return 1;

    double temp = power(base, exponent / 2);

    if (exponent % 2 == 0)
        return temp * temp;
    else
        return base * temp * temp;
}

long long getCurrentTimeMicroseconds() {
    using Clock = std::chrono::high_resolution_clock;
    return std::chrono::duration_cast<std::chrono::microseconds>(
        Clock::now().time_since_epoch()).count();
}

long long getPeakRssKb() {
    PROCESS_MEMORY_COUNTERS memInfo;
    GetProcessMemoryInfo(GetCurrentProcess(), &memInfo, sizeof(memInfo));
    return memInfo.PeakWorkingSetSize / 1024;
}

struct Record {
    double base;
    long long exponent;
    double timeMs;
    long long memoryKb;
};

void writeGnuplotScript(const std::string& fileName,
                        const std::string& title,
                        const std::string& yLabel,
                        int column) {
    std::ofstream gp(fileName);
    gp << "set terminal pngcairo size 900,600\n";
    gp << "set datafile separator ','\n";
    gp << "set xlabel 'Test Case Index'\n";
    gp << "set ylabel '" << yLabel << "'\n";
    gp << "set title '" << title << "'\n";
    gp << "set grid\n";
    gp << "plot 'results.csv' using 1:" << column
       << " with linespoints lw 2 title ''\n";
}

void runGnuplot(const std::string& scriptFile, const std::string& pngFile) {
    std::string command = "gnuplot " + scriptFile;
}

int main(int argc, char* argv[]) {
    std::string inputFile = (argc > 1) ? argv[1] : "input.txt";
    std::vector<Record> results;

    std::ifstream inputStream(inputFile);

    double base;
    long long exponent;
    long long rssBefore = getPeakRssKb();

    while (inputStream >> base >> exponent) {
        long long startTime = getCurrentTimeMicroseconds();
        double result = power(base, exponent);
        long long endTime = getCurrentTimeMicroseconds();

        long long rssAfter = getPeakRssKb();
        long long memoryUsed = std::max(0LL, rssAfter - rssBefore);
        rssBefore = rssAfter;

        results.push_back({base, exponent, (endTime - startTime) / 1000.0, memoryUsed});
    }

    std::ofstream csv("results.csv");
    csv << "index,base,exponent,time_ms,memory_kb\n";
    for (std::size_t i = 0; i < results.size(); ++i) {
        csv << i + 1 << ',' << results[i].base << ',' << results[i].exponent << ','
            << std::fixed << std::setprecision(6) << results[i].timeMs << ','
            << results[i].memoryKb << '\n';
    }

    std::ofstream txt("results.txt");
    txt << std::left << std::setw(6) << "Idx"
        << std::setw(14) << "Base"
        << std::setw(14) << "Exponent"
        << std::setw(16) << "Time (ms)"
        << "Memory (kB)\n"
        << std::string(60, '-') << '\n';

    for (std::size_t i = 0; i < results.size(); ++i) {
        txt << std::setw(6) << i + 1
            << std::setw(14) << results[i].base
            << std::setw(14) << results[i].exponent
            << std::setw(16) << std::fixed << std::setprecision(6)
            << results[i].timeMs
            << results[i].memoryKb << '\n';
    }

    writeGnuplotScript("time_plot.gp", "Execution Time per Test", "Time (ms)", 4);
    writeGnuplotScript("mem_plot.gp", "Memory Usage per Test", "Memory (kB)", 5);

    runGnuplot("time_plot.gp", "time_plot.png");
    runGnuplot("mem_plot.gp", "mem_plot.png");

    return 0;
}