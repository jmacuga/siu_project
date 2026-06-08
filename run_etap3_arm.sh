#!/bin/bash

usage() {
    echo "Użycie: $0 {train|eval} [--branched]"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

MODE=""
BRANCHED=""
for arg in "$@"; do
    case $arg in
        train|eval)
            if [ -n "$MODE" ]; then
                echo "Podaj tylko jeden tryb: train lub eval." >&2
                exit 1
            fi
            MODE=$arg
            ;;
        --branched)
            BRANCHED=1
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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# VNC / MATE desktop in tiryoh/ros-desktop-vnc uses :1 as ubuntu; GUI terminals need a valid cookie.
if [ -z "${DISPLAY:-}" ]; then
    export DISPLAY=:1
fi
if [ -z "${XAUTHORITY:-}" ]; then
    if [ -f "${HOME}/.Xauthority" ]; then
        export XAUTHORITY="${HOME}/.Xauthority"
    elif [ "$(id -u)" -eq 0 ] && [ -f /home/ubuntu/.Xauthority ]; then
        # np. sudo ./run.sh — sesja VNC jest użytkownika ubuntu
        export XAUTHORITY=/home/ubuntu/.Xauthority
    fi
fi

# ROS workspace (ARM Docker: ~/siu_ws lub /opt/siu_ws; stary layout: /root/siu_ws)
ROS_SETUP=""
for candidate in "${HOME}/siu_ws/devel/setup.bash" /opt/siu_ws/devel/setup.bash /root/siu_ws/devel/setup.bash; do
    if [ -f "$candidate" ]; then
        ROS_SETUP="$candidate"
        break
    fi
done
if [ -z "$ROS_SETUP" ]; then
    echo "Nie znaleziono devel/setup.bash (szukano: \"\$HOME/siu_ws\", /opt/siu_ws, /root/siu_ws)." >&2
    exit 1
fi


MODEL_NAME="model/trening_wieloagentowy_v7-Gr5_Cr200_Sw5.0_Sv-20.0_Sf-5.0_Dr2.0_Oo-100.0_Cd1.5_Ms100_Pb6_D0.99_E0.995_e0.1_M20000_m500_B32_U200_P4000_T4-2000.tf"
BRANCHED_MODEL_NAME="model/multiagent-branched-model-v3-trening_wieloagentowy_z_galeziami_kolizji-Gr5_Cr200_Sw1.5_Sv-20.0_Sf-5.0_Dr2.0_Oo-100.0_Cd1.5_Ms150_Pb6_D0.99_E0.995_e0.1_M20000_m500_B32_U200_P2000_T4-1750.tf"

COPY_CMD=""
COPY_CSV_CMD=""
case $MODE in
    train)
        PY_SCRIPT="dqn_multi.py"
        COPY_CMD="cp trasa_nr3.png /home/ubuntu/siu_ws/src/ros_tutorials/turtlesim/images/roads.png"
        COPY_CSV_CMD="cp scenariusz_wieloagentowy_v3.csv src/routes.csv"
        ;;
    eval)
        if [ -n "$BRANCHED" ]; then
            PY_SCRIPT="play-dqn.py --multi --detect_collision --branched --n_agents 8 --n_steps 2000 $BRANCHED_MODEL_NAME"
        else
            PY_SCRIPT="play-dqn.py --multi --detect_collision --n_agents 8 --n_steps 2000 $MODEL_NAME"
        fi
        COPY_CMD="cp trasa_nr3.png /home/ubuntu/siu_ws/src/ros_tutorials/turtlesim/images/roads.png"
        COPY_CSV_CMD="cp scenariusz_wieloagentowy_v3.csv src/routes.csv"
        ;;
    *)
        echo "Nieznany argument: $MODE"
        exit 1
        ;;
esac

# Obraz tiryoh ma terminator; lxterminal bywa niezainstalowany lub bez dostępu do wyświetlacza.
launch_term() {
    local title="$1"
    local cmd="$2"
    if command -v terminator >/dev/null 2>&1; then
        terminator -T "$title" -e "bash -lc $(printf '%q' "$cmd")" &
    elif command -v mate-terminal >/dev/null 2>&1; then
        mate-terminal --title="$title" -e "bash -lc $(printf '%q' "$cmd")" &
    elif command -v lxterminal >/dev/null 2>&1; then
        lxterminal -t "$title" -e "bash -lc $(printf '%q' "$cmd")" &
    else
        echo "Brak terminator/mate-terminal/lxterminal — uruchom skrypt z terminala na pulpicie VNC (MATE)." >&2
        bash -lc "$cmd" &
    fi
}

cmd_ros="source $(printf '%q' "$ROS_SETUP"); $COPY_CMD; echo Start Roslyn; roslaunch turtlesim siu.launch; exec bash"
cmd_py="source $(printf '%q' "$ROS_SETUP"); echo Tryb: $MODE; cd $(printf '%q' "$SCRIPT_DIR")/src && echo Uruchamiam $PY_SCRIPT && python3 $PY_SCRIPT; exec bash"

launch_term "ROS" "$cmd_ros"
sleep 2
$COPY_CSV_CMD
launch_term "Python $MODE" "$cmd_py"
