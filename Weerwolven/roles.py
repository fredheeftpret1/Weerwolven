from collections import Counter
from random import randint
from time import sleep


def police():
    print("Hallo politie!")
    sleep(1)
    print("Jij mag van 1 persoon weten of die een weerwolf is.")
    chosen = False
    while not chosen:
        choice = input(">>")
        if player_functionality.bestaat_speler(choice):
            if player_functionality.speler_naam_is_rol(choice, "Weerwolf"):
                print("Dat is een weerwolf.")
            else:
                print("Dat is geen weerwolf.")
            chosen = True
        else:
            print("Die speler bestaat niet, of is al dood.")


def doctor():
    print("Hallo dokter!")
    sleep(1)
    print("Jij mag een iemand kiezen, en deze kan niet worden gedood door een weerwolf deze ronde.")
    chosen = False
    while not chosen:
        choice = input(">>")
        if player_functionality.bestaat_speler(choice):
            main.saved_by_doctor.append(choice)
            chosen = True
        elif player_functionality.speler_naam_is_rol(choice, "Dokter"):
            print("Dat is ook een dokter")
        else:
            print("Die speler bestaat niet, of is al dood.")





def save_saved_person():
    # First, check who's saved by doctor
    if len(main.saved_by_doctor) == 1:
        main.saved_by_doctor = main.saved_by_doctor[0]
    else:
        main.saved_by_doctor = main.saved_by_doctor[len(main.saved_by_doctor) - 1]
    # Then, delete that person from the choices of the werewolves
    for i in range(len(werewolves_choices)):
        if main.werewolves_choices[i] == main.saved_by_doctor:
            del main.werewolves_choices[i]

