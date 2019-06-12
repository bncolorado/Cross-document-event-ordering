#  Cross document event ordering (lexical baseline)
Scripts for Cross-document event ordering and cross-document event coreference resolution based on semantic information.

A baseline that groups together two event mentions if their heads  (usually verbs, but not always) are the same word or synonyms. It needs NLTK and Wordnet to find semantic relations. 

Updated to Python3. NLTK must be previously installed:

[https://www.nltk.org/install.html](https://www.nltk.org/install.html)

To install WordNet from NLTK data:

		import nltk
		nltk.download('wordnet')

More info: Navarro-Colorado and Saquete (2016) "Cross-document event ordering through temporal, lexical and distributional knowledge" Knowledge-Based Systems, Volume 110, 15 October 2016, Pages 244–254 http://www.sciencedirect.com/science/article/pii/S0950705116302477
