# Disk Health Monitoring and Automatic Data Migration

This project monitors disk health and performance using SMART data and I/O statistics, detects potential disk failures using machine learning (Isolation Forest), and automatically migrates data from problematic disks to backup locations if anomalies are detected.

## Features
- Collects disk health data (SMART) and I/O performance metrics.
- Uses an unsupervised learning model (Isolation Forest) to detect anomalies.
- Automatically migrates data from failing disks using `rsync`.

## Prerequisites

Make sure the following tools are installed:
- **smartmontools** (for collecting SMART data):
  ```bash
  sudo apt-get install smartmontools
  ```
- **sysstat** (for I/O statistics collection):
  ```bash
  sudo apt-get install sysstat
  ```
- **Python 3.x** (with `pip` for package management).

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/disk-health-monitoring.git
   cd disk-health-monitoring
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the data collection script executable:**
   ```bash
   chmod +x collect_disk_metrics.sh
   ```

## Usage

### Step 1: Start Data Collection
Run the bash script to start collecting disk metrics (SMART data and I/O stats) every 60 seconds. The data will be saved in `disk_metrics.csv`.
```bash
./collect_disk_metrics.sh
```

### Step 2: Run Anomaly Detection and Data Migration
Once you have enough data, run the Python script to detect disk anomalies and automatically migrate data if necessary.

```bash
python disk_anomaly_detection.py
```

### Step 3: Monitor Logs
The Python script will print logs indicating:
- Any detected anomalies (disks that might be failing).
- The status of the data migration using `rsync`.

## Customization

### Change Backup Location
In the `disk_anomaly_detection.py` script, you can customize the backup location where data from failing disks will be migrated by modifying the `destination_dir` variable.

```python
destination_dir = "/mnt/backup_drive"  # Change this to your backup drive mount point
```

### Modify Data Collection Frequency
To modify how often disk metrics are collected, change the `sleep` value in the `collect_disk_metrics.sh` script (default is 60 seconds).

```bash
sleep 60  # Collect data every 60 seconds
```

## License
This project is licensed under the MIT License.
