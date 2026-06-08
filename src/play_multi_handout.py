import turtlesim_env_single
import numpy as np
from tensorflow.keras.models import load_model
from dqn_multi import DqnMulti
from turtlesim_env_multi import TurtlesimEnvMulti

env=TurtlesimEnvMulti()                  # utworzenie środowiska
env.PI_BY=3                                             # zmiana wybranych parametrów środowiska
env.DETECT_COLLISION=True
env.BRANCHED_MODEL=True
env.setup('scenariusz_wieloagentowy_v4.csv', agent_cnt=8)                                 # połączenie z symulatorem
agents=env.reset()                                      # utworzenie i umiejscowienie agenta
# agents=env.reset(None, 7)                                      # utworzenie i umiejscowienie agenta
tnames=agents.keys()                          # zapamiętanie identyfikatora agenta
prefix='trening_wieloagentowy_v3'                        # bazowy z kolizjami
dqnm=DqnMulti(env,id_prefix=prefix)                     # utworzenie klasy uczącej
dqnm.model=load_model('models/multiagent-branched-model-1-trening_wieloagentowy_z_galeziami_kolizji-Gr5_Cr200_Sw1.5_Sv-20.0_Sf-5.0_Dr2.0_Oo-100.0_Cd1.5_Ms150_Pb6_D0.99_E0.995_e0.1_M20000_m500_B32_U200_P4000_T4-1500.tf') # koncowy

current_states={tname:agent.map for tname,agent in agents.items()}
last_states={tname:agent.map for tname,agent in agents.items()}

for step in range(7000):
    controls={tname:np.argmax(dqnm.decision(dqnm.model,last_states[tname],current_states[tname])) for tname in tnames}
    actions={tname:dqnm.ctl2act(controls[tname]) for tname in tnames}

    step_results = env.step(actions, realtime=False)
    current_states = {tname: step_results[tname][0] for tname in tnames}
    rewards = {tname: step_results[tname][1] for tname in tnames}
    done = {tname: step_results[tname][2] for tname in tnames}

    last_states={tname:[i.copy() for i in current_states[tname]] for tname in tnames}
 
