import re
text = "Random <tag>first</tag> some text <tag>second</tag> end"

# (a) greedy → matches everything from first <tag> to last </tag>
greedy = re.search(r'<tag>.*</tag>', text)
print("Greedy:", greedy.group())

# (b) non-greedy → separate matches
parts = re.findall(r'<tag>.*?</tag>', text)
print("Non-greedy:", parts)
