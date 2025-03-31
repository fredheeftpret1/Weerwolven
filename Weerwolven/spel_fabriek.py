from speler_fabriek import Speler
from handige_functies import clear_console, print_story, krijg_teksten, print_story_confirmation, print_story_pick_from_list
import random
from collections import Counter

# Variabelen
start_rollen = ["Dorpeling", "Weerwolf", "Politie", "Dokter",
         "Dorpeling", "Weerwolf", "Dorpeling", "Dokter",
         "Dorpeling", "Weerwolf", "Dorpeling", "Dokter"]
max_players = 12
min_players = 4

def print_intro():
    with open("intro.txt", "r") as file:
        intro = file.read()
    print(intro)
    input("Zijn jullie klaar om te spelen?")


def bepaal_aantal_spelers():
    print("Met hoeveel wil je spelen?")
    while True:
        try:
            num_of_players = int(input(">> "))
            if min_players <= num_of_players <= max_players:
                return num_of_players  # Geldige invoer, we stoppen de lus
            else:
                print(f"Dit spel is voor {min_players} tot {max_players} spelers.")

        except ValueError:
            print("Voer een getal in.") # Players are not chosen

def bepaal_naam_speler(spelers_lijst):
    """Vraagt de speler om een unieke naam en controleert of deze al bestaat."""
    print("\n")

    while True:
        print("Wat is je naam?")
        naam = input(">>")
        if any(speler.naam == naam for speler in spelers_lijst):
            print(f"Speler {naam} bestaat al.")
        elif naam == "":
            print("Geef een geldige naam in.")
        else:
            return naam


def bepaal_waarde(actieve_rol: str, volgorde, spel):
    """Bepaalt de waarde van een stem voor de weerwolf/dokter"""
    andere_van_rol = 0
    for de_rol in spel.rollen_lijst:
        if de_rol == actieve_rol:
            andere_van_rol += 1
    match andere_van_rol:
        case 1:
            stem_waarde = 1
        case 2:
            match volgorde:
                case 1:
                    stem_waarde = 1
                case 2:
                    stem_waarde = 2
        case 3:
            match volgorde:
                case 1:
                    stem_waarde = 2
                case 2:
                    stem_waarde = 3
                case 3:
                    stem_waarde = 4
    return stem_waarde

def maak_spelers_lijst(spel):
    aantal_spelers = bepaal_aantal_spelers()

    spel.rollen_lijst = start_rollen[:aantal_spelers - 1]
    random.shuffle(spel.rollen_lijst)

    spelers_lijst = []
    for rol in spel.rollen_lijst:
        naam = bepaal_naam_speler(spelers_lijst)
        spelers_lijst.append(Speler(naam, rol))

    return spelers_lijst

def maak_debug_spelers():
    spelers_lijst = []
    spelers_lijst.append(Speler("Finn", "Dorpeling"))
    spelers_lijst.append(Speler("Papa", "Politie"))

    return spelers_lijst


def iedereen_gespeeld(spelers_lijst):
    for speler in spelers_lijst:
        if not speler.beurt_gespeeld:
            return False
    # Als de loop hier geraakt, heeft iedereen gespeeld
    return True


def kies_volgende_speler(spelers_lijst):
    """Kies een willekeurige speler die nog niet heeft gespeeld."""
    niet_gespeeld = [speler for speler in spelers_lijst if not speler.beurt_gespeeld]

    if niet_gespeeld:  # Controleer of er nog spelers over zijn
        return random.choice(niet_gespeeld)

    return None  # Geen spelers meer beschikbaar

def afhandelen_dode_speler(spel):
    dode_speler = wie_gaat_er_dood(spel)
    geredde_speler = wie_wordt_gered(spel)
    if dode_speler == geredde_speler:
        dode_speler = None

    if dode_speler is None:
        print_story(genereer_tekst_wolven_actie(False))
    else:
        actie_tekst = genereer_tekst_wolven_actie(True)
        actie_tekst = actie_tekst.replace("(DODE SPELER)", dode_speler.naam)
        print_story(actie_tekst)
        for speler in spel.spelers_lijst:
            if speler.naam == dode_speler.naam:
                speler.is_dood = True

