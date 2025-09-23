import random
import os
## Wisielec

slownik = []


with open("C:\\Users\\ASUS ZENBOOK\\Desktop\\python\\slownik.txt", 'r') as plik:
    for line in plik:
        clear = line.strip()
        if clear not in slownik:
            slownik.append(clear)

def losowanie_slowa():
    liczba = random.randint(0,len(slownik) - 1)
    losowe_slowo = slownik[liczba]
    return losowe_slowo

def szyfrowanie(losowe_slowo):
    return ['_'] * len(losowe_slowo)
      
def odszyfrowanie_litery(losowe_slowo, zaszyfrowane, litera):
    for i in range(len(losowe_slowo)):
        if losowe_slowo[i] == litera:
            zaszyfrowane[i] = litera
    return zaszyfrowane

def zagdywanie(losowe_slowo):
    życia = 10
    alfabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z']
    zaszyfrowane = szyfrowanie(losowe_slowo)
    while życia > 0 and "_" in zaszyfrowane:
        print("\nZgadywane słowo : ", " ".join(zaszyfrowane))
        print(f"Liczba twoich żyć to {życia}")
        print(f"Oto dostępne litery {alfabet}")
        podana_litera = input("Podaj literę : ").lower()

        if podana_litera in losowe_slowo:
            odszyfrowanie_litery(losowe_slowo, zaszyfrowane, podana_litera)
            print("\n Dobrze! zgaduj dalej \n")
            print("==============================================================================")

        elif podana_litera not in losowe_slowo:
            życia -= 1
            
            print("\n Podana litera nie znajudje sie w haśle, tracisz życie \n ")
            print("==============================================================================")
        
        if podana_litera in alfabet:
            alfabet.remove(podana_litera)

    if "_" not in zaszyfrowane:
        print("Gratulacje ! odgadłeś słowo", losowe_slowo)
    else:
        print("Koniec gry! Nie udało się odgadnąć słowa:", losowe_slowo)



def komunikat_powitanie():
    
    slowo = losowanie_slowa()
    print("################### WISIELEC #########################")
    print("Musisz odgadnąć słowo: ")
    szyfrowanie(slowo)
    print(" " * 10)
    print("Masz 3 życia, za każdą błędną literę stracisz jedno!")
    start = input("Zaczynamy ?? tak/nie >>>>>").lower()

    if start == 'tak':
        zagdywanie(slowo)
    else:
        print("Do zobaczenia")

if __name__ == "__main__":
    os.system('cls')
    komunikat_powitanie()

