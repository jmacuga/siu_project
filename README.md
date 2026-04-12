Kolory użyte do rysowania plansz:
<img width="989" height="597" alt="kolory" src="https://github.com/user-attachments/assets/043eb122-950b-4b32-8194-b546100623b8" />

## Setup

1. Run container
`docker compose up -d`
2. Open desktop at http://localhost:6080
3. Pull the repo if needed
`cd /siu_project`
`git pull`
4. Copy the board
`cp /siu_project/trasa_nr1.png /roads.png`
## Run 

`roslaunch turlesim siu.launch`
`python siu_example.py`

## How to attach container as remote server for VSCode
    1. Install Dev Containers extention
    2. Select siu container

## TODO
- [ ] uzupełnić kod:
    - [ ] okresowe zapisywanie modelu
    - [ ] rzejechać 1/2 okresu, skręcić, przejechać pozostałą 1/2
- [ ] wytrenować model
- [ ] zarejestrować najlepszy wynik
    - [ ] w formie graficznej z zaznaczonymi krokami na planszy
    - [ ] film z włączonym oraz z wyłączonymi znaczeniem położenia agenta.
- [ ] eksperymenty
    - [ ] 
    - [ ] 
- [ ] sprawozdanie
    - [ ] opis eksperymentów
