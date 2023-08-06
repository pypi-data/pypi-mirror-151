import os,pip
import requests as visit
from .hopter import Error_pta
from .headers import headers_water
from .LICENSE import license_print
from rich.console import Console

console = Console()

headers = headers_water()

def systems(order):
  print('\033[96m',end='\r')
  os.system(order)

def runpy(module):
  print('\033[0m',end='\r')
  os.system('python3 '+module)

def python():
  os.system('python3')

def install(modules):
  print('\033[96m',end='\r')
  os.system('python3 -m pip install -U {}'.format(modules))

def uninstall(modules):
  print('\033[96m',end='\r')
  os.system('python3 -m pip uninstall {}'.format(modules))

def all_help():
  with console.status("\033[96mLoading help documentation …"):
    try:
      print('\033[96m'+str(visit.get('https://hostudio123.github.io/HOPYBOX/help',headers=headers).text))
    except:
      Error_pta('GetHelpError','Command','Unable to get help documentation','help')

def license():
  print('\033[96m'+license_print())

def module_help(module):
  print('\033[96m'+str(help(module)))
  
def pip_list():
  print('\033[96mLoading pack list …',end='\r')
  os.system('pip list')

def debug(command):
  try:
    print(eval(command))
  except Exception:
    console.print_exception(show_locals=True)