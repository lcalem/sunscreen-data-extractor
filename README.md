# sunscreen-data-extractor

## Motivation
Daily sunscreen use is something I do to reduce the risks of premature photoaging and melanoma. But finding a good sunscreen that meets all my requirements (good UVA and UVB protection, absence of photo-unstable filters, no white cast or excessive shine, good overall formulation, etc) can be a bit daunting. 
This piece of code helps me extract some of these data to pre-filter which sunscreens are suitable candidates for testing.

## How to run

There is a makefile where you can find useful commands:
`make test` launches two basic tests to see if the code is not broken
`make run` launches the tool to extract data from all sunscreens from one website (more to come) and outputs the results in a csv. (sunscreen_results.csv)

