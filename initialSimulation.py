import traci
import pandas as pd
import time

# Connect to the running SUMO GUI simulation
traci_port = 9999
traci.init(traci_port)

data = []

step = 0
start_time = time.time()  # Start time for the simulation
last_step_with_cars = 0

while step < 900:  # Arbitrary step limit; can be adjusted
    traci.simulationStep()
    num_vehicles = traci.simulation.getMinExpectedNumber()  # Get the number of remaining vehicles

    if num_vehicles > 0:
        last_step_with_cars = step  # Track the last step where cars were present
    
    tls_ids = traci.trafficlight.getIDList()  # Get all traffic light IDs (junctions)
    
    for tls_id in tls_ids:
        lane_ids = traci.trafficlight.getControlledLanes(tls_id)  # Get lanes controlled by the traffic light
        for lane_id in lane_ids:
            car_count = traci.lane.getLastStepVehicleNumber(lane_id)
            waiting_time = traci.lane.getWaitingTime(lane_id)
            if car_count >= 0:
                data.append([step, tls_id, lane_id, car_count, waiting_time])
    
    if num_vehicles == 0:
        break  # Stop the simulation when no cars remain
    
    step += 1

# Calculate elapsed time since no more cars remain
elapsed_time = time.time() - start_time

traci.close()

# Log simulation time
print(f"Initial Simulation Time (until no cars remain): {elapsed_time:.2f} seconds")

# Save data to a CSV file
df = pd.DataFrame(data, columns=['step', 'junction_id', 'lane_id', 'car_count', 'waiting_time'])
df.to_csv('traffic_data4.csv', index=False)
