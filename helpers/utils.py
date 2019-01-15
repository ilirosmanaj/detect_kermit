from sys import stdout


def print_progress(percent: float):
    # percent float from 0 to 1.
    stdout.write("\r")
    stdout.write("    {:.0f}%".format(percent * 100))
    stdout.flush()
