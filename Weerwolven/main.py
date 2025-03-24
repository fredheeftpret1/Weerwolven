from spel_fabriek import Spel

spel = Spel(False)

def main():
    spel.spel_loop()


if __name__ == "__main__":
    spel.spel_loop()

"""if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("error.txt", "a") as file:
            file.write(str(e))
        print("Er is zojuist een nieuw bestand aangemaakt, genaamd error.txt. ",
              "Gelieve dit bestand door te sturen naar finn.rijnhout+weerwolven_error@gmail.com",
              sep="\n")
        print(e)"""