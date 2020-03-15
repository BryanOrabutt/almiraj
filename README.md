# Almiraj

## Directory structure

* src contains afl-unicorn, openOCD.py (for JTAG), helper scripts for emulation, unicorn engine, openocd tcl scripts for BBB and XDS110 JTAG emulator
* BBB contains the beaglebone black freeRTOS port as well as TI starterware libraries for bare metal code
* src/fuzz_testing contains the python test harness for fuzzing binaries with afl-unicorn. as well as helper scripts for fuzzing
* openocd contains a TI fork of openOCD with support for the XDS110 jtag emulator
* src/unicorn_testing contains python code to emulate binaries in unicorn without fuzzing

## Files created:

The files we created are listed below. A \* after the directory indicates all files were made by us.

* src/helper_scripts/\*
* src/openocd_scripts/openOCD.py
* src/openocd_scripts/runit.sh
* BBB/main.c
* src/fuzz_testing/run_fuzz
* src/fuzz_testing/get_files

## Files modifed:

Files created by others but modified by us are listed below. A \* after a directory indicates all files were modified by us

* src/openocd_scripts/bbb.cfg
* src/fuzz_testing/test_harness.py
* src/unicorn_testing/freertos_emu.py
* BBB/makedefs_ti
* BBB/makefile
* BBB/include/rtos/FreeRTOSConfig.h

---
Project by [Bryan Orabutt](https://github.com/BryanOrabutt) and [Zach Heller](https://github.com/zacheller/)
