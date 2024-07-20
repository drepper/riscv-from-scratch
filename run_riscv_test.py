#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © 2024 Ulrich Drepper <drepper@akkadia.org>
# This work is licensed via CC BY-NC-SA 4.0
"""Framework to simulate execution of the test from the RISC-V tests repository."""

import argparse
import os
import subprocess
import sys

from pysim_riscv import Simulator
from myriscv import CPUState


def check_success(state: CPUState) -> tuple[bool, int]:
  "Check whether the simulation stopped when the tests finished successfully."
  testnr = state.read_register('gp')
  return state.is_ecall() and state.read_register('a7') == 93 and state.read_register('a0') == 0, testnr


def main():
  "Run the specified test."
  # The default is to assume that directory with the tests is a submodule at the top level of
  # the source repo.
  riscv_tests_dir = os.path.join(os.path.dirname(sys.argv[0]), 'riscv-tests')

  parser = argparse.ArgumentParser()
  parser.add_argument('--riscv-tests', default=riscv_tests_dir)
  parser.add_argument('XLEN', type=int, choices=[32,64])
  parser.add_argument('EXT', choices=['a', 'c', 'd', 'f', 'i', 'm', 'zba', 'zbb', 'zbc', 'zbs', 'zfh'])
  parser.add_argument('test', type=str)

  args = parser.parse_args()

  srcfname = os.path.join(riscv_tests_dir, 'isa', f'rv{args.XLEN}u{args.EXT}', f'{args.test}.S')
  if not os.path.exists(srcfname):
    print(f'Error: {srcfname} does not exist')
    sys.exit(1)

  execdir = 'test-binaries'
  if not os.path.exists(execdir) or not os.path.isdir(execdir):
    try:
      os.mkdir(execdir)
    except FileExistsError:
      print(f'Error: could not create directory \x1b[33m{execdir}\x1b[0m for the test binaries')
      sys.exit(1)

  execfname = os.path.join(execdir, os.path.splitext(os.path.basename(srcfname))[0])

  xlen_args = {
    32: ['-march=rv32g', '-mabi=ilp32'],
    64: ['-march=rv64g', '-mabi=lp64'],
  }

  res = subprocess.run(['riscv64-linux-gnu-gcc', '-nostdlib', f'-I{riscv_tests_dir}/env/p', f'-I{riscv_tests_dir}/isa/macros/scalar', *xlen_args[args.XLEN], srcfname, '-o', execfname], check=False)
  if res.returncode != 0:
    print('Failed to compile test')
    sys.exit(1)

  state = Simulator(execfname).run()


  success, testnr = check_success(state)
  if not success:
    print(f'\nTest {testnr} failed!  The executable is \x1b[48;5;220m\x1b[2m {os.path.realpath(execfname)} \x1b[0m')
    ip = state.read_register('ip')
    subprocess.run(f"riscv64-linux-gnu-objdump -d {execfname} | grep --color -C 5 -E '^[[:space:]]*{ip:x}:[[:space:]].*'", shell=True, check=False)
    sys.exit(1)

  os.unlink(execfname)

  sys.exit(0)


if __name__ == '__main__':
  main()
