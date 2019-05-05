#!/usr/bin/env python

from __future__ import print_function
from unicorn import *
from unicorn.x86_const import *

#******* Architectures (from unicorn.h) ******************************************************************
# typedef enum uc_arch {
    # UC_ARCH_ARM = 1,    // ARM architecture (including Thumb, Thumb-2)
    # UC_ARCH_ARM64,      // ARM-64, also called AArch64
    # UC_ARCH_MIPS,       // Mips architecture
    # UC_ARCH_X86,        // X86 architecture (including x86 & x86-64)
    # UC_ARCH_PPC,        // PowerPC architecture
    # UC_ARCH_SPARC,      // Sparc architecture
    # UC_ARCH_M68K,       // M68K architecture
    # UC_ARCH_MAX,
# } uc_arch;
#*********************************************************************************************************

#******* Modes (from unicorn.h) **************************************************************************
# typedef enum uc_mode {
    # UC_MODE_LITTLE_ENDIAN = 0,  // little-endian mode (default mode)
    # UC_MODE_ARM = 0,    // 32-bit ARM
    # UC_MODE_16 = 1 << 1,    // 16-bit mode (X86)
    # UC_MODE_32 = 1 << 2,    // 32-bit mode (X86)
    # UC_MODE_64 = 1 << 3,    // 64-bit mode (X86, PPC)
    # UC_MODE_THUMB = 1 << 4, // ARM's Thumb mode, including Thumb-2
    # UC_MODE_MCLASS = 1 << 5,    // ARM's Cortex-M series
    # UC_MODE_V8 = 1 << 6,    // ARMv8 A32 encodings for ARM
    # UC_MODE_MICRO = 1 << 4, // MicroMips mode (MIPS)
    # UC_MODE_MIPS3 = 1 << 5, // Mips III ISA
    # UC_MODE_MIPS32R6 = 1 << 6, // Mips32r6 ISA
    # UC_MODE_V9 = 1 << 4, // SparcV9 mode (Sparc)
    # UC_MODE_QPX = 1 << 4, // Quad Processing eXtensions mode (PPC)
    # UC_MODE_BIG_ENDIAN = 1 << 30,   // big-endian mode
    # UC_MODE_MIPS32 = UC_MODE_32,    // Mips32 ISA (Mips)
    # UC_MODE_MIPS64 = UC_MODE_64,    // Mips64 ISA (Mips)
# } uc_mode;
#*********************************************************************************************************

#Shellcode (the script emulates this)
CODE = "\x48\x41\x81\xF9\xBE\x1F\x00\x00\x75\xF6" # <-- dec eax, inc ecx, cmp ecx 0x1fbe jne 0xF9
#Memory address where emulation starts
ADDRESS = 0x1000000

try:
        print("[Init]")
        #Initialize emulator in X86-32bit mode
        #Uc constructor takes two arguments: architecture and mode - now x86 architecture with 32 bit mode
        mu = Uc(UC_ARCH_X86, UC_MODE_32)

        #Memory mapping
        #ADDRESS is the virtual address where our code will be emulated, second argument is the size of virtual memory chunk
        mu.mem_map(ADDRESS, 4096)

        #Write machine code to previously mapped memory
        mu.mem_write(ADDRESS, CODE)

        #With reg_write we can initialize registers to custom values
        #Enum values for some registers can be viewed below...
        mu.reg_write(UC_X86_REG_ECX, 0x0)
        mu.reg_write(UC_X86_REG_EBX, 0x0)
        mu.reg_write(UC_X86_REG_EAX, 0xDEADDEAD)

        #Start the emulation!
        #Parameters are: address where we start, address where we stop, [additionally] time length of emulation (infinite loops, etc.), [additionally] maximum count of instructions to be emulated
        print("[Emulation]")
        mu.emu_start(ADDRESS, ADDRESS + len(CODE))

        #Write out registers to file (reg_read is the opposite of reg_write)
        eax = mu.reg_read(UC_X86_REG_EAX)
        ebx = mu.reg_read(UC_X86_REG_EBX)
        ecx = mu.reg_read(UC_X86_REG_ECX)
        file = open("1.txt", "w")
        file.write("EAX=" + str(hex(eax)) + "\n")
        print("EAX=" + str(hex(eax)) + "\n")
        file.write("EBX=" + str(hex(ebx)) + "\n")
        print("EBX=" + str(hex(ebx)) + "\n")
        file.write("ECX=" + str(hex(ecx)) + "\n")
        print("ECX=" + str(hex(ecx)) + "\n")
        file.close()

        #Done!
        print("[Done]")

except UcError as e:
        print("ERROR: %s" % e)