def genereer_tekst_stemming(stemmen_dict, spel):
    algemene_teksten = krijg_teksten().get("ALGEMEEN", [])
    stemmen_teksten = algemene_teksten.get("stemmen")

    # Kies een willekeurige variatie
    variatie_index = random.randint(0, len(stemmen_teksten) - 1)

    stemming_tekst = "\n".join(f"{key} heeft gestemd op {value}." for key, value in stemmen_dict.items())
    print_story(stemming_tekst)

    resultaten = meeste_stemmen(stemmen_dict)

    if len(resultaten) == 1:
        verliezer = resultaten[0]

        resultaat_tekst = stemmen_teksten[variatie_index].get("unaniem")
        resultaat_tekst = resultaat_tekst.replace("(WEGGESTEMDE SPELER)", verliezer)
        spel.geef_speler_bij_naam(verliezer).is_dood = True
    else:
        resultaat_tekst = stemmen_teksten[variatie_index].get("gelijkstand")
        resultaat_tekst = resultaat_tekst.replace("(GELIJKSTAND SPELERS)", ", ".join(resultaten[:-1]) + " en " + resultaten[-1])

    print_story(resultaat_tekst)

def genereer_tekst_wolven_actie(er_is_een_dode):
    algemene_teksten = krijg_teksten().get("ALGEMEEN", [])
    weerwolf_actie_teksten = algemene_teksten.get("weerwolf_actie")

    # Kies een willekeurige variatie
    variatie_index = random.randint(0, len(weerwolf_actie_teksten) - 1)

    if er_is_een_dode:
        return weerwolf_actie_teksten[variatie_index].get("dode_gevallen")
    else:
        return weerwolf_actie_teksten[variatie_index].get("geen_dode_gevallen")

def genereer_eind_tekst(spel, winnaars):
    algemene_teksten = krijg_teksten().get("ALGEMEEN", [])
    eind_teksten = algemene_teksten.get("einde").get(winnaars)

    # Kies een willekeurige variatie
    overlevenden = []
    variatie_index = random.randint(0, len(eind_teksten) - 1)
    for speler in spel.levende_spelers():
        overlevenden.append(speler.naam)

    eind_tekst = eind_teksten[variatie_index].get("tekst").replace("(OVERLEVENDE PLACEHOLDER)", ", ".join(overlevenden[:-1]) + " en " + overlevenden[-1])
    return eind_tekst


def wie_gaat_er_dood(spel):
    if not spel.weerwolf_keuzes: # If nobody is dead
        return
    counter = Counter(spel.weerwolf_keuzes) # Count the votes
    max_count = max(counter.values()) # Max values
    # Who is most chosen?
    for choice in counter.keys():
        if counter[choice] != max_count:
            del spel.weerwolf_keuzes[spel.weerwolf_keuzes.index(choice)]
            del counter[choice]
    if len(spel.weerwolf_keuzes) == 1:
        return spel.weerwolf_keuzes[0]
    else:
        return spel.weerwolf_keuzes[len(spel.weerwolf_keuzes) - 1]

def wie_wordt_gered(spel):
    # First, check who's saved by doctor
    if len(spel.dokter_keuzes) == 0:
        wordt_gered = None
    elif len(spel.dokter_keuzes) == 1:
        wordt_gered = spel.dokter_keuzes[0]
    else:
        wordt_gered = spel.dokter_keuzes[len(spel.dokter_keuzes) - 1]
    return wordt_gered

