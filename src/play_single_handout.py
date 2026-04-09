import numpy as np
from tensorflow.keras.models import load_model
import turtlesim_env_single
from dqn_single import DqnSingle
env=turtlesim_env_single.provide_env()                  # sfabrykowanie środowiska
env.setup('routes.csv',agent_cnt=1)                     # wczytanie tras i zarezerwowanie 1 agenta
agents=env.reset()                                      # utworzenie i umiejscowienie agenta
tname=list(agents.keys())[0]                            # zapamiętanie identyfikatora agenta
dqn=DqnSingle(env, 'test')                              # utworzenie klasy uczącej (tam są metody wyliczania sterowania)
dqn.model=load_model('moj_bardzo_udany_model.tf')
current_state=agents[tname].map
last_state=[i.copy() for i in current_state]
for step in range(10):
    control=np.argmax(dqn.decision(dqn.model,last_state,current_state))
    last_state=current_state
    current_state,reward,done=env.step({tname:dqn.ctl2act(control)})
