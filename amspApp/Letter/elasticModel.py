





"""

Analyzers are process which extracts indexable terms from text given for indexing.
For example
In the text "i am a dinosaur from modern age" When this is analyzed against "stop word" analyzer only dinosaur, modern and age keywords are stored in the index. Which means if you search for "am", though the word is present in the text you indexed, it wont point to that indexed document.
Similarly snowball is a combination of stopword , lowercase and standard analyzer - https://www.elastic.co/guide/en/elasticsearch/reference/2.4/analysis-snowball-analyzer.html


"""