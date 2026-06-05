# encoding: utf8
import numpy as np
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from turtlesim_env_base import TurtlesimEnvBase

class TurtlesimEnvMulti(TurtlesimEnvBase):
    def __init__(self):
        super().__init__()

    def _front_occupied(self, tname: str, current_map) -> bool:
        """True, gdy w polu widzenia z przodu (raster fo) wykryto innego agenta."""
        fo = current_map[6]
        return fo[self.GRID_RES // 2, self.GRID_RES - 1] == 0

    def _collision_culprits(self, actions: dict, collisions: list, step_maps: dict) -> set:
        """
        Wyznacza agentów-sprawców kolizji w bieżącym kroku symulacji.
        Para z getColisions(); sprawca: wyższa prędkość w kroku, przy remisie — wykrycie z przodu (fo).
        """
        culprits: set[str] = set()
        if not self.DETECT_COLLISION:
            return culprits
        if not collisions:
            return culprits

        step_speed = {}
        front_blocked = {}
        for tname in actions:
            pose = self.agents[tname].pose
            pose1 = self.tapi.getPose(tname)
            dx = pose1.x - pose.x
            dy = pose1.y - pose.y
            step_speed[tname] = np.sqrt(dx * dx + dy * dy) / self.SEC_PER_STEP
            front_blocked[tname] = self._front_occupied(tname, step_maps[tname])

        eps = 1e-6     #epsilon, to treat small differences as a tie
        for collision in collisions:
            n1 = collision.get('name1')
            n2 = collision.get('name2')
            if n1 not in actions or n2 not in actions:
                continue
            a, b = n1, n2
            va, vb = step_speed[a], step_speed[b]
            if va > vb + eps:
                culprits.add(a)
            elif vb > va + eps:
                culprits.add(b)
            else:
                if front_blocked[a]:
                    culprits.add(a)
                if front_blocked[b]:
                    culprits.add(b)
                if a not in culprits and b not in culprits:
                    culprits.add(a)
        return culprits

    def setup(self,routes_fname:str,agent_cnt=None):
        super().setup(routes_fname,agent_cnt)
        for agent in self.agents.values():              # liczba kroków - indywidualnie dla każdego agenta
            agent.step_sum=0

    def reset(self,tnames=None,sections='default'):
        ret=super().reset(tnames,sections)
        if tnames is None:
            tnames=self.agents.keys()
        for tname in tnames:
            self.agents[tname].step_sum=0               # liczba kroków zerowana wybiórczo
        return ret

    def step(self,actions,realtime=False):              # {id_żółwia:(prędkość,skręt)}
        # pozycja PRZED krokiem sterowania
        for tname,action in actions.items():
            agent=self.agents[tname]
            agent.step_sum+=1
            agent.pose=self.tapi.getPose(tname)         # zapamiętanie położenia przed wykonaniem ruchu
            _,_,_,agent.fd,_,_ = self.get_road(tname)   # odl. do celu (na wypadek, gdyby uległa zmianie)
            # action: [prędkość,skręt]
            # TODO - DONE STUDENCI przejechać 1/2 okresu, skręcić, przejechać pozostałą 1/2
            if realtime:  
                twist = Twist()
                twist.linear.x = action[0] 
                twist.angular.z = action[1] / self.SEC_PER_STEP 
                self.tapi.setVel(tname, twist)
                rospy.sleep(self.SEC_PER_STEP) 
                self.tapi.setVel(tname, Twist())
            else:  # skok+obrót
                pose = self.agents[tname].pose
                # obliczenie i wykonanie przesunięcia
                vx = np.cos(pose.theta + action[1]) * action[0] * self.SEC_PER_STEP
                vy = np.sin(pose.theta + action[1]) * action[0] * self.SEC_PER_STEP
                p = Pose(x=pose.x + vx, y=pose.y + vy, theta=pose.theta + action[1])
                self.tapi.setPose(tname, p, mode='absolute')
            rospy.sleep(self.WAIT_AFTER_MOVE)

        # pozycje i sytuacje PO kroku sterowania
        ret={}                                              # {tname:(get_map(),reward,done)}
        collisions = self.tapi.getColisions(self.agents.keys(), self.COLLISION_DIST)
        step_maps = {tname: self.get_map(tname) for tname in actions}
        collision_culprits = self._collision_culprits(actions, collisions, step_maps) # DONE STUDENCI wykrywanie kolizji + kara

        for tname in actions:
            pose=self.agents[tname].pose                    # położenie przed ruchem
            pose1=self.tapi.getPose(tname)                  # położenie po ruchu
            self.agents[tname].pose=pose1                  
            
            fx1,fy1,fa1,fd1,_,_ = self.get_road(tname)      # warunki drogowe po przemieszczeniu
            vx1 = (pose1.x-pose.x)/self.SEC_PER_STEP        # aktualna prędkość - składowa x
            vy1 = (pose1.y-pose.y)/self.SEC_PER_STEP        #        -"-                   y
            v1  = np.sqrt(vx1**2+vy1**2)                    # aktualny moduł prędkości
            fv1 = np.sqrt(fx1**2+fy1**2)                    # zalecany moduł prędkości
            # wyznaczenie składników funkcji celu
            done=False
            r1 = min(0,self.SPEED_FINE_RATE*(v1-fv1))       # kara za przekroczenie prędkości
            r2 = 0
            if fv1>.001:
                vf1 = (vx1*fx1+vy1*fy1)/fv1                 # rzut prędkości faktycznej na zalecaną
                if vf1>0:
                    r2 = self.SPEED_RWRD_RATE*vf1           # nagroda za jazdę z prądem
                else:
                    r2 = -self.SPEED_RVRS_RATE*vf1          # kara za jazdę pod prąd
            r3 = self.DIST_RWRD_RATE*(self.agents[tname].fd-fd1)    # nagroda za zbliżenie się do celu
            r4=0
            if abs(fx1)+abs(fy1)<.01 and fa1==1:            # wylądowaliśmy poza trasą
                r4 = self.OUT_OF_TRACK_FINE
                done=True
            map=self.get_map(tname)
            # kolizja: kara i koniec epizodu tylko u agenta-sprawcy
            r5 = 0
            if tname in collision_culprits:
                r5 = self.COLLISION_FINE
                done = True       

            reward=fa1*(r1+r2)+r3+r4+r5
            # sp=speed, fl=flow, cl=closing, tr=track, xx=collision
            print(f'RWD: {reward:.2f} = {fa1:.2f}*(sp{r1:.2f} fl{r2:.2f}) cl{r3:.2f} tr{r4:.2f} xx{r5:.2f}')
            if self.agents[tname].step_sum>self.MAX_STEPS:
                done=True
            ret[tname]=(map,reward,done)
        return ret

def provide_env():
    return TurtlesimEnvMulti()

if __name__ == "__main__":
    import random
    env=provide_env()
    env.PI_BY=100                                           # początkowo wszyscy skierowani praktycznie na azymut
    env.DETECT_COLLISION=True
    env.setup('routes.csv',agent_cnt=100)
    agents=env.reset()
    for i in range(100):                                    # losowy agent wykonuje losowy ruch
        tname=random.choice(list(agents.keys()))
        res=env.step({tname:(random.uniform(.2,1),random.uniform(-.3,.3))})
        if res[tname][2]:                                   # kolizja lub aut wyklucza agenta z dalszej symulacji
            del agents[tname]
