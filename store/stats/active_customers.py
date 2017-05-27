from mesa.datacollection import DataCollector

def active_customers_compute(model):
    customers = [agent for agent in model.schedule.agents if hasattr(agent, "need_count")]
    return len(customers)

ActiveCustomersCollector = DataCollector(
    model_reporters={"NCustomers": active_customers_compute},
    agent_reporters={"NCustomersR": lambda s: 1 if hasattr(s, "need_count") else 0}
)