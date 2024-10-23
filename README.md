# SATS

# Synchronized Automated Traffic Signaling with SUMO GUI and LSTM

This project aims to develop and simulate an automated traffic signaling system using the SUMO GUI and a machine learning algorithm (LSTM) for better traffic management.

## Overview

The goal is to synchronize traffic signals based on real-time traffic data, optimizing flow and reducing congestion. We use the SUMO (Simulation of Urban MObility) simulator for traffic simulation and the TraCI (Traffic Control Interface) to interact with the simulation. A Long Short-Term Memory (LSTM) neural network is employed for predicting traffic patterns and adjusting signals accordingly.

## Features

- **Real-time Traffic Simulation**: Using SUMO GUI to visualize and simulate traffic.
- **Automated Signal Control**: Dynamically control traffic lights based on real-time data.
- **Machine Learning Integration**: Implement LSTM for traffic prediction and optimization.
- **Dynamic Port Handling**: Automatically detect and connect to the SUMO GUI simulation port.

## Requirements

- Python 3.x
- SUMO (Simulation of Urban MObility)
- TraCI (part of SUMO tools)
- TensorFlow or PyTorch (for LSTM implementation)
