#Helper Scripts

Here are a collection of useful helper scripts for fuzzing with Almiraj.

##disasm_parser.py

This script is used to take a disassmebly file (produced by objdump) and find the address map for all functions in the program binary. This is *essential* to using Unicorn successfully as every region of the program binary that may be visiting must be mapped into Unicorn's address space.

To use this script do the following:

* Run objdump from your toolchain (e.g. arm-none-eabi-objdump) and redirect to a file. example: `arm-none-eabi-objdump -d appimage.bin > disasm.txt`
* Run the python scrip `./disasm_parser.py disasm.txt`

The program will produce a file called `memmap.json` that *must* be included in the directory containing your Unicorn test harness.
