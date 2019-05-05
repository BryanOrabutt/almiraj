#!/usr/bin/env python

from __future__ import print_function
from unicorn import *
from unicorn.arm_const import *
from capstone import *

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

#globals
CODE = ""
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

# callback for handling invalid memory access (must be registered with hook_add for apropriate usage)
def hook_invalid(mu, access, address, size, value, user_data):
        print("Invalid memory access at 0x%x..." %(address));
        mu.mem_map(address, 1024)  

        return True

# callback for tracing instructions (must be registered with hook_add for apropriate usage)
def hook_code(uc, address, size, user_data):
    global CODE
    print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" %(address, size))
    # read this instruction code from memory
    print(">>> Instruction code at [0x%x] =" %(address), end="")
    tmp = CODE[address-ADDRESS:address-ADDRESS+size]
    for i in md.disasm(tmp, address):
        print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
        #Maybe more reg_read can be put here...
        reg = mu.reg_read(UC_ARM_REG_R1)  
        print('>>> R1 = 0x%x' %(reg))  

#Memory address where emulation starts
ADDRESS = 0x1000000

try:
        #Init...
        print("[Init]")
        mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        mu.mem_map(ADDRESS, 2 * 1024 * 1024)

        #Open code from file
        file = open("xxx.sc","rb")
        CODE = file.read(80)

        #Write machine code to previously mapped memory
        mu.mem_write(ADDRESS, CODE)

        #Emulation start!
        print("[Emulation]")
        #Add hooks here!
        #One must use the mu.hook_add function, which takes two arguments>
        # - a hook code, type of uc_hook_type (see type definition above!)
        # - a hook function (for example "hook_code")
        #An example for hook_code: "mu.hook_add(UC_HOOK_SOMETHING, hook_something)"
        #...
        mu.hook_add(UC_HOOK_CODE, hook_code)
        mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, hook_invalid)

        mu.emu_start(ADDRESS, ADDRESS + 80)

        print(mu.mem_read(0,40))  

        #Done!
        print("[Done]")

except UcError as e:
        print("ERROR: %s" % e)
