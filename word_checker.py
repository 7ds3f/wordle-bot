import enchant

def read_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.readlines()
        file.close()
        return words

def check_words(file_path, rec, unrec):
    words = read_words(file_path)
    words = [x.strip() for x in words]
    d = enchant.Dict("en_US")
    for word in words:
        if not d.check(word):
            unrec.append(word)
        else:
            rec.append(word)

def write_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(word)
            file.write('\n')
        file.close()

def run_check(file_path):
    unrecognized = []
    recognized = []
    check_words(file_path, recognized, unrecognized)
    print(len(unrecognized), 'unrecognized words in', file_path)
    print(len(recognized), 'recognized words in', file_path)
    write_words(file_path[4:], recognized)


run_check("old_feudle_words.txt")
run_check("old_standard_words.txt")