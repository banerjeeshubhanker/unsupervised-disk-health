import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os
import subprocess

# Load the data collected from the bash script
df = pd.read_csv('disk_metrics.csv')

# Preprocessing the data
df['timestamp'] = pd.to_datetime(df['timestamp'])
device_column = df['device']
df.drop(columns=['timestamp', 'device'], inplace=True)
df.fillna(0, inplace=True)

# Normalize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Train the Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(scaled_data)

# Predict anomalies
df['anomaly'] = model.predict(scaled_data)
df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Save results with anomaly labels
df['device'] = device_column
df.to_csv('disk_metrics_with_anomalies.csv', index=False)

# Print out detected anomalies
anomalies = df[df['anomaly'] == 1]
print("Anomalies detected on the following devices:")
print(anomalies[['device']])

# Function to migrate data using rsync
def migrate_data(source_device, destination_directory):
    source_path = f"/mnt/{source_device}"
    destination_path = destination_directory
    rsync_command = f"rsync -a {source_path}/ {destination_path}/"
    
    try:
        # Mount the source disk if not mounted (this is system-specific and can be adjusted)
        if not os.path.ismount(source_path):
            subprocess.run(['mount', source_device, source_path], check=True)
        
        # Run rsync to migrate data
        print(f"Starting data migration from {source_device} to {destination_path}...")
        subprocess.run(rsync_command, shell=True, check=True)
        print(f"Data migration from {source_device} to {destination_path} completed.")
        
        # Optionally unmount the disk after migration
        subprocess.run(['umount', source_path], check=True)
        print(f"Unmounted {source_device}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during data migration: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Migrate data for each detected anomaly
destination_dir = "/mnt/backup_drive"  # Change this to your backup drive mount point

if len(anomalies) > 0:
    for device in anomalies['device'].unique():
        migrate_data(device, destination_dir)
else:
    print("No anomalies detected, no data migration needed.")
