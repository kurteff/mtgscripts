# Use: python -i aether.py
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
	Aether.py v0.1, by kfshradio
	Press ENTER to continue.

	Commands:
	-storm(): input how many spells you can cast this turn and it outputs how much life you can gain this turn.
	-draw(): tells you probability you will draw a certain card type.
	"""
	)

def storm(count):
	res = int(raw_input("""How many Aetherflux Reservoir do you have in play?
> """))
	life = 0
	ogcount = count
	while count > 0:
		life += count * res
		count -= 1
	print"If you cast %d spells this turn, you'll gain %d life." % (ogcount, life)

def draw():
	hand = int(raw_input("""Lands in hand?
> """))
	field = int(raw_input("""Lands in play?
> """))
	scry_nonland = int(raw_input("""Nonland cards scried to bottom this turn?
> """))
	scry_land = int(raw_input("""Lands scried to bottom this turn?
> """))
	deck = int(raw_input("""Cards in deck?
> """))

	deck -= scry_nonland
	lands_in_deck = 18 - hand - field - scry_land

	land_draw = float(lands_in_deck)/float(deck)
	land_draw *= 100

	print"The probability you draw a land is %r.\n" % land_draw
	
	# scry a land to bottom
	land_draw /= 100
	lands_in_deck -= 1
	new_land_draw = float(lands_in_deck)/float(deck)
	scry_land_draw = new_land_draw - land_draw
	scry_land_draw *= 100
	print"If you scry a land to the bottom right now it will alter your probability of drawing a land by %r.\n" % scry_land_draw

	# scry a nonland to bottom
	lands_in_deck += 1
	deck -= 1
	new_land_draw = float(lands_in_deck)/float(deck)
	scry_land_draw = new_land_draw - land_draw
	scry_land_draw *= 100
	print"If you scry a nonland to the bottom right now it will alter your probability of drawing a land by %r." % scry_land_draw
