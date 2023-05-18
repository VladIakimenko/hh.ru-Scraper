## Concept
Scrapes hh.ru for vacancies in St. Petersburg and Moscow. The results can be filtered by a key word. Interaction with user is realized in a simple console dialogue. The search results is saved to a json file for further use.

## Modes
The app operates in 2 modes: 
1. A direct request to hh.ru with 'requests' library. The hh.ru policy restricts the output in such cases with 20 items only. Might be usefull for a quick update overview.
2. A selenium session that paginates through all the vacancies available and saves numerous results (around 2000 before filtering).
NOTE: Seems to be effected with a non-obvious anti-robots defence. Might require to manually refresh the browser at the 3rd or 4th page. Then it goes through the rest of the pages up to the end successfully.

## PS
This is a raw code snippet for personal use, which has never been optiized to be user-friendly or well balanced. It has never intented to be a stand-alone functional app. Might be used as a time saving template for hh.ru scrapers.
