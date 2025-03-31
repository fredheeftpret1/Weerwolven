from handige_functies import krijg_teksten, print_story_confirmation, print_story, print_story_pick_from_list
import random
from time import sleep
from spel_fabriek import bepaal_waarde


def voer_dorpeling_uit():
    # Haal de lijst "DORPELING" op
    dorpelingen_teksten = krijg_teksten().get("DORPELING", [])

    # Kies een willekeurige droom
    droom_index = random.randint(0, len(dorpelingen_teksten) - 1)

    # Vertel de situatie en vraag naar bevestiging voor het vervolg
    bevestiging = print_story_confirmation(dorpelingen_teksten[droom_index]["situatie"], len(dorpelingen_teksten[droom_index]["vervolg"]))

    # Vertel het vervolg aan de hand van de bevestiging
    print_story_confirmation(dorpelingen_teksten[droom_index]["vervolg"][str(bevestiging)], 1)

    # Vertel de eindzin
    print_story(dorpelingen_teksten[droom_index]["afsluittekst"])

    input("Druk op ENTER om je beurt te beëindigen >>")


def voer_weerwolf_uit(player, spel, volgorde):
    # Haal de lijst "WEERWOLVEN" op
    weerwolven_teksten = krijg_teksten().get("WEERWOLF", [])

    # Kies een willekeurige variatie
    variatie_index = random.randint(0, len(weerwolven_teksten) - 1)

    # Vertel de bekendmaking en vraag naar bevestiging voor het vervolg
    bekendmaking = weerwolven_teksten[variatie_index]["bekendmaking"]
    bekendmaking = bekendmaking.replace("(WOLF BEKENDMAKING PLACEHOLDER)", wolven_bekendmaking(player,spel))
    print_story_confirmation(bekendmaking, 1)

    # Vertel het uitkiezen en vraag naar bevestiging wie te doden
    uitkiezen = weerwolven_teksten[variatie_index]["uitkiezen"]
    uitkiezen = uitkiezen.replace("(WOLF KEUZE PLACEHOLDER)", wolven_keuze(spel))
    opties = wolven_opties(spel)
    uitkiezen = uitkiezen.replace("(WOLF OPTIES PLACEHOLDER)", opties_namen_uit_lijst(opties))
    keuze = print_story_confirmation(uitkiezen, len(opties)) - 1 # -1 omdat de eerste in de lijst 0 is en de input gaat dan 1 zijn
    keuze_waarde = bepaal_waarde("Weerwolf", volgorde, spel)
    for i in range(keuze_waarde): # Voeg de keuze de waarde aantal keer toe aan de lijst
        spel.weerwolf_keuzes.append(opties[keuze])
    # Vertel de eindzin
    eindzin = weerwolven_teksten[variatie_index]["afsluittekst"]
    eindzin = eindzin.replace("(WOLF KEUZE)", opties[keuze].naam)
    print_story(eindzin)

    input("Druk op ENTER in om je beurt te beëindigen >>")

def wolven_bekendmaking(player, spel):
    andere_weerwolven = lijst_andere_van_rol("Weerwolf",player, spel)
    namen = [obj.naam for obj in andere_weerwolven]  # Haal de naam uit elke weerwolf

    match len(andere_weerwolven):
        case 0: bekendmaking = "Jij bent de enige weerwolf!"

        case 1: bekendmaking = f"{namen[0]} is ook een weerwolf!"

        case _: bekendmaking = f"{', '.join(namen[:-1])} en {namen[-1]} zijn ook weerwolven!"

    return bekendmaking

def wolven_keuze(spel):
    namen = [obj.naam for obj in spel.weerwolf_keuzes]  # Haal de naam uit elke weerwolf keuze

    match len(spel.weerwolf_keuzes):
        case 0:
            keuze_tekst = "Er is nog niemand aangeduid om op te eten"

        case 1:
            keuze_tekst = f"{namen[0]} is al gekozen als mogelijk prooi!"

        case _:
            keuze_tekst = f"{', '.join(namen[:-1])} en {namen[-1]} zijn al gekozen als mogelijke prooien!"

    return keuze_tekst

def wolven_opties(spel):
    return lijst_andere_behalve_rol("Weerwolf", spel)

def voer_dokter_uit(speler, spel, volgorde):
    # Haal de lijst "DOKTER" op
    dokter_teksten = krijg_teksten().get("DOKTER", [])

    # Kies een willekeurige variatie
    variatie_index = random.randint(0, len(dokter_teksten) - 1)

    # Vertel de bekendmaking en vraag naar bevestiging voor het vervolg
    bekendmaking = dokter_teksten[variatie_index]["bekendmaking"]
    bekendmaking = bekendmaking.replace("(DOKTER BEKENDMAKING PLACEHOLDER)", dokter_bekendmaking(speler,spel))
    print_story_confirmation(bekendmaking, 1)

    # Vertel het uitkiezen en vraag naar bevestiging wie te redden
    uitkiezen = dokter_teksten[variatie_index]["uitkiezen"]
    uitkiezen = uitkiezen.replace("(DOKTER KEUZE PLACEHOLDER)", dokter_keuze(spel))
    opties = lijst_andere_behalve_jezelf(speler, spel)
    uitkiezen = uitkiezen.replace("(DOKTER OPTIES PLACEHOLDER)", opties_namen_uit_lijst(opties))
    keuze = print_story_confirmation(uitkiezen, len(opties)) - 1 # -1 omdat de eerste in de lijst 0 is en de input gaat dan 1 zijn
    stem_waarde = bepaal_waarde("Dokter", volgorde, spel)
    for i in range(stem_waarde): # Voeg de keuze de stem waarde aantal keer toe aan de lijst
        spel.dokter_keuzes.append(opties[keuze])
    # Vertel de eindzin
    eindzin = dokter_teksten[variatie_index]["afsluittekst"]
    eindzin = eindzin.replace("(DOKTER KEUZE)", opties[keuze].naam)
    print_story(eindzin)

    input("Druk op ENTER in om je beurt te beëindigen >>")