def check_einde_spel(spel):
    werewolves_alive = any(obj.rol == "Weerwolf" for obj in spel.levende_spelers())
    villagers_alive = any(obj.rol != "Weerwolf" for obj in spel.levende_spelers())
    if werewolves_alive and villagers_alive:
        if spel.debug: print_story("Er zijn nog weerwolven en dorpsbewoners over.")
        return False

    elif werewolves_alive and not villagers_alive:
        print_story(genereer_eind_tekst(spel, "weerwolven_winnen"))
        return True

    elif not werewolves_alive and villagers_alive:
        print_story(genereer_eind_tekst(spel, "dorpelingen_winnen"))
        return True



def meeste_stemmen(stemmen_dict):
    """Bepaalt wie de meeste stemmen heeft gekregen."""
    if not stemmen_dict:
        return None  # Geen stemmen uitgebracht

    telling = Counter(stemmen_dict.values())  # Tel hoe vaak elke naam voorkomt
    max_stemmen = max(telling.values())  # Bepaal het hoogste aantal stemmen

    # Zoek alle namen die dit aantal stemmen hebben (bij een gelijkspel)
    winnaars = [naam for naam, aantal in telling.items() if aantal == max_stemmen]

    return winnaars


class Spel:
    def __init__(self, debug):
        self.debug = debug

        if not debug: print_intro()
        if not debug: self.spelers_lijst = maak_spelers_lijst(self)
        if debug: self.spelers_lijst = maak_debug_spelers()

        self.einde_spel = False
        self.nacht = 0
        self.weerwolf_keuzes = []
        self.dokter_keuzes = []
        self.dokter_nr = 1
        self.weerwolf_nr = 1


    def reset(self):
        self.weerwolf_keuzes = []
        self.dokter_keuzes = []
        for speler in self.levende_spelers():
            speler.beurt_gespeeld = False

        clear_console()

    def beleef_nacht(self):
        while not iedereen_gespeeld(self.levende_spelers()):
            clear_console()
            actieve_speler = kies_volgende_speler(self.levende_spelers())
            input(actieve_speler.naam + " is aan de beurt. Druk op ENTER in als jij dit bent.")
            actieve_speler.voer_rol_uit(self)
            clear_console()

        input("De nacht is bijna voorbij. Druk op ENTER als jullie allemaal wakker zijn.")
        afhandelen_dode_speler(self)
        input("Druk op ENTER om door te gaan naar de stemming.")

        self.reset()

    def beleef_dag(self):
        stemmen_dict = {}

        while not iedereen_gespeeld(self.levende_spelers()):
            actieve_speler = kies_volgende_speler(self.levende_spelers())
            print_story(actieve_speler.naam + " moet nu gaan stemmen.")
            stemmen_dict[actieve_speler.naam] = actieve_speler.vraag_stem(self.levende_spelers())
            actieve_speler.beurt_gespeeld = True
            clear_console()

        input("Iedereen heeft gestemd. Druk op ENTER voor de resultaten.")
        genereer_tekst_stemming(stemmen_dict, self)

        input("Druk op ENTER om door te gaan naar de volgende nacht.")


        self.reset()


    def debug_parameters(self):
        #self.weerwolf_keuzes.append(self.spelers_lijst[1])
        #self.dokter_keuzes.append(self.spelers_lijst[1])

        for s in self.spelers_lijst:
            if s == self.spelers_lijst[0]:
                pass
            else:
                s.is_dood = True

    def spel_loop(self):
        if self.debug:
            self.debug_parameters()

        while True:
            self.beleef_nacht()
            self.einde_spel = check_einde_spel(self)
            if self.einde_spel:
                break
            self.beleef_dag()
            self.einde_spel = check_einde_spel(self)
            if self.einde_spel:
                break
            self.nacht += 1

    def levende_spelers(self):
        levende_spelers_lijst = [speler for speler in self.spelers_lijst if not speler.is_dood]
        return levende_spelers_lijst

    def geef_speler_bij_naam(self, naam):
        return  next((speler for speler in self.spelers_lijst if speler.naam == naam), None)











