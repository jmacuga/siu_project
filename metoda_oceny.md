rides - łączna liczba wszystkich uruchomonych agentow (liczba prob)
laps - liczba osiagnietych okrazen
targets - liczba osiagnietych celow
collisions - liczba kolizji

n_steps -liczba krokow symulacji
agents - liczba agentow jednoczesnie

<!-- Q = (laps - collisions)/(steps \* agents) -->

Q = (targets − lambda × collisions) / (n_steps × agents)

lambda = 0.5

Kolizja kończy epizod agenta sprawcy i wymusza restart, skutkuje tym samym co nieudana próba okrążenia.

Lambda zwiekszona powoduje premiowanie bezpieczenstwa -->

### Dla modelu wytrenowanego klasycznie, z wykrywaniem

<!-- scenariusz: v4
kolizji:
steps = 2000 \* 8 = 16 000
rides = 68
laps = 619
collisions = 60
laps = 619 -->

<!-- Q = 0.0349 -->

scenariusz v3
agents=8
collisions =80
targets=44
rides=97
laps=11.0

Q =

agents=16
collisions=429
targets=138
rides=457
laps= 34.5

### Dla modelu branched:

scenariusz: v3
agents = 8
n_steps = 2000
collisions=106
targets=34,
rides=160,
laps=8.5
Q = -0.006

### Dla modelu branched trenowanego na v3

agents=8
collisions=39
targets=80
rides=80
laps=20

agents=16
collisions=216
targets=150,
rides=286
laps=37.5
