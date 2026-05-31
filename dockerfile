
FROM dudekw/siu-20.04

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt update -y && apt upgrade -y && apt install python3-pip python3-venv -y

# RUN apt install python3-pip -y
RUN python3 -m venv --system-site-packages /root/.venv

COPY requirements.txt .

RUN /root/.venv/bin/pip3 install -r requirements.txt

# ENTRYPOINT [ "./startup.sh" ]kk