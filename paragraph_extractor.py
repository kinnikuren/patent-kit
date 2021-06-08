import re
import os
#import file_reader

input_string = "[0021-0023, 0025, 0033, 0038-0040, and 0048]"

comma_split = input_string.split(',')
print(comma_split)

para_list = []
for i in comma_split:
    stripped = i.strip()
    #print(stripped)

    if '-' in stripped:
        hyphen_split = stripped.split('-')
        print(hyphen_split)

        start_para = None
        end_para = None
        #for j in hyphen_split:
            
        match_obj = re.search(r'\d+', hyphen_split[0])
        start_para = int(match_obj[0])
        match_obj = re.search(r'\d+', hyphen_split[-1])
        end_para = int(match_obj[0])

        print(start_para)
        print(end_para)
        for j in range(start_para, end_para+1):
            para_list.append(j)
        #print(match_obj[0])
    else:
        match_obj = re.search(r'\d+', stripped)

        para = int(match_obj[0])
        para_list.append(para)

print(para_list)

#print(os.listdir())

with open("zhou.txt", 'r', encoding="ansi") as myfile:
    data = myfile.read()

#print(data)
#text = file_reader.get_string_from_file("zhou.txt")
#print(text)

results = []

for para in para_list:
    regex = '\[\d*' + str(para) + '\].+\n'
    match_obj = re.search(regex, data)
    results.append(match_obj[0])

print('\n'.join(results))