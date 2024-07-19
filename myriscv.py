# -*- coding: utf-8 -*-
# © 2024 Ulrich Drepper <drepper@akkadia.org>
# This work is licensed via CC BY-NC-SA 4.0
"""The actual CPU simulation implementation."""

from typing import Union


class CPUState:
  """This class contains the state for the simulation."""

  def __init__(self, entry: int, stackaddr: int):
    pass

  def is_ecall(self) -> bool:
    """Return true if the last executed instruction was an ECALL."""
    # TBD
    return False

  def read_register(self, reg: str) -> Union[None, int]:
    """Return the value in the current state of the register named by REG.  The function can
    return None if a non-existing register name is provided."""
    # TBD
    return None

  def __str__(self) -> str:
    return '*** TBD ***'


class MySimulator:
  """This is the actual simulator class."""

  def __init__(self, entry: int, stackaddr: int):
    self.state = CPUState(entry, stackaddr)

  def run(self, n_steps: Union[None, int] = None) -> CPUState:
    """Simulate n_steps instruction.  If n_steps is None do not stop until an exceptions occurs,
    including system calls using the ecall instructions.  Return a reference to the current state
    of the simulation."""
    return self.state

  def step(self) -> CPUState:
    "Simulate one single instruction (single-stepping)."
    return self.run(1)
