def build_protocal_mapping() -> {}:
    protocal_mapping = {}
    fd = open('protocal_numbers.csv', 'r')
    for line in fd:
        tokens = line.split("\t")
        if len(tokens) >= 2 :
            protocal_num = tokens[0]
            protocal_name = tokens[1]
            if not protocal_name:
                continue;
            protocal_mapping[protocal_num] = protocal_name.lower()
    fd.close()
    return protocal_mapping


def build_tag_mapping() -> {}:
    tag_mapping = {}
    fd = open('tags.csv', 'r')
    for line in fd:
        tokens = line.split(",")
        if len(tokens) >= 2 :
            port_num = tokens[0]
            protocal_name = tokens[1]
            tag_name = tokens[2].split(" ")[0]
            key = port_num+" "+protocal_name
            tag_mapping[key] = tag_name

    fd.close()
    return tag_mapping

def parse_log(input_log_name, protocal_mapping, tag_mapping): 
    fd = open(input_log_name, 'r')
    tag_counter = {}
    comb_counter = {}
    for line in fd:
        tokens = line.split(" ")
        if len(tokens) >= 8 :
            dstport = tokens[6]
            protocal_num = tokens[7]
            protocal_name = protocal_mapping[protocal_num]
            key = dstport+" "+protocal_name
            if key in tag_mapping:
                tag = tag_mapping[key]
                tag_counter[tag] = tag_counter.get(tag, 0) + 1
                counterKey = dstport+" "+protocal_num
                comb_counter[counterKey] = comb_counter.get(counterKey, 0) + 1
            else:
                tag_counter['Untagged'] = tag_counter.get('Untagged', 0) + 1
    fd.close()
    return tag_counter, comb_counter

def output_result(output_file_name, tag_counter, comb_counter):
    fd = open(output_file_name, 'w')
    fd.write('Tag Counts:\n')
    fd.write('\n')
    fd.write('Tag.             Count\n')
    for key, value in tag_counter.items():
       fd.write(key+' '+str(value)+'\n')

    fd.write('\n')
    fd.write('Port/Protocol Combination Counts:\n')
    fd.write('\n')
    fd.write('Port.   Protocol. Count\n')
    for key, value in comb_counter.items():
        fd.write(key+' '+str(value)+'\n')
    fd.close()

protocal_mapping = build_protocal_mapping()
tag_mapping = build_tag_mapping()
tag_counter, comb_counter = parse_log('input.log',
                                      protocal_mapping,
                                      tag_mapping)
output_result('output.txt', 
              tag_counter,
              comb_counter)
