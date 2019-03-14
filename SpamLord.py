import sys
import os
import re
import pprint
from io import open

patterns1 = [] #contains patterns for %s@%s.[com|edu]
patterns2 = [] #contains patterns for %s@%s.%s.[com|edu]

first_e = '([A-Za-z0-9._]+)\s*@\s*([A-Za-z0-9._]+)\.edu'
patterns1.append(first_e)
second_e = '([A-Za-z0-9._]+)\s*at\\s*([A-Za-z0-9._]+)\s*dt\s*[com|COM]'
patterns1.append(second_e)
third_e = '([A-Za-z0-9._]+)\s*AT\s*([A-Za-z0-9._]+)\s*DOT\s*[edu|com|COM|EDU]'
patterns1.append(third_e)
fourth_e = '([A-Za-z0-9._]+)\s*[<][A-Za-z0-9._]+[>]\s*@\s*([A-Za-z0-9._]+)\.edu'
patterns1.append(fourth_e)
fifth_e = '([A-Za-z0-9._]+)\s*at\s*([A-Za-z0-9._]+)\.EDU'
patterns1.append(fifth_e)
sixth_e = '([A-Za-z0-9._]+)\s*WHERE\s*([A-Za-z0-9._]+)\s*DOM\s*edu'
patterns1.append(sixth_e)
seventh_e = '([A-Za-z0-9-]+)\-*@\-*([A-Za-z0-9-]+)\.\-e-d-u' #captures dlwh@stanford.edu
patterns1.append(seventh_e)
eighth_e = '([A-Za-z0-9._]+)\s*&#[A-Za-z0-9._]+;\s*([A-Za-z0-9._]+)\.edu'
patterns1.append(eighth_e)
ninth_e = '([A-Za-z0-9._]+)\s*\([\s*A-Za-z0-9.&;#_]*["|;}]@([A-Za-z0-9._]+)\.edu'
patterns1.append(ninth_e)
tenth_e = '([A-Za-z0-9._]{2,})\s+at\s+([A-Za-z0-9._]+)\s*dot\s*edu' #captures subh@stanford.edu and vladlen@stanford.edu
patterns1.append(tenth_e)
eleventh_e = 'obfuscate\(\'([A-Za-z0-9]+)\.edu\',\'([A-Za-z0-9]+)\''
patterns1.append(eleventh_e)
twelfth_e = '([A-Za-z0-9._]+)\s*at\s*([A-Za-z0-9._]{2,})\s*dot\s*([A-Za-z0-9._]{2,})\s*dot\s*[com|edu|COM]'
patterns2.append(twelfth_e)
thirteenth_e = '([A-Za-z0-9._]+)\s*at\s*([A-Za-z0-9._]{2,})\s*;\s*([A-Za-z0-9._]{2,})\s*;\s*[com|edu|COM]'
patterns2.append(thirteenth_e)
fourteenth_e = '([A-Za-z0-9._]+)\s*at\s*([A-Za-z0-9_]{2,})\s*([A-Za-z0-9_]{5,})\s*edu' #captures elusive pal@cs.stanford.edu
patterns2.append(fourteenth_e)
fifteenth_e = '([A-Za-z0-9_.-]+)\s*at\s*([A-Za-z0-9]{2,})\.*([A-Za-z0-9_]{5,})\.edu<' #captures elusive lam@cs.stanford.edu
patterns2.append(fifteenth_e)

patterns3 = []

