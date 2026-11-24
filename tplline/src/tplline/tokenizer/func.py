"""Functions for template rendering."""
import random
import time
import string


def random_sequence(pattern):
    """
    Generate a random string replacing all '@' in PATTERN with a random digit (0-9).
    """
    return ''.join(c if c != '@' else str(random.randint(0, 9)) for c in list(pattern))


def random_string(length):
    """
    Returns an uppercase sequence of random letters of LENGTH.
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(int(length)))


def random_date(min_date, max_date, sformat):
    """
    Generate a random date between MIN_DATE and MAX_DATE. The output is formatted
    according SFORMAT. Both MIN_DATE and MAX_DATE must be in the same format as
    the output. For all possible formats reference to https://strftime.org/
    """
    stime = time.mktime(time.strptime(min_date, sformat))
    etime = time.mktime(time.strptime(max_date, sformat))
    ptime = stime + random.random() * (etime - stime)
    return time.strftime(sformat, time.localtime(ptime))


def random_time(sformat):
    """
    Returns a random time (24 hours) formatted as SFORMAT.
    For all possible formats reference to https://strftime.org/
    """
    return time.strftime(sformat, time.localtime(random.random() * (24 * 60 * 60)))


def random_in(*args):
    """
    Returns a random values among arguments.
    """
    return random.choice(args)


def random_number(nmin, nmax):
    """
    Returns a random number between NMIN and NMAX.
    """
    return str(random.randint(int(nmin), int(nmax)))

# ~@:-]
