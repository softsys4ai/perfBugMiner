


import os

def _read_file(filename):

    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '').replace('\t', '').replace('\u3000', '')

def save_file(dirname):

    f_train = open('data/issues/issues.train.txt', 'w', encoding='utf-8')
    f_val = open('data/issues/issues.val.txt', 'w', encoding='utf-8')
    for category in os.listdir(dirname):
        cat_dir = os.path.join(dirname, category)
        if not os.path.isdir(cat_dir):
            continue
        files = os.listdir(cat_dir)
        count = 0
        files_length = len(files)
        for cur_file in files:
            count+=1
            filename = os.path.join(cat_dir, cur_file)
            content = _read_file(filename)
            if count<files_length*0.9:
                f_train.write(category + '\t' + content + '\n')
            else:
                f_val.write(category + '\t' + content + '\n')

        print('Finished:', category)

    f_train.close()
    f_val.close()


if __name__ == '__main__':
    save_file('data/issues_raw')
    print(len(open('data/issues/issues.train.txt', 'r', encoding='utf-8').readlines()))
    print(len(open('data/issues/issues.val.txt', 'r', encoding='utf-8').readlines()))
