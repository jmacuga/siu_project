#!/bin/bash

usage() {
    echo "Użycie: $0 {train|eval|test}"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

MODE=""
for arg in "$@"; do
    case $arg in
        train|eval|test)
            if [ -n "$MODE" ]; then
                echo "Podaj tylko jeden tryb: train, eval lub test." >&2
                exit 1
            fi
            MODE=$arg
            ;;
        --etap3)
            ETAP3=1
            ;;
        *)
            echo "Nieznany argument: $arg" >&2
            usage
            ;;
    esac
done

if [ -z "$MODE" ]; then
    usage
fi

COPY_PNG_CMD=""
COPY_CSV_CMD=""

case $MODE in
    train)
        PY_SCRIPT="dqn_multi_handout.py"
        COPY_PNG_CMD="cp trasa_nr3.png /roads.png"
        COPY_CSV_CMD="cp scenariusz_wieloagentowy.csv src/routes.csv"
        ;;
    eval)
        PY_SCRIPT="play_multi_handout.py"
        COPY_PNG_CMD="cp trasa_nr3.png /roads.png"
        COPY_CSV_CMD="cp scenariusz_wieloagentowy.csv src/routes.csv"
        ;;
esac

# terminal 1 - Roslyn
lxterminal -e "bash -c '
source /root/siu_ws/devel/setup.bash;
# kopiowanie jeśli potrzebne
$COPY_PNG_CMD

echo Start Roslyn;
roslaunch turtlesim siu.launch
'" &

sleep 2

# terminal 2 - Python + ewentualne kopiowanie
lxterminal -e "bash -c '
source /root/siu_ws/devel/setup.bash;
echo Tryb: $MODE;
if [ "$ETAP3" -eq 1 ]; then echo Etap 3: wieloagentowy; fi

$COPY_CSV_CMD
cd src
echo Uruchamiam $PY_SCRIPT;
python3 $PY_SCRIPT
'" &