def dokter_bekendmaking(speler, spel):
    andere_dokters = lijst_andere_van_rol("Dokter",speler, spel)
    namen = [obj.naam for obj in andere_dokters]  # Haal de naam uit elke dokter

    match len(andere_dokters):
        case 0: bekendmaking = "Jij bent de enige dokter!"

        case 1: bekendmaking = f"{namen[0]} is ook een dokter!"

        case _: bekendmaking = f"{', '.join(namen[:-1])} en {namen[-1]} zijn ook dokters!"

    return bekendmaking

def dokter_keuze(spel):
    namen = [obj.naam for obj in spel.dokter_keuzes]  # Haal de naam uit elke dokter keuze

    match len(spel.dokter_keuzes):
        case 0:
            keuze_tekst = "Er is nog niemand aangeduid om te genezen"

        case 1:
            keuze_tekst = f"{namen[0]} is al gekozen als mogelijk patiënt!"

        case _:
            keuze_tekst = f"{', '.join(namen[:-1])} en {namen[-1]} zijn al gekozen als mogelijke patiënten!"

    return keuze_tekst


def voer_politie_uit(speler, spel):
    # Haal de lijst "POLITIE" op
    politie_teksten = krijg_teksten().get("POLITIE", [])

    # Kies een willekeurige variatie
    variatie_index = random.randint(0, len(politie_teksten) - 1)

    # Vertel de bekendmaking en vraag naar bevestiging voor het vervolg
    bekendmaking = politie_teksten[variatie_index]["bekendmaking"]
    print_story_confirmation(bekendmaking, 1)

    # Vertel het uitkiezen en vraag naar bevestiging wie te redden
    uitkiezen = politie_teksten[variatie_index]["uitkiezen"]
    opties = lijst_andere_behalve_jezelf(speler, spel)
    uitkiezen = uitkiezen.replace("(POLITIE OPTIES PLACEHOLDER)", opties_namen_uit_lijst(opties))
    keuze = print_story_confirmation(uitkiezen, len(opties)) - 1

    # Vertel de eindzin
    if opties[keuze].rol == "Weerwolf":
        eindzin = politie_teksten[variatie_index]["afsluittekst weerwolf"]
    else:
        eindzin = politie_teksten[variatie_index]["afsluittekst dorpeling"]

    eindzin = eindzin.replace("(POLITIE KEUZE)", opties[keuze].naam)
    print_story(eindzin)

    input("Druk op ENTER in om je beurt te beëindigen >>")

def lijst_andere_van_rol(rol, actieve_speler, spel):
    lijst = []
    for speler in spel.levende_spelers() :
        if speler.rol == rol and speler != actieve_speler:
            lijst.append(speler)
    return lijst

def lijst_andere_behalve_rol(rol, spel):
    lijst = []
    for speler in spel.levende_spelers():
        if speler.rol != rol:
            lijst.append(speler)
    return lijst

def lijst_andere_behalve_jezelf(speler, spel):
    lijst = spel.levende_spelers()
    lijst.remove(speler)
    return lijst

def opties_namen_uit_lijst(opties):
    namen = [obj.naam for obj in opties]  # Haal de namen op
    opties_namen = "Je kan kiezen uit " + " - ".join(
        f"({i + 1}) {namen[i]}" for i in range(len(namen))
    )

    return opties_namen


class Speler:
    def __init__(self, naam, rol):
        self.naam = naam
        self.rol = rol
        self.beurt_gespeeld = False
        self.is_dood = False

        if naam == "Finn":
            self.developer = True
        else:
            self.developer = False


        print(f"Welkom bij het spel, {self.naam}!")
        sleep(1)


    def voer_rol_uit(self, spel):
        match self.rol:
            case "Dorpeling":
                voer_dorpeling_uit()
            case "Weerwolf":
                voer_weerwolf_uit(self, volgorde=spel.weerwolf_nr, spel=spel)
                spel.weerwolf_nr += 1
            case "Politie":
                voer_politie_uit(self,  spel)
            case "Dokter":
                voer_dokter_uit(self, volgorde=spel.dokter_nr, spel=spel)
                spel.dokter_nr += 1
            case _:
                print("Rol niet herkend")

        self.beurt_gespeeld = True

    def vraag_stem(self, spelers_lijst):
        spelers_lijst.remove(self)

        print_story("Wie denk jij dat de weerwolf is?")
        stem = spelers_lijst[print_story_pick_from_list(spelers_lijst) - 1].naam
        input("Jij hebt gestemd op " + stem + ". Druk op ENTER om door te gaan.")
        return stem
