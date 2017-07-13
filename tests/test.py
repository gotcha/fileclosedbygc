from fileclosedbygc import log
import logging


def main():
    open('anonymous.txt', 'a')
    f = open('variable.txt', 'a')  # NOQA
    t2 = open('explicit_close.txt', 'a')
    t2.close()
    log.debug("end main")


if __name__ == '__main__':

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)

    log.debug("before main")
    main()
    log.debug("after main")