first_p = '([0-9]{3})[- ]([0-9]{3})[- ]([0-9]{4})'
patterns3.append(first_p)
second_p = '(?:[(])([0-9]{3})(?:[)])[ ]*([0-9]{3})-([0-9]{4})' #captures most phone numbers
patterns3.append(second_p)
third_p = '(?:[(])([0-9]{3})(?:[)])([0-9]{3})-([0-9]{4})' #utilizes non-capturing groups... is not necessary
patterns3.append(third_p)
fourth_p = '(?:[+1])([0-9]{3})([0-9]{3})([0-9]{4})' #format +11234567890
patterns3.append(fourth_p)
fifth_p = '(?:[1])([0-9]{3})([0-9]{3})([0-9]{4})' #format 11234567890
patterns3.append(fifth_p)
sixth_p = '(?:[+1])\s([0-9]{3})\s?\-?([0-9]{3})\s?\-?([0-9]{4})' #format +1 then number with optional spaces and dashes
patterns3.append(sixth_p)
#seventh_p = '([0-9]\s[0-9]\s[0-9])\s+([0-9]\s[0-9]\s[0-9])\s+([0-9]\s[0-9]\s[0-9]\s[0-9])' #capturing spaces not necessary
#patterns3.append(seventh_p)



def process_file(name, f):
    """
    TODO
    This function takes in a filename along with the file object (actually
    a StringIO object at submission time) and
    scans its contents against regex patterns. It returns a list of
    (filename, type, value) tuples where type is either an 'e' or a 'p'
    for e-mail or phone, and value is the formatted phone number or e-mail.
    The canonical formats are:
         (name, 'p', '###-###-#####')
         (name, 'e', 'someone@something')
    If the numbers you submit are formatted differently they will not
    match the gold answers

    NOTE: ***don't change this interface***, as it will be called directly by
    the submit script

    NOTE: You shouldn't need to worry about this, but just so you know, the
    'f' parameter below will be of type StringIO at submission time. So, make
    sure you check the StringIO interface if you do anything really tricky,
    though StringIO should support most everything.
    """
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        for p1 in patterns1:
            matches = re.findall(p1, line)
            if ('com' in p1 or 'COM' in p1):
                for m in matches:
                    email = '%s@%s.com' % m
                    res.append((name, 'e', email))
            elif ('-e-d-u' in p1):
                for m in matches:
                    user = m[0].replace('-', '') #takes care of special case where -e-d-u is found and hyphens must be removed from user
                    domain = m[1].replace('-', '') #for case where domain has hyphens throughout
                    email = user+'@'+domain+'.edu'
                    res.append((name, 'e', email))
            elif ('obfuscate' in p1): 
                for m in matches:
                    user = m[1]; #switches user and domain for obfuscate (confused) case... some serious trickery
                    domain = m[0];
                    email = user+'@'+domain+'.edu'
                    res.append((name, 'e', email))
            else:
                for m in matches:
                    email = '%s@%s.edu' % m
                    res.append((name, 'e', email))



        for p2 in patterns2:
            matches = re.findall(p2, line)
            for m in matches:
                email = '%s@%s.%s.edu' % m
                res.append((name, 'e', email))

        for p3 in patterns3:
            matches = re.findall(p3, line)
            for m in matches:
                phone = '%s-%s-%s' % m #simple matching across all phone numbers
                res.append((name, 'p', phone))
            
    return res


def process_dir(data_path):
    """
    You should not need to edit this function, nor should you alter
    its interface as it will be called directly by the submit script
    """
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path, fname)
        f = open(path, 'r', encoding='ISO-8859-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list


def get_gold(gold_path):
    """
    You should not need to edit this function.
    Given a path to a tsv file of gold e-mails and phone numbers
    this function returns a list of tuples of the canonical form:
    (filename, type, value)
    """
    # get gold answers
    gold_list = []
    f_gold = open(gold_path, 'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list


def score(guess_list, gold_list):
    """
    You should not need to edit this function.
    Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives.  Importantly, it
    converts all of the values to lower case before comparing
    """
    guess_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in guess_list
    ]
    gold_list = [
        (fname, _type, value.lower())
        for (fname, _type, value)
        in gold_list
    ]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    # print('Guesses (%d): ' % len(guess_set))
    # pp.pprint(guess_set)
    # print('Gold (%d): ' % len(gold_set))
    # pp.pprint(gold_set)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp), len(fp), len(fn)))


def main(data_path, gold_path):
    """
    You should not need to edit this function.
    It takes in the string path to the data directory and the
    gold file
    """
    guess_list = process_dir(data_path)
    gold_list = get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
