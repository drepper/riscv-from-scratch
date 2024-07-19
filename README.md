Writing Your First RISC-V Simulator
===================================

Author: Ulrich Drepper <drepper@akkadia.org>
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This repository contains the beginnings of a first RISC-V simulator. It is not complete, it only provides a
starting point.  The existing functionality implements compiling test cases, loading them into the simulated
memory, and passing control to a user-provided **real** simulator.

The task is to write a functional simulation in the class `MySimulator` in the `myriscv.py` file.  A simulation
object based on the class will be created and the `run()` method will be called.  `step()` is available as an
alternative for single-stepping but this method is not used here.

The simulation is of the userspace part of the RISC-V ISA only.  This means that as soon as the program uses the
`ecall` instruction, the simulation can be stopped.  This is the expected behavior for the programs in the
[test suite](https://github.com/riscv/riscv-tests.git).


Preparations
------------

To be able to commit your changes, you need to create a fork of this repository and clone it locally.
Go to the project [repository's page](https://github.com/drepper/riscv-from-scratch) on GitHub and click the "Fork"
button.  Then run locally in a shell in a directory meant for source code:

```bash
git clone --recurse-submodules https://github.com/<your-username>/riscv-from-scratch.git
```

Here `<your-username>` is your GitHub username.  This will create a local copy of the repository and also fetch all
submodules.

We also need the RISC-V toolchain to be installed on our system.  The following command should do that
on a Fedora system:

```bash
sudo dnf install gcc-c++-riscv64-linux-gnu
```


Missing Bits
------------

All the additional code goes into the `myriscv.py` file.  The existing code is just a starting point.  Of course
is everyone allowed to split out the new code into multiple new files.  Just make sure everything loads correctly.

The `CPUState` class has three methods that need to be implemented for the testing framework to assess the result
of the simulation:

-  `get_register(reg)`: Return the value of a register named `reg`.  Note that RISC-V integer registers have multiple
   names.  All should be supported but the framework uses `a0`, `a7`, and `gp`.
-  `is_ecall()`: Return whether the last instruction executed was an `ecall`.  Simulating an `ecall` instruction
   should stop the simulation and the implementation at that point should be able to determine whether `ecall` was
   the last instruction to be executed.
-  `__str__()`: Return a string representation of the CPU state.  This is useful for debugging by using single-stepping
   and looking at the state of the CPU after every instructions.


Usage
-----

The RISC-V ISA test suite cover all the basic instructions is a pretty thorough way.  The tests are further
grouped by the extension of the ISA which introduced them.  The basic tests are in the `i` extension and they
should be implemented and tested first.

  | Name | Description |
  +:----:|:----------- |
  | `i`  | Basic instructions |
  | `m`  | Multiplication and division |
  | `a`  | Atomic instructions |
  | `f`  | Single precision floating point |
  | `d`  | Double precision floating point |
  | `c`  | Compressed instructions |
  | `zba` | Address generation instructions |
  | `zbb` | Basic bit manipulation instructions |
  | `zbc` | Carryless multiplication instructions |
  | `zbs` | Single-bit instructions |
  | `zfh` | Half-precision floating point instructions |

All but the `i` extension is optional.  Additional instructions should perhaps be executed in the order in which they
appear in the table but this is no hard require.  There are some dependencies between extensions (e.g., `d` and `zfh`
depend on the `f` extension) but aside from that, everyone should feel free to approach the problem as they wish.

All the available tests for the implemented extensions should be run to be sure the implementation is actually
correct.  All tests can be run in 32-bit or 64-bit mode.

To run a single test use:

```bash
./run_riscv_test.py 64 i add
```

Once the simulation finishes the current state of the CPU will be investigated to determine whether the test passed or
failed.


Getting Started
---------------

How to get started you ask?

A good starting point is the Wikipedia page on [Instruction cycle](https://en.wikipedia.org/wiki/Instruction_cycle).
It explains the basic loop of a simple CPU implementation.  Most CPUs today in principal follow this pattern but
in a lot more complex and convoluted and parallel way.

Next, it is necessary to know about the basics of the RISC-V instruction set.  Volume 1 of the [RISC-V Instruction Set Manual](https://riscv.org/specifications/) is revelent here.  We do not deal (yet) with the system programming, so
volume 2 can be ignored for now.

After reading chapter 1 it is, as explained above, best to start with implementing and testing the `i` extension
explained in chapter 2.  The 64-bit variant is explained in chapter 7.  It might be good to implement the `i`
extension for both sizes first before moving on to the other extensions.  The reason is that this gives an
opportunity to learn how to unify the implementation for these width.  Reading the code in `pysim_riscv.py` you
can see that the `Simulation` object has a member called `xlen` which is the common name used throughout the ISA
manual to differentiate between 32-bit and 64-bit variants.  Use this member variable instead of any hardcoded
values in your code.

The `c` extension introduces a new dimension.  It allows to compress (hence `c` extension) the binary code by
encoding often-used instructions with just 16 bits.  This introduces complexities in that instructions now are
no longer guaranteed to be aligned to 32-bit addresses.  Not that much of a problem in this pure Python
implementation but it is complicating in the an efficient implementation using a hardware description language
like Verilog or VHDL (or even higher-level languages like Chisel or NMigen).


Programming Style
-----------------

The existing code uses code annotations.  They do nothing at execution time but static analyzers, including
those that are implicitly run by IDEs like VsCodium, can use the information and provide immediate feedback.
It is highly recommended to continue following this practice.

Additionally the style can be checked with

```bash
pylint --rcfile pylint.conf run_riscv_test.py
```

and similarly for the other Python files.  The selected style is biased and everyone should feel free to
adjust it as wanted.


What Comes Next?
----------------

Implementing this simulator gives a good understanding of the RISC-V ISA and it also introduces you to the
principles of instruction execution.  This can then be used to implement the same CPU using an HDL or perhaps,
to lessen the lift, in NMigen which is also Python-based.  A NMigen design can be run on a FPGA and could
theoretically even be synthesized into ASICs.

Another direction would be to implement a simple compiler that generates RISC-V code from a high-level language.
This will then allow to see the entire step from highlevel programming languages to the signals inside the
CPU when executing the instructions.  This can then lead to thinking about and implementing optimizations in
both the generated code and the CPU implementation itself.


In Case Of Bugs
---------------

File bugs/issues on [GitHub](https://github.com/drepper/riscv-from-scrath/issues).
