import jionlp

raw = '凤翔街道'

x = jionlp.parse_location(raw, town_village=True)
print(x)

