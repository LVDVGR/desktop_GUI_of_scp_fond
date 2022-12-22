bad_words = ["delete", "drop", "select", "database", "insert"]
def check_faggots(input_data):
    check_data = input_data.lower()
    for bad_word in bad_words:
        print(bad_word, input_data, '\n')
        if bad_word == check_data:
            return False

    return True

print(check_faggots('select'))

def check_void(input_data):
    if input_data and input_data.strip():
        return True
    else:
        print('empty false')
        return False

def set_better(text):
    total = ''
    first = "'"
    second = ','
    for char in text:
        if char == first:
            total += '\n'
            total += 'deletethis'
        else:
            total += char

    total = total.replace("deletethis,", '')
    total = total.replace("deletethis", '')
    return total







