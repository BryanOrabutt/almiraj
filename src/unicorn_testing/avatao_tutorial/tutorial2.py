#!/usr/bin/env python

from __future__ import print_function
from unicorn import *
from unicorn.arm_const import *

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
#******* Hook types (from unicorn.h) *********************************************************************
#// All type of hooks for uc_hook_add() API.
#typedef enum uc_hook_type {
#    UC_HOOK_INTR = 1 << 0,   // Hook all interrupt/syscall events
#    UC_HOOK_INSN = 1 << 1,   // Hook a particular instruction
#    UC_HOOK_CODE = 1 << 2,   // Hook a range of code
#    UC_HOOK_BLOCK = 1 << 3,  // Hook basic blocks
#    UC_HOOK_MEM_READ_UNMAPPED = 1 << 4,   // Hook for memory read on unmapped memory
#    UC_HOOK_MEM_WRITE_UNMAPPED = 1 << 5,  // Hook for invalid memory write events
#    UC_HOOK_MEM_FETCH_UNMAPPED = 1 << 6,  // Hook for invalid memory fetch for execution events
#    UC_HOOK_MEM_READ_PROT = 1 << 7,   // Hook for memory read on read-protected memory
#    UC_HOOK_MEM_WRITE_PROT = 1 << 8,  // Hook for memory write on write-protected memory
#    UC_HOOK_MEM_FETCH_PROT = 1 << 9,  // Hook for memory fetch on non-executable memory
#   UC_HOOK_MEM_READ = 1 << 10,   // Hook memory read events.
#    UC_HOOK_MEM_WRITE = 1 << 11,  // Hook memory write events.
#    UC_HOOK_MEM_FETCH = 1 << 12,  // Hook memory fetch for execution events
#} uc_hook_type;
#*********************************************************************************************************

#You can install hooks to special events (list of events can be found above)
#Here are two examples, that you can use...
#
#Example 1 - hook function def for basic hooks (UC_HOOK_CODE, UC_HOOK_BLOCK, etc)
def hook_code(uc, address, size, user_data):
    print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))  
    tmp = uc.mem_read(address, size)  
    print('>>> Instruction code at [0x%x] =' %(address), end='')  
    for i in tmp:  
        print(' %02x' %i, end='')         
    return True
#Example 2 - hook function def for memory access (UC_HOOK_MEM_READ, etc)
def hook_invalid(mu, access, address, size, value, user_data):
    #Write code here
    


    return True
#Other function prototypes can be found in unicorn/unicorn.py...

#Memory address where emulation starts
ADDRESS = 0x1000000

try:
        #Init...
        print("[Init]")
        mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        mu.mem_map(ADDRESS, 1024)

        #Open code from file here
        file = open('xxx.sc', 'rb')
        CODE = file.read()

        #Write machine code to previously mapped memory
        mu.mem_write(ADDRESS, CODE)

        #Emulation start!
        print("[Emulation]")
        #Add hooks here!
        #One must use the mu.hook_add function, which takes two arguments>
        # - a hook code, type of uc_hook_type (see type definition above!)
        # - a hook function (for example "hook_code")
        #An example for hook_code: "mu.hook_add(UC_HOOK_SOMETHING, hook_something)"
        
        mu.hook_add(UC_HOOK_CODE, hook_code)

        mu.emu_start(ADDRESS, ADDRESS + len(CODE))

        #Done!
        print("[Done]")

except UcError as e:
        print("ERROR: %s" % e)