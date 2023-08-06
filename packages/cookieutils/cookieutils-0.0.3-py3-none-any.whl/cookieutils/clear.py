import os
def oscls():
  os.system('cls' if os.name=='nt' else 'clear')

def pcls():
  print("\033[H\033[2J", end="", flush=True)

  