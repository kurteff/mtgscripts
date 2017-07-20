# Use: python -i storm.py
import os

# Def section ##########
def clear(*args):
	"""Clears the screen and also prints an optional argument as output
	after screen is cleared."""
	os.system('cls' if os.name == 'nt' else 'clear')
	for arg in args:
		print(arg)

# Script ##########
clear("""
	Storm.py v0.1, by kfshradio
	Press ENTER to continue.
	"""
	)

raw_input()

clear("Please input your starting hand:")
cantrips = int(raw_input("""
	Number of two-mana artifacts in your starting hand: 
	> """))
lands = int(raw_input("""
	Lands in starting hand:
	> """))
res = int(raw_input("""
	Number of Aetherflux Reservoirs in your starting hand:
	> """))
out = int(raw_input("""
	Number of Paradoxical Outcomes in your starting hand:
	> """))
dudes = int(raw_input("""
	Number of creatures in your starting hand:
	> """))
ramp = int(raw_input("""
	Number of G ramp spells in your starting hand:
	> """))
crush = int(raw_input("""
	Number of 'Crush of Tentacles' in your starting hand:
	> """))
cheerio = int(raw_input("""
	Number of 0 CMC artifacts in your starting hand:
	> """))
handsize = cantrips + lands + res + out + dudes + ramp + crush + cheerio

# debug, delete for final prog
print("So, there are %d cards in your starting hand, huh?" % handsize)

t1 = raw_input("""
	Are you going first? (y/n)
	> """)

if t1 == "y":
	print("Cool, you're on the play!")
else:
	if t1 == "n":
		print("Cool, you're on the draw!")
	else:
		print("nice typing skills idiot")
