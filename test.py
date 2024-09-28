import numpy as np
def parse_input(tables):
    """Parse the input markdown tables into structured data."""
    lab_data = []
    for table in tables:
        rows = table.strip().split("\n")[2:]  # Skip headers
        lab_info = []
        for row in rows:
            cells = row.split("|")[1:-1]  # Remove leading and trailing pipes
            lab_info.append({
                "lab": int(cells[0].strip()),
                "cell_counts": [int(i) for i in (cells[1].strip().split(" "))],
                "increment": cells[2].strip(),
                "condition": list(map(int, cells[3].strip().split()))
            })
        lab_data.append(lab_info)
    return lab_data


def evaluate_increment(increments,cell_counts):
    """Evaluate the increment expressions on the list of cell counts."""
    op = increments.split(" ")
    cell_counts = np.array(cell_counts)
    
    if op[1] == "+":
        if op[2] == "count":
            result = (cell_counts + cell_counts)
        else:
            result = (cell_counts + int(op[2]))
    else:
        if op[2] == "count":
            result = (cell_counts * cell_counts)
        else:
            result = (cell_counts * int(op[2]))
    

    return result.astype('float128').tolist()


def simulate_labs(lab_data):
    """Simulate the lab work for 10,000 days and return the analysis counts."""
    days = {i * 1000: [0] * 8 for i in range(1, 11)}  # Track counts for 10,000 days
    current_counts = {i: lab_data[i]["cell_counts"] for i in range(8)}  # Keep track of current counts in each lab

    for day in range(10):
        for lab_idx in range(8):

            dish = lab_data[lab_idx]
            cell_count = evaluate_increment(dish["increment"], dish["cell_counts"])

            condition, pass_if_true, pass_if_false = dish["condition"]

            for i in range(len(cell_count)):
                if (cell_count[i] % condition) == 0:
                    current_counts[pass_if_true].append(cell_count[i])
                else:
                    current_counts[pass_if_false].append(cell_count[i])

            # Increment the count for the current lab

            sum = len(current_counts[lab_idx])

            days[int(int(day / 1000) + 1) * 1000][lab_idx]  += sum
            current_counts[lab_idx] = []
            for i in range(8):
                lab_data[i]["cell_counts"]=current_counts[i]
            print(lab_data)

    return days


data = "|Lab | Cell counts             | Increment     | Condition |\n|----|-------------------------|---------------|-----------|\n|0   | 98 89 52                | count * 2     | 5  6 1    |\n|1   | 57 95 80 92 57 78       | count * 13    | 2  2 6    |\n|2   | 82 74 97 75 51 92 83    | count + 5     | 19 7 5    |\n|3   | 97 88 51 68 68 76       | count + 6     | 7  0 4    |\n|4   | 63                      | count + 1     | 17 0 1    |\n|5   | 94 91 51 63             | count + 4     | 13 4 3    |\n|6   | 61 54 94 71 74 68 98 83 | count + 2     | 3  2 7    |\n|7   | 90 56                   | count * count | 11 3 5    |"
res = parse_input([data])

print(res)
result = simulate_labs(res[0])
print(result)