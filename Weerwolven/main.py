from spel_fabriek import Spel
from save import slaag_op
import speler_fabriek

spel = Spel(False)

def main():
    spel.spel_loop()


if __name__ == "__main__":
    spel.spel_loop()
    slaag_op("save_tekst", spel.spelers_lijst, spel.nacht, spel.einde_spel, speler_fabriek.Speler.verkrijg_spelers())