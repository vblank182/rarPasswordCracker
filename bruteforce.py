import rarfile,zipfile
import datetime, time
from threading import Thread
import optparse
import itertools

rarfile.UNRAR_TOOL="unrar"

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, maxlength + 1)))
def extractFile(arFile, attempt):
    try:
        arFile.extractall(pwd=attempt)
        print (f"Password found! Password is {attempt}")
        return True
    except Exception as e:
        pass
    if datetime.datetime.now().microsecond % 100 == 0:
        print (f"Attempting {attempt}...")
        return False

def main():
    start_time = time.time()
    
    parser = optparse.OptionParser("usage%prog --fr <rarfile> -c <charset> -n <size>")
    parser.add_option('--fr', dest='rname', type='string', help='specify rar file')
    parser.add_option('--fz', dest='zname', type='string', help='specify zip file')
    parser.add_option('-c', dest='charset', type='string', help='specify charset')
    parser.add_option('-n', dest='size', type='string', help='size of password')
    (options, args) = parser.parse_args()
    if (options.rname == None and options.zname == None) or (options.charset == None) or (options.size == None):
        print (parser.usage)
        exit(0)
    else:
        if options.rname:
            arname = options.rname
            arFile = rarfile.RarFile(arname)
        else:
            arname = options.zname
            arFile = zipfile.ZipFile(arname)
        charset = options.charset
        size = options.size

    size = int(size)
    for attempt in bruteforce(charset, size):
        # match it against your password, or whatever
        done = extractFile(arFile,attempt)
        if done: break

        # uncomment below lines if you want to use multiple threads
        # t = Thread(target=extractFile, args=(arFile,attempt))
        # t.start()
        
    end_time = time.time()
    print (f"Ran in {round(end_time - start_time, 2)} seconds.")
    
    exit(0)

if __name__=='__main__':
    main()
    
