
hand = int(raw_input("""Lands in hand?
> """))
field = int(raw_input("""Lands in play?
> """))
gy = int(raw_input("""Lands in graveyard?
> """))
scry_nonland = int(raw_input("""Nonland cards scried to bottom this turn?
> """))
scry_land = int(raw_input("""Lands scried to bottom this turn?
> """))
deck = int(raw_input("""Cards in deck?
> """))
lands_run = int(raw_input("""How many lands does your deck run?
> """))

deck -= scry_nonland
lands_in_deck = lands_run - gy - hand - field - scry_land

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
