Kolory użyte do rysowania plansz:
<img width="989" height="597" alt="kolory" src="https://github.com/user-attachments/assets/043eb122-950b-4b32-8194-b546100623b8" />

## Setup

1. Run container
   `docker compose up -d`
   Jeżeli chcemy przebudować obraz
   `docker compose up --build`
2. Open desktop at http://localhost:6080
3. Pull the repo if needed
   `cd /siu_project`
   `git pull`
4. Copy the board
   `cp /siu_project/trasa_nr1.png /roads.png`

## Run

W katalogu głównym znajduje się skrypt run.sh, który obsługuje trzy tryby pracy:

- ./run.sh train – uruchamia proces trenowania modelu.
- ./run.sh eval – uruchamia ruch żółwia na mapie treningowej (ewaluacja).
- ./run.sh test – uruchamia ruch żółwia na drugiej mapie (testowanie).

## How to attach container as remote server for VSCode

    1. Install Dev Containers extention
    2. Select siu container

## Etap 2

- [x] uzupełnić kod:
  - [x] okresowe zapisywanie modelu
  - [x] rzejechać 1/2 okresu, skręcić, przejechać pozostałą 1/2
- [x] wytrenować model
- [ ] zarejestrować najlepszy wynik
  - [x] w formie graficznej z zaznaczonymi krokami na planszy
  - [x] film z włączonym oraz z wyłączonymi znaczeniem położenia agenta.
- [x] eksperymenty
- [x] sprawozdanie
  - [x] opis eksperymentów

## Etap 3

- [ ] przygotować nową planszę
- [ ] przygtować nowe scenariusze
- [ ] uzupełnić kod
  - [ ] strategia wstawiania olwi w obszarach startowych
    - albo zawsze w swoim obszarze startowym
    - albo w innym obszarze startowym
- [ ] wytrenować sposób 1 - z wykrywaniem kolizji
- [ ] wytrenować sposób 2 - z douczaniem
- [ ] opracowac metodę ilościowej oceny modelu
- [ ] walidacja modeli
  - [ ] z wykrywaniem kolizji
  - [ ] z wykrywaniem kolizji, l. agentow x2
  - [ ] douczony
  - [ ] douczony, l agentow x2
- [ ] raport
