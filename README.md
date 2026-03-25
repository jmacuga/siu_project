Kolory użyte do rysowania plansz:
<img width="953" height="614" alt="kolory" src="https://github.com/user-attachments/assets/304284eb-6070-4ce3-826a-ac7a92ad28e5" />

## Setup

1. Run container
`docker compose up -d`
2. Pull the repo if needed
`cd /siu_project`
`git pull`
3. Attach container as remote server for VSCode
    1. Install Dev Containers extention
    2. Select siu container
4. Copy the board
`cp /siu_project/trasa_nr1.png /roads.png`

## Run 

`roslaunch turlesim siu.launch`
`python siu_example.py`