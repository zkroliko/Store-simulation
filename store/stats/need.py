from mesa.datacollection import DataCollector

def need_compute(model):
    needed_items = [agent.need_count() for agent in model.schedule.agents if hasattr(agent, "need_count")]
    N = len(needed_items)
    if N > 0:
        B = sum(xi for i, xi in enumerate(needed_items))
        return B
    else:
        return 0

NeedCollector = DataCollector(
    model_reporters={"TotalNeeded": need_compute},
    agent_reporters={"TotalNeededR": lambda s: s.need_count() if hasattr(s, "need_count") else 0}
)