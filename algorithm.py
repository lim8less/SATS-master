import json
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib
import sys

# Ensure stdout uses utf-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load and preprocess data
data = pd.read_csv('traffic_data4.csv', encoding='utf-8')

# Filter numeric columns
numeric_cols = ['car_count', 'waiting_time']
junction_ids = data['junction_id'].unique().tolist()
scalers = {}

# Normalize data per junction
for junction_id in junction_ids:
    junction_data = data[data['junction_id'] == junction_id][numeric_cols]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scalers[junction_id] = scaler
    data.loc[data['junction_id'] == junction_id, numeric_cols] = scaler.fit_transform(junction_data)

# Save the scalers for later use
joblib.dump(scalers, 'scalers.pkl')

# Prepare data for LSTM
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), :]
        X.append(a)
        Y.append(dataset[i + look_back, 1])  # Using waiting_time for Y (predicting green light duration)
    return np.array(X), np.array(Y)

look_back = 3
X_list, Y_list = [], []

# Create dataset for each junction
for junction_id in junction_ids:
    junction_data = data[data['junction_id'] == junction_id][numeric_cols].values
    if len(junction_data) > look_back:
        X_junction, Y_junction = create_dataset(junction_data, look_back)
        X_list.append(X_junction)
        Y_list.append(Y_junction)
    else:
        print(f"Not enough data for junction {junction_id}")

# Combine datasets from all junctions
if X_list and Y_list:
    X = np.concatenate(X_list, axis=0)
    Y = np.concatenate(Y_list, axis=0)
    X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2]))

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 2)))  # Input shape adjusted to (look_back, 2)
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X, Y, epochs=10, batch_size=32, verbose=2)

    # Save the trained model
    model.save('traffic_light_model.h5')

    # Predict for each junction
    predictions_dict = {}

    for junction_id in junction_ids:
        junction_data = data[data['junction_id'] == junction_id][numeric_cols].values
        if len(junction_data) > look_back:
            X_junction, _ = create_dataset(junction_data, look_back)
            X_junction = np.reshape(X_junction, (X_junction.shape[0], X_junction.shape[1], X_junction.shape[2]))

            predictions = model.predict(X_junction)
            predictions = np.reshape(predictions, (-1, 1))  # Reshape predictions to match scaler's expectations
            scaler = scalers[junction_id]
            predictions = scaler.inverse_transform(np.hstack((np.zeros((predictions.shape[0], 1)), predictions)))[:, 1]  # Inverse transform with dummy first column
            predictions_dict[junction_id] = predictions.tolist()
        else:
            print(f"Not enough data for junction {junction_id} to make predictions")

    # Save junction_ids and predictions to a JSON file
    with open('predictions.json', 'w') as f:
        json.dump({'junction_ids': junction_ids, 'predictions': predictions_dict}, f)

    # Evaluate and plot results for each junction
    plt.figure(figsize=(15, 10))

    all_predictions = np.concatenate([pred for pred in predictions_dict.values()])
    for junction_id in junction_ids:
        junction_data = data[data['junction_id'] == junction_id]
        true_data = junction_data['waiting_time'].values[look_back+1:]  # Adjust for look_back
        predictions = all_predictions[:len(true_data)]
        all_predictions = all_predictions[len(true_data):]

        plt.plot(true_data, label=f'True Data for junction {junction_id}')
        plt.plot(predictions, label=f'Predictions for junction {junction_id}')

    plt.xlabel('Time Steps')
    plt.ylabel('Waiting Time')
    plt.title('True vs Predicted Waiting Time for Each Junction')
    plt.legend()
    plt.show()
else:
    print("Not enough data to train the model.")
