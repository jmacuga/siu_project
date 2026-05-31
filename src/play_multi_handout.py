import turtlesim_env_single
import numpy as np
from tensorflow.keras.models import load_model
from dqn_multi_handout import DqnMulti
from turtlesim_env_multi_handout import TurtlesimEnvMulti

env=TurtlesimEnvMulti.provide_env()                   # utworzenie środowiska
env.PI_BY=3                                             # zmiana wybranych parametrów środowiska
env.DETECT_COLLISION=True
env.setup('routes.csv', agent_cnt=4)                                 # połączenie z symulatorem
agents=env.reset()                                      # utworzenie i umiejscowienie agenta
# agents=env.reset(None, 7)                                      # utworzenie i umiejscowienie agenta
tnames=agents.keys()                          # zapamiętanie identyfikatora agenta
prefix='X6-c20c20c20d64-M-lr001'                        # bazowy z kolizjami
dqnm=DqnMulti(env,id_prefix=prefix)                     # utworzenie klasy uczącej
dqnm.model=load_model('dqns-Gr5_Cr200_Sw1.5_Sv-10.0_Sf-5.0_Dr2.0_Oo-100_Cd1.5_Ms20_Pb6_D0.99_E0.99_e0.05_M20000_m500_B32_U200_P4000_T4_1000.tf') # koncowy

current_states={tname:agent.map for tname,agent in agents.items()}
last_states={tname:agent.map for tname,agent in agents.items()}

for step in range(7000):
    controls={tname:np.argmax(dqnm.decision(dqnm.model,last_states[tname],current_states[tname])) for tname in tnames}
    actions={tname:dqnm.ctl2act(controls[tname]) for tname in tnames}
    current_states,rewards,done=env.step(actions, realtime=False)
    last_states={tname:[i.copy() for i in current_states[tname]] for tname in tnames}
 
