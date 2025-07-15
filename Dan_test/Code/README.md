# Muon Detector Data Filter – Perl Script by Dan
**Last updated:** 4 May 2025

This `inOut_v2.pl` `Perl` script filters raw `.data` files from muon detector runs, identifying and extracting events that have been detected by **all four ASEC layers**.

## Overview

The script processes a directory of `.data` files generated during muon detector operations. It outputs a single file containing only the events that were detected across **all four layers**.

## Features

- Two separate scripts for linux/MacOS (`inOut_v2.pl`) and Windows (`inOut_v2_windows.pl`).

## Usage

From the script directory, run:

```bash
perl inOut_v2.pl <../data_directory> <output_file_name>
```

- `<../data_directory>`: Path to the directory containing `.data` files.
- `<output_file_name>`: Name for the filtered output file.

## Example

```bash
perl inOut_v2.pl ../Data filtered_output.data
```

## Notes
- When using Windows - use '\' for paths
- Ensure `Perl` is installed on your system by running:
```bash
perl -v
```
- The input directory must contain valid `.data` files from the detector.
	- **Ensure that you intend to filter *all* `.data` files within the specified directory.**
- The output file will be overwritten if it already exists.
