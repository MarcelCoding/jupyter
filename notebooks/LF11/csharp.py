import cmd
import sys
import os
import random
from typing import Type

# DEINS

class ClassA:

  def __init__(self, path: str | None = None, entry_id: int | None = None):
    if path is None or entry_id is None:
      self._id = random.randint(10000, 99999)
      self.field_a = "Feld A"

    else:
      columns = self._read_from_file(path, entry_id)

      if columns is None:
        raise AssertionError("id not in file found")
      else:
        self._from_csv(columns)
        
  @staticmethod
  def _read_from_file(path: str, entry_id: int) -> list[str] | None:
    if os.path.exists(path):
      with open(path, "r", encoding="utf-8") as f:
        line = f.readline()

        while line != "":
          # <id>;<field_a>
          columns = line.split(';')
          current_id = int(columns[0])

          if entry_id == current_id:
            return columns

          line = f.readline()
    return None

  def _from_csv(self, columns: list[str]):
    self._id = int(columns[0])
    self.field_a = columns[1]
    
  def _as_csv(self) -> str:
    return f"{self._id};{self.field_a}"

  def id(self) -> int:
    return self._id

  def fields(self) -> str:
    return f"{self._id}\n{self.field_a}"

  def append_to_file(self, path: str):
    with open(path, 'a') as f:
      line = f"{self._as_csv()}\n"
      f.write(line)

  def remove_from_file(self, path: str):
    with open(path, 'r') as f:
      lines = f.readlines()

    with open(path, 'w') as f:
      for line in lines:
        # <id>;<field_a>
        columns = line.split(';')
        current_id = int(columns[0])

        if current_id is not self._id:
          f.write(line)

          
class ClassB(ClassA):

  def __init__(self, path: str | None = None, entry_id: int | None = None):
    super().__init__(path, entry_id)
    
    if path is None or entry_id is None:
      self.field_b = "Feld B"
          
  def _as_csv(self):
    return f"{super()._as_csv()};{self.field_b}"

  def _from_csv(self, columns: list[str]):
    super()._from_csv(columns)
    self.field_b = columns[2]
    
  def fields(self) -> str:
    return f"{super().fields()}\n{self.field_b}"
  

# Unsers - VEB Coding in BSZET

def read_class(class_type: Type[ClassA]):
  path = input("Enter filepath: ").strip()

  try:
    entry_id = int(input("Enter entry id: ").strip())
  except ValueError:
    print("Gib mir Zahl!")
    return

  if len(path) != 0:
    print(class_type(path, entry_id).fields())
    return

  print("Das kein Pfad du Peta.")

def append_class(class_type: Type[ClassA], **kwargs):
  path = input("Enter filepath: ").strip()

  if len(path) != 0:
    class_instance = class_type()
    for attribute, value in kwargs.items():
      setattr(class_instance, attribute, value)
    class_instance.append_to_file(path)
    return

  print("Das kein Pfad du Peta.")
  

class CsharpShell(cmd.Cmd):
  intro = 'Welcome to the csharp-in-cool shell.   Type help or ? to list commands.\n'
  prompt = '(csharp-in-cool) '

  def do_read_class_a(self, arg) -> bool:
    read_class(ClassA)
    return False

  def do_read_class_b(self, arg) -> bool:
    read_class(ClassB)
    return False
    
  def do_append_class_a(self, arg) -> bool:
    field_a = input("Enter Field A: ")
    append_class(ClassA, field_a=field_a)
    return False

  def do_append_class_b(self, arg) -> bool:
    field_a = input("Enter Field A: ")
    field_b = input("Enter Field B: ")
    append_class(ClassB, field_a=field_a, field_b=field_b)
    return False

  def do_bye(self, arg):
    return True
  

if __name__ == '__main__':
  CsharpShell().cmdloop()