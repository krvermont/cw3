from funcs import get_data, get_executed_data, get_last_data, get_needed_data

def main():
    count_last_data = 5
    executed_data_empty = True

    data = get_data()
    data = get_executed_data(data, executed_data_empty)
    data = get_last_data(data, count_last_data)
    data = get_needed_data(data)

    for row in data:
        print(row)

if __name__ == "__main__":
    main()