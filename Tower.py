import TS_Generation as TG
import Interface
import time
start=time.time()
class Agent:
    def __init__(self,name,belief_base,goals):
        self.name=name
        self.belief_base = belief_base
        self.goals = goals
        self.sent_messages = []
        self.received_messages = []
def main():
    belief_base = ["on(1,0)", "on(2,0)", "on(3,0)", "on(4,0)", "on(5,0)", "on(6,0)","on(7,0)", "on(8,0)","on(9,0)","on(10,0)"]
    goal_base1 = ["on(1,2)", "on(2,3)", "on(3,4)", "on(4,0)", "on(5,0)", "on(6,5)","on(7,6)", "on(8,0)","on(9,8)","on(10,1)"]
    goal_base2 = ["on(1,2)", "on(2,0)", "on(3,1)", "on(4,0)", "on(5,4)", "on(6,0)","on(7,6)","on(8,7)","on(9,8)","on(10,3)"]
    goal_base3 = ["on(1,0)", "on(2,1)", "on(3,2)", "on(4,3)","on(5,0)","on(6,4)","on(7,5)","on(8,6)","on(9,7)","on(10,8)"]
    goals = [goal_base1,goal_base2,goal_base3]  # ,goal_base2,belief_base,goal_base3]
    knowledge_base = ["clear(0)",
                      "forall x. exists y. on(x,y) implies block(x)",
                      "forall x,y in D2 . block(x) and not on(y,x) and not holding(x) implies clear(x)",
                      "forall x,y. on(x,y) implies above(x,y)",
                      "forall x,y. exists z. on(x,z) and above(z,y) implies above(x,y)",
                      "forall x. on(x,0) implies tower([x])",
                      "forall x,y,t. on(x,y) and tower([y|t]) implies tower([x,y|t])"]

    constraints_of_action_generation = [
        "forall x. exists y,t. a-goal tower([x,y|t]) and  tower([y|t]) and clear(y) and holding(x) implies constructiveMove(x,y)",
        "forall x. exists y,t. a-goal tower([x,y|t]) and  tower([y|t]) and clear(y) and clear(x) implies constructiveMove(x,y)",
        "forall z. exists x,y,t. a-goal tower([x,y|t]) and above(z,x) implies misplaced(z)",
        "forall z. exists x,y,t. a-goal tower([x,y|t]) and above(z,y) implies misplaced(z)",
        "forall z. exists x. a-goal clear(x) and on(z,x) implies misplaced2(z)"
    ]
    linear_mode = False
    #linear_mode = True
    enableness_of_actions = [
        "forall x. exists y,z. constructiveMove(x,y) and clear(x) and not holding(z) implies pickup(x)",
        "forall x,z in D2 . misplaced(x) and clear(x) and not holding(z) implies pickup(x)",
        "forall x,z in D2 . misplaced2(x) and clear(x) and not holding(z) implies pickup(x)",
        "forall x,y. constructiveMove(x,y) and holding(x) and clear(y) implies putdown(x,y)",
        "forall x. holding(x) implies putdown(x,0)"]
    action_specification = {
        "pickup": "forall x,y. pickup(x) and not holding(x) and on(x,y) implies holding(x) and not on(x,y)",
        "putdown": "forall x,y. putdown(x,y) and clear(y) and holding(x) implies on(x,y) and not holding(x)"}
    constants = ["0", "1", "2", "3", "4", "5", "6","7","8","9","10"]
    domain = {"D1": ["0", "1", "2", "3", "4", "5", "6","7","8","9","10"],
              "D2": ["1", "2", "3", "4", "5", "6","7","8","9","10"]}
    tower = Agent("tower", belief_base, goals)
    sent_message_update=[]
    event_processing=[]
    Agents = [tower]
    generated_system = TG.system_generation(Agents, knowledge_base, constraints_of_action_generation,
                                            enableness_of_actions, action_specification, sent_message_update,
                                            event_processing, domain, linear_mode, constants)
    end = time.time()
    system = generated_system[0]
    transitions = generated_system[1]
    properties = generated_system[2]
    for i in system:
        print(i,system[i])
    f = open("Record.txt", "w+")
    f.write("The duration time is :" + str(end - start))
    f.close()

    Interface.interface_generation(system, transitions, properties)

main()