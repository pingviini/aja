def parse_instance(path):
    with open(path, 'r') as instance:
        data = instance.readlines()
        start = 0
        end = 0
        eggs_list = []
        for counter, line in enumerate(data):
            if not start:
                if 'sys.path[0:0]' in line:
                    start = counter + 1
            if counter >= start and not end:
                if ']' in line:
                    end = counter

        eggs_list = clean_eggs_list(data[start:end])
        return eggs_list


def clean_eggs_list(eggs_list):
    tmp = []
    for line in eggs_list:
        line = line.lstrip().rstrip()
        line = line.replace('\'', '')
        line = line.replace(',', '')
        tmp.append(line)
    return tmp
