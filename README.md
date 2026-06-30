# Mutation-Based Fuzz Testing Lab

## Overview
This project implements a mutation-based fuzz testing framework to evaluate the robustness of a binary image conversion program. The fuzzer generates modified inputs from a seed image to identify crash-inducing edge cases.

## Objectives
- Design a mutation-based input generation strategy
- Automatically generate test cases from a valid seed input
- Identify crash-inducing inputs in a target program
- Analyze and report vulnerability discovery results

## Approach
The fuzzer applies random and rule-based mutations to a valid JPEG input file to generate new test cases. These mutated inputs are then executed against the target program to observe abnormal behavior such as segmentation faults.

## Key Concepts
- Mutation-based fuzzing
- Input space exploration
- Software robustness testing
- Crash detection and analysis

## Tools Used
- C / C++ or Python (fuzzer implementation)
- Linux (Eustis environment)
- File-based input mutation techniques

## Output
- Mutated test cases triggering program crashes
- Statistical analysis of discovered failure cases
- Report with experimental evaluation and findings

## Note
This project was completed in a controlled academic cybersecurity lab environment focused on software testing and vulnerability analysis.
