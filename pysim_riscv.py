#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © 2024 Ulrich Drepper <drepper@akkadia.org>
# This work is licensed via CC BY-NC-SA 4.0
"""Generic bits of the RISC-V simulator which should be usable by all implementations of the
actual simulator functionality."""

from elftools.elf.elffile import ELFFile

from myriscv import MySimulator


class Memory:
  """Implementation of simulated memory.  Allocation is sparse so there should be in theory
  no limit on the address space range.  The user of the class has access to the load and
  store methods which can transfer up to 64kB at once."""
  pagesize = 64 * 1024

  def __init__(self) -> None:
    self.data: dict[int, bytes] = {}

  def load(self, offset: int, size: int) -> bytes:
    """Return SIZE bytes of data from memory at address OFFSET."""
    assert size <= self.pagesize
    page1 = offset // self.pagesize
    page2 = (offset + size - 1) // self.pagesize

    # Note that loads to unallocated memory pages will raise an exception.  That is wanted.
    if page1 == page2:
      return self.data[page1][offset:offset + size]
    return self.data[page1][offset:] + self.data[page2][:size - (self.pagesize - offset % self.pagesize)]

  def store(self, offset: int, data: bytes) -> None:
    """Store the bytes in DATA in memory starting at OFFSET."""
    assert len(data) <= self.pagesize
    page1 = offset // self.pagesize
    page2 = (offset + len(data) - 1) // self.pagesize
    size = len(data)
    if page1 not in self.data:
      self.data[page1] = b'\0' * self.pagesize
    if page1 == page2:
      self.data[page1] = self.data[page1][:offset] + data + self.data[page1][offset + len(data):]
    else:
      self.data[page1] = self.data[page1][:offset] + data[:self.pagesize - offset % self.pagesize]
      if page2 not in self.data:
        self.data[page2] = b'\0' * self.pagesize
      self.data[page2] = data[-size - (self.pagesize - offset % self.pagesize):] + self.data[page2][len(data) - size:]


class Simulator(MySimulator):
  """Simulator class used by the test harness.  It is derived from the actual implementation which
  is supposed to contain the actual implementation.  This class should not have to be changed, it
  only contains the code to set up the simulated memory and then loads to selected executable
  into memory."""
  def __init__(self, execfname: str, stackaddr: int = 64*1024*1024, debug: bool = False):
    with open(execfname, 'rb') as f:
      self.elffile = ELFFile(f)

      # Basic checks for a file RISC-V ELF file.
      if self.elffile.get_machine_arch() != 'RISC-V':
        raise RuntimeError('Not a RISC-V ELF file')
      if self.elffile.header['e_type'] != 'ET_EXEC':
        raise RuntimeError('Not an executable ELF file')
      if not self.elffile.little_endian:
        raise RuntimeError('Not a little-endian ELF file')

      self.debug = debug
      self.xlen = self.elffile.elfclass

      if self.debug:
        print(f'Entry point: {self.elffile.header['e_entry']:#x}')
        print(f'Class      : {self.xlen}')

      self.memory = Memory()

      # Load the program
      for seg in self.elffile.iter_segments():
        if seg.header['p_type'] == 'PT_LOAD':
          if f.seek(seg.header['p_offset']) != seg.header['p_offset']:
            raise RuntimeError('Failed to seek to segment offset')
          data = f.read(seg.header['p_filesz'])
          for i in range(0, len(data), self.memory.pagesize):
            self.memory.store(seg.header['p_paddr'] + i, data[i:i + min(self.memory.pagesize, len(data) - i)])

      # Also allocate the memory for the stack.
      self.memory.store(stackaddr - 1, b'\x00')

    super().__init__(self.elffile.header['e_entry'], stackaddr)


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--debug', help="Enable debug mode", action="store_true")
  parser.add_argument('--stacksize', help="Stack size", type=int, default=64*1024*1024)
  parser.add_argument('executable', type=str, help="Name of the RISC-V ELF executable")

  args = parser.parse_args()

  print(Simulator(args.executable, args.stacksize, debug=args.debug).run())
