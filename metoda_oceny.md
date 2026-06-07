rides - łączna liczba wszystkich uruchomonych agentow (liczba prob)
laps - liczba osiagnietych okrazen
targets - liczba osiagnietych celow
collisions - liczba kolizji

n_steps -liczba krokow symulacji
agents - liczba agentow jednoczesnie

Q = (laps - collisions)/(steps \* agents)

<!-- lambda = 1 -->

Kolizja kończy epizod agenta sprawcy i wymusza restart, skutkuje tym samym co nieudana próba okrążenia.

<!-- Przy lambda = 1 jedna kolizja na próbę obniża wynik o tyle samo, co brak jednego pełnego okrążenia.

Lambda zwiekszona powoduje premiowanie bezpieczenstwa -->

Dla modelu wytrenowanego klasycznie, z wykrywaniem kolizji:
steps = 2000 \* 8 = 16 000
rides = 68
laps = 619
collisions = 60
laps = 619
Q = 0.0349
