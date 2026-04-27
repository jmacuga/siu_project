import numpy as np
from tensorflow.keras.models import load_model
import turtlesim_env_single
from dqn_single import DqnSingle
env=turtlesim_env_single.provide_env()                  # sfabrykowanie środowiska
env.setup('routes.csv',agent_cnt=1)                     # wczytanie tras i zarezerwowanie 1 agenta
agents=env.reset()                                      # utworzenie i umiejscowienie agenta
# agents=env.reset(None, 7)                                      # utworzenie i umiejscowienie agenta
tname=list(agents.keys())[0]                            # zapamiętanie identyfikatora agenta
dqn=DqnSingle(env, 'test')                              # utworzenie klasy uczącej (tam są metody wyliczania sterowania)
dqn.model=load_model('dqns-Gr5_Cr200_Sw1.5_Sv-10.0_Sf-5.0_Dr2.0_Oo-30_Cd1.5_Ms20_Pb6_D0.9_E0.995_e0.05_M20000_m4000_B32_U200_P4000_T4_1000.tf')
current_state=agents[tname].map
last_state=[i.copy() for i in current_state]
for step in range(1000):
    control=np.argmax(dqn.decision(dqn.model,last_state,current_state))
    last_state=current_state
    current_state,reward,done=env.step({tname:dqn.ctl2act(control)}, realtime=False)
