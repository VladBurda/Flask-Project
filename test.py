class Test:
    def __init__(self, name):
        self.name = name
        self.topic_list = {}

    def print_topics(self):
        for i in self.topic_list:
            print(i, ":", self.topic_list[i])

t1 = Test("Group1")

topics_gr1 = """1. Liczby pierwsze: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
2. Kolory tęczy: czerwony, pomarańczowy, żółty, zielony, niebieski, indygo, fioletowy
3. Planety Układu Słonecznego: Merkury, Wenus, Ziemia, Mars, Jowisz, Saturn, Uran, Neptun
4. Najwyższe góry świata:
Mount Everest (8848 m)
K2 (8611 m)
Kangczendzonga (8586 m)
Lhotse (8516 m)
Makalu (8485 m)
5. Najczęściej używane języki na świecie (liczba użytkowników):
Angielski (~1,5 mld)
Chiński mandaryński (~1,1 mld)
Hindi (~600 mln)
Hiszpański (~500 mln)
Arabski (~400 mln)"""

def autosplitting_topics(group, topics):
    lines = topics.split("\n")
    current_key = None
    current_value = []

    for line in lines:
        parts = line.split(". ", 1)  # Splitting only at first occurrence of ". "
        if len(parts) == 2 and parts[0].isdigit():  
            if current_key is not None:
                group.topic_list[current_key] = "\n".join(current_value)  # Save previous topic
            current_key = int(parts[0])
            current_value = [parts[1]]
        else:
            if current_key is not None:
                current_value.append(line)  # Append multiline content

    if current_key is not None:
        group.topic_list[current_key] = "\n".join(current_value)  # Save last topic

autosplitting_topics(t1, topics_gr1)
#t1.print_topics()
js = t1.topic_list
print(js)
