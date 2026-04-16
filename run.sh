#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Użycie: $0 {train|eval|test}"
    exit 1
fi

MODE=$1

# domyślny brak kopiowania
COPY_CMD=""

case $MODE in
    train)
        PY_SCRIPT="dqn_single.py"
        COPY_CMD="cp trasa_nr1.png /roads.png"

        ;;
    eval)
        PY_SCRIPT="play_single_handout.py"
        COPY_CMD="cp trasa_nr1.png /roads.png"
        ;;
    test)
        PY_SCRIPT="play_single_handout.py"
        COPY_CMD="cp trasa_nr2.png /roads.png"

        ;;
    *)
        echo "Nieznany argument: $MODE"
        exit 1
        ;;
esac

# terminal 1 - Roslyn
lxterminal -e "bash -c '
source /root/siu_ws/devel/setup.bash;
# kopiowanie jeśli potrzebne
$COPY_CMD

echo Start Roslyn;
roslaunch turtlesim siu.launch
'" &

sleep 2

# terminal 2 - Python + ewentualne kopiowanie
lxterminal -e "bash -c '
source /root/siu_ws/devel/setup.bash;
echo Tryb: $MODE;


cd src
echo Uruchamiam $PY_SCRIPT;
python3 $PY_SCRIPT
'" &