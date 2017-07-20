## mtgscripts ##

a collection of Magic: The Gathering-related code.

####`aether.py`####
Interactive Python shell for calculating lifegain based on storm count with [Aetherflux Reservoir](http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=417765) in play. Basically a combination of `storm.py` and `flood.py`.

####`storm.py`####
Unfinished hypergeometric calculator for playing an [Aetherflux Reservoir](http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=417765) deck.

####`flood.py`####
A hypergeometric calculator for giving the probability of you drawing a land on your draw step given the relevant factors. Works for any deck.

####`mtgscripts/mm17_R`####
Some data analysis I did in R corresponding with the release of _Modern Masters 2017_ to predict when the best time to buy specific singles would be. Here are some summaries:
![Individual card fluctuation](https://github.com/grtkrtf/mtgscripts/blob/master/mm17_R/ppc.png?raw=true)
![Set-based fluctuation](https://github.com/grtkrtf/mtgscripts/blob/master/mm17_R/ppc_2.png?raw=true)
One interesting finding was that the price of _Eternal Masters_ is continuing to drop. This is most likely because of the delayed reprints that happened in December (it was originally printed in June). Unfortunately, this has yet to happen with _Modern Masters 2017_...
