from scipy.stats import hypergeom as hg
from math import comb
from itertools import product
import numpy as np
import random
from tqdm import tqdm

def hypergeom(deck_size=60, n_mulligans=2, n_amulet=4,
					 n_untapped=15, n_extra_land=8, n_titan=8,
					 n_bounce=10, n_exclude=2, on_draw=True,
					 turn=2, is_subprocess=False):
	'''
	Uses joint hypergeometric probabilities to calculate the probability
	of winning the game in a given set of conditions while playing
	Amulet Titan. This is calculated as:

	P(win) = 1 - P(no amulet OR no untapped land OR no extra land effect OR no Titan OR no bounce OR drew a combo land)

	NOTE: There is one minor computational error that I am too lazy
	to account for here, namely regarding Summoner's Pact.
	Technically, Pact breaks the "without replacement" clause of
	hypergeometric calculation as it can count for two conditions
	at once (i.e., you could win with Pact for Titan + Pact for Grazer).
	That (and other things I'm forgetting to model) means the final
	probability you are given of a win on a given turn are likely
	slightly inflated.

	TO DO:
	* Fix the Summoner's Pact issue
	* Model Green Sun's Zenith (currently unaccounted)
	* Better handling of Saga/TMG on Turn 3 calculations

	Parameters:
	* deck_size : Number of starting cards in library.
	* n_mulligans : Number of mulligans you are willing to take to
					'dig' for the combo. Default is 2 from my own
					heuristics.
	* n_amulet : Number of Amulets of Vigor in the deck. Do NOT
				 include "virtual" amulets like Saga or TMG if
				 trying to calculate a Turn 2 kill.
				 (Also adjust n_untapped accordingly!)
	* n_untapped : Number of untapped mana sources in deck that
				   are capable of casting an Amulet of Vigor on
				   Turn 1 (so, they don't have to be green.)
				   NOTE: Urza's Saga and The Mycosynth Gardens
				   must be counted as EITHER a land OR an Amulet,
				   so don't "double dip" when setting the values
				   for n_amulet and n_untapped!
	* n_extra_land : Number of "extra land drop" effects that can net
					 4+ mana with double Amulet and a bounce land.
					 In practice, this means Grazer, Explore, or Azusa.
					 Notably, Dryad does NOT count (only nets 3 mana).
					 Count Summoner's Pacts in this number.
	* n_titan : Number of Primeval Titans in deck, counting Pacts.
	* n_bounce : Number of lands that produce at least 4 mana
				 (two of which at least being green mana) if
				 you have two Amulets in play. So, Lotus Field
				 would count, but Crumbling Vestige would not.
				 Do NOT count Vesuva here.
	* n_exclude : Cards that if you draw them to hand, they break
				  the combo line. Default is 2, representing:
				  Hanweir Battlements, (can't haste)
				  Mirrorpool (can't copy Titan)
				  It's possible this number should be larger but
				  I'm too lazy to think deeply about it right now.
	* on_draw : boolean for tracking whether or not you are on the
				draw; i.e., you see an extra card.
	* turn : Which of your turns you would like to calculate probability for.
	* is_subprocess : Leave this as False, it's a bool flag for doing
					  mulligan calculations
	'''
	draw_size = 7 + (turn - 1) + (1 if on_draw else 0)

	# Calculate base failure probabilities
	p_no_amulet = hg.pmf(0, deck_size, n_amulet, draw_size)
	p_no_untapped = hg.pmf(0, deck_size, n_untapped, draw_size)
	p_no_extra_land = hg.pmf(0, deck_size, n_extra_land, draw_size)
	p_no_titan = hg.pmf(0, deck_size, n_titan, draw_size)
	p_no_bounce = hg.pmf(0, deck_size, n_bounce, draw_size)

	# Probability of drawing a combo land
	p_bad_card = 1 - hg.pmf(0, deck_size, n_exclude, draw_size)
	
	# Generate all combinations of "failure" events from base probabilities
	fail_events = ['amulet', 'untapped', 'extra_land', 'titan', 'bounce', 'bad_card']
	fail_probs = [p_no_amulet, p_no_untapped, p_no_extra_land,
				  p_no_titan, p_no_bounce, p_bad_card]

	total_fail_prob = 0 # Initialize for loop

	# Loop over all non-empty subsets of fail events
	for bits in product([0, 1], repeat=len(fail_events)):
		if sum(bits) == 0:
			continue
		indices = [i for i, bit in enumerate(bits) if bit]
		prob = 1
		for i in indices:
			prob *= fail_probs[i]
		# inclusion-exclusion sign: add for odd-size subsets, subtract for even
		if len(indices) % 2 == 1:
			total_fail_prob += prob
		else:
			total_fail_prob -= prob

	# Probability of success is 1 - probability of any failure
	p_success = 1 - total_fail_prob

	# Factor in mulligans
	if n_mulligans > 0 and not is_subprocess:
		return mulligans(deck_size, n_mulligans, n_amulet, n_untapped, n_extra_land,
						 n_titan, n_bounce, n_exclude, on_draw, turn)
	else:
		return p_success

def monte_carlo(nperm=10000, deck_size=60, n_mulligans=2, n_amulet=4,
				n_untapped=15, n_extra_land=8, n_titan=8,
				n_bounce=10, n_exclude=2, on_draw=True,
				turn=2):
	'''
	Simulates a Monte Carlo distribution to calculate kill probability
	(as opposed to using a hypergeometric function).

	Parameters are basically the same as hypergeom(), except for:
		* nperm : How many times to run the simulation
	'''
	# Create "decklist"
	deck = (
		['Amulet']*n_amulet + ['Untapped land']*n_untapped +
		['Extra land effect']*n_extra_land + ['Titan']*n_titan +
		['Bounce land']*n_bounce + ['Combo lands (BAD)']*n_exclude +
		['Other'] * (deck_size - n_amulet - n_untapped - n_extra_land -
					 n_titan - n_bounce - n_exclude)
	)

	best_successes = 0 # init
	pbar = tqdm(np.arange(nperm))
	pbar.set_description("Permuting opening hands...")
	for _ in pbar:
		best_this_trial = 0

		for m in np.arange(n_mulligans):
			draw = 7 + (turn - 1) + (1 if on_draw else 0)
			hand = random.sample(deck, draw)
			has_amulet = 'Amulet' in hand
			has_untapped = 'Untapped land' in hand
			has_extra = 'Extra land effect' in hand
			has_titan = 'Titan' in hand
			has_bounce = 'Bounce land' in hand
			has_bad = 'Combo lands (BAD)' in hand
			if has_amulet and has_untapped and has_extra and has_titan and has_bounce and not has_bad:
				best_this_trial += 1
				break # don't need to keep mulliganing if we find a kill

		best_successes += best_this_trial

	return best_successes / nperm

def mulligans(deck_size, n_mulligans, n_amulet, n_untapped, n_extra_land,
	n_titan, n_bounce, n_exclude, on_draw, turn):
	'''
	Internal helper function to avoid recursion errors – DO NOT CALL THIS
	'''
	is_subprocess = True
	p_success = []
	for i in np.arange(n_mulligans):
		p_success.append(hypergeom(deck_size, n_mulligans, n_amulet, n_untapped, n_extra_land,
									n_titan, n_bounce, n_exclude, on_draw, turn, is_subprocess))
	return max(p_success)