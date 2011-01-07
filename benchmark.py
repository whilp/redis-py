import logging
import os
import timeit
import redis

db = redis.Redis(host="localhost", port=16379, db=2)

def enable_logging():
    log = logging.getLogger("redis")
    devnull = open(os.devnull, 'w')
    handler = logging.StreamHandler(strm=devnull)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    log.propagate = 1

def disable_logging():
    log = logging.getLogger("redis")
    for handler in log.handlers:
        log.removeHandler(handler)
    log.setLevel(logging.CRITICAL)
    log.propagate = 0

def command():
    db.set("foo", "bar")

def time(func, repeat=3, number=10e4):
    name = func.__name__
    setup = "from __main__ import %s" % name
    timer = timeit.Timer(stmt="%s()" % name, setup=setup)

    seconds = min(timer.repeat(repeat=repeat, number=int(number)))
    perpass = seconds/number
    usec = 10e6 * perpass

    return usec

def run(tests, repeat=3, number=10e4):
    for test in tests:
        name = test.__name__

        yield name, time(test, repeat=repeat, number=number)

def main(argv):
    number = 10e1
    repeat = 3

    enable_logging()
    print "===> with logging"
    for name, result in run(tests, repeat=repeat, number=number):
        print "%20s: %.2f usec/pass" % (name, result)

    disable_logging()
    print "===> without logging"
    for name, result in run(tests, repeat=repeat, number=number):
        print "%20s: %.2f usec/pass" % (name, result)

tests = [command]

if __name__ == "__main__":
    import sys
    try:
        status = main(sys.argv)
    except KeyboardInterrupt:
        status = 0
    sys.exit(status)
