def count_records(file_path):

    record_counts = {}
    
    with open(file_path, 'r') as file:
        for line in file:            
            line = line.strip()
            
            if line in record_counts:
                record_counts[line] += 1
            else:
                record_counts[line] = 1
    
    return record_counts

file_path = 'data.txt'

record_counts = count_records(file_path)
for record, count in record_counts.items():
    print(f"{record}: {count}")