# SAP-1 Microprocessor Design and Implementation with Assembler

This project demonstrates the design and implementation of a Simple-As-Possible (SAP-1) microprocessor, integrating both hardware and software components for automatic program execution. The project was developed using Logisim for the hardware design and Python for the custom assembler. The SAP-1 microprocessor is capable of executing assembly-level instructions autonomously, using an automatic program loader to load machine code directly into SRAM.

## Project Overview

### Goal

The objective of this project was to design and implement a fully functional SAP-1 microprocessor system. The system integrates hardware and software components into a unified framework, capable of automatic program loading, execution, and output display without manual intervention.

### Scope

The project encompasses the complete design flow of a basic computer system, including:
- **CPU Design and Control Sequencing:** Modules like the general-purpose register, ALU, instruction register, program counter, and control sequencer.
- **RAM Auto-Loading Mechanism:** A debugging-based auto-loader for direct loading of machine code into SRAM.
- **Assembler Software:** A Python-based assembler that converts human-readable assembly code into 10-bit machine code.
- **Unique Feature Extensions:** Additional modules like the barrel shifter and ring rotator for enhanced logical and data manipulation.

The work demonstrates fundamental principles of computer architecture, including instruction compilation, hardware-level execution, and automation.

## System Architecture

### Major Components

The system consists of the following major components, each implemented as individual circuit blocks in Logisim:

- **General Purpose Register (GPR):** Temporarily stores and manipulates data during execution.

- **Arithmetic Logic Unit (ALU):** Performs basic arithmetic and logical operations such as addition and subtraction.
- **Instruction Register (IR):** Holds the current instruction fetched from memory, including opcode and operand.
- **Program Counter (PC):** Keeps track of the address of the next instruction to be executed.
- **6-to-64 Decoder:** Converts a 6-bit binary number to one-hot encoding for memory location selection.
- **Memory (SRAM):** Stores machine code and data for the microprocessor.
- **Ring Counter:** Generates timing signals for the fetch-decode-execute cycle.
- **Control Sequencer:** Manages the flow of data and control signals based on instruction and timing.
- **Barrel Shifter and Ring Rotator:** Performs logical shifts and bitwise rotations on data.
- **RAM Auto-Loader:** Loads machine code directly into SRAM without manual intervention.

### Datapath & Control Path

The datapath and control sequencer manage the flow of data and control signals between the components of the system. The control sequencer synchronizes the operations of the microprocessor, ensuring that instructions are fetched, decoded, and executed in sequence.

### Instruction Set and Encoding

The SAP-1 microprocessor supports a range of instructions, including data manipulation, conditional branching, and bitwise operations. Each instruction is represented by a 10-bit machine code word, consisting of a 4-bit opcode and a 6-bit operand.

### Timing and Micro-Operation Sequence

Each instruction follows a six-phase timing cycle (T0–T5), during which the fetch, decode, and execute operations are performed. The timing sequence ensures that all components operate synchronously.

## Unique Feature Implementation

In addition to the standard SAP-1 architecture, several key enhancements were made:
- **Conditional Flag System:** Flags such as Zero (Z) and Carry (C) are used for conditional branching (e.g., JNZ, JNC).
- **Shift and Rotate Functional Units:** The barrel shifter and ring rotator allow for bitwise operations like logical shifts and rotations.
- **Program Counter Bus Input for JMP Instructions:** This modification allows dynamic target addresses to be loaded from memory.
- **Expanded Bus and Memory Architecture:** The original 8-bit bus was expanded to 10 bits, allowing up to 64 memory locations.

## Software Component – Assembler/Compiler

The assembler is implemented in Python and translates assembly-level code into 10-bit machine code. The assembler ensures that all operands include the correct suffix (binary, decimal, or hexadecimal) and validates the format before encoding the instructions.

### Assembler Design Flow

1. **Tokenization:** The assembler separates each line into instruction and operand tokens.
2. **Opcode Mapping:** Each mnemonic is mapped to its corresponding 4-bit opcode.
3. **Operand Validation:** Operands are checked for suffix, range, and bit-width.
4. **Encoding:** The assembler combines the opcode and operand to form a 10-bit machine code word.
5. **Output Generation:** The machine code is written in v3.0 hexadecimal format for loading into SRAM.

### Sample Input & Output

#### Example Program 1:
This program compares two numbers and uses conditional branching based on the comparison.

- **Input Assembly Code:**
    ```
    LDA 13d
    CMP 14d
    JNZ 6d
    LDI 001h
    HLT
    ```
- **Output Machine Code:**
    ```
    v3.0 hex words addressed
    0: 04d 20e 286 180 001 140
    ```

#### Example Program 2:
This program demonstrates a loop that compares two numbers and adjusts the second number based on the comparison.

- **Input Assembly Code:**
    ```
    LDA 15d
    CMP 14d
    JNZ 4d
    HLT
    ```
- **Output Machine Code:**
    ```
    v3.0 hex words addressed
    0: 04f 20e 284 140 2c9 04e
    ```

#### Example Program 3:
This program demonstrates bitwise shifting and rotating operations on the accumulator.

- **Input Assembly Code:**
    ```
    LDA 9d
    SFT 000001b
    STA 8d
    SFT 000001b
    STA 8d
    RTE 010010b
    STA 8d
    ```
- **Output Machine Code:**
    ```
    v3.0 hex words addressed
    0: 049 301 1c8 301 1c8 352
    ```

### Error Handling

The assembler includes robust error handling for:
- Missing suffixes in operands.
- Invalid numeric formats (binary, decimal, hexadecimal).
- Out-of-range operands.

## Challenges and Debugging

Key challenges faced during the project include:
- **CMP Instruction and Flag Handling:** A dedicated flag register was added to ensure correct flag updates.
- **Program Counter Reliability:** A redesign was implemented to ensure reliable instruction sequencing.
- **Shifter and Rotator Output Stability:** Registers were added to stabilize outputs of the barrel shifter and ring rotator.
- **Assembler Robustness:** The assembler was developed with comprehensive syntax and range checks to ensure reliable operation.

## Demonstration and Repository Links

### Demonstration Video

[![SAP-1 Microprocessor Demonstration](#)](https://youtu.be/mreEUxgNvG8)

*Placeholder for video link. Replace with actual video URL.*

### Project Repository

All project files, including the Logisim design, assembler source code, and documentation, are available on GitHub. Anyone can use the files to rebuild and test the project.

- **GitHub Repository:** [https://github.com/Tahmid-fuad/Control_sequencer](https://github.com/Tahmid-fuad/Control_sequencer)

The repository also contains the full report and sample programs for easy verification.

## Conclusion

This project successfully demonstrates the design of an enhanced SAP-1 microprocessor system, combining both hardware and software to create a fully functional microprocessor. The enhancements, such as conditional flags, bit manipulation units, and expanded memory architecture, transform the SAP-1 into a versatile platform for learning and experimentation in computer architecture.

---

