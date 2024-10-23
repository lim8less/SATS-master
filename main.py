import subprocess
import time
import traci

def run_initial_simulation():
    # Run the initial SUMO simulation with the initial configuration file on port 9999
    print("Running initial SUMO simulation on port 9999...")
    sumo_process = subprocess.Popen(["sumo-gui", "-c", "initial_configuration.sumo.cfg", "--remote-port", "9999"])
    
    # Run initialSimulation.py concurrently
    print("Running initialSimulation.py...")
    simulation_process = subprocess.Popen(["python", "initialSimulation.py"])

    # Wait for both processes to complete
    sumo_process.wait()
    simulation_process.wait()

    print("Initial simulation has completed.")

def generate_model_and_predictions():
    # Run the algorithm.py script to process traffic_data4.csv
    print("Running algorithm.py...")
    subprocess.run(["python", "algorithm.py"])

def generate_traffic_light_logic():
    # Run the finalSimulation.py script to generate traffic_light_logic.xml
    print("Running finalSimulation.py...")
    subprocess.run(["python", "finalSimulation.py"])

def run_final_simulation():
    # Start the final SUMO simulation with TraCI
    traci.start(["sumo-gui", "-c", "configuration.sumo.cfg"])

    step = 0
    start_time = time.time()  # Start timing the final simulation

    while step < 1000:  # Arbitrary step limit; can be adjusted
        traci.simulationStep()
        num_vehicles = traci.simulation.getMinExpectedNumber()  # Get the number of remaining vehicles

        if num_vehicles == 0:
            break  # Stop when no cars remain
        
        step += 1

    # Calculate elapsed time when no cars remain
    elapsed_time = time.time() - start_time

    traci.close()
    print(f"Final Simulation Time (until no cars remain): {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    start_time = time.time()

    run_initial_simulation()
    generate_model_and_predictions()
    generate_traffic_light_logic()
    run_final_simulation()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
