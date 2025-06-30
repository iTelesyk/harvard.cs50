from pagerank import *
damping_factor = 0.85

# corpus = {
#     "1.html": {"2.html", "3.html"},
#     "2.html": {"3.html"},
#     "3.html": {"2.html"},
# }
# page = "1.html"

corpus= {'1': {'2'}, '2': {'3', '1'}, '3': {'2', '4'}, '4': {'2'}}
page = "4"

result = transition_model(corpus, page, damping_factor)
print(result)



spr = sample_pagerank(corpus=corpus, damping_factor=damping_factor, n=SAMPLES)
print(spr)
