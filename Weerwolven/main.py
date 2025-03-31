from spel_fabriek import Spel
from save import slaag_op

spel = Spel(False)


def main():
    spel.spel_loop()
    slaag_op("opslaag_tekst.txt",spel)


if __name__ == "__main__":
    main()