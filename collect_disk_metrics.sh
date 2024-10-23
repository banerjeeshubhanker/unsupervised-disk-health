#!/bin/bash

# Define output CSV file
OUTPUT_FILE="disk_metrics.csv"

# Check if the output file exists, if not, create it with headers
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "timestamp,device,read_iops,write_iops,read_latency,write_latency,utilization,reallocated_sectors,seek_error_rate,temp_celsius" > "$OUTPUT_FILE"
fi

# Function to collect SMART data and disk I/O performance metrics
collect_metrics() {
    # Get current timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Loop through all devices
    for DEV in /dev/sd[a-z]; do
        # Get SMART data
        SMART_DATA=$(smartctl -A $DEV | grep -E "Reallocated_Sector_Ct|Seek_Error_Rate|Temperature_Celsius")
        REALLOC_SECTORS=$(echo "$SMART_DATA" | grep "Reallocated_Sector_Ct" | awk '{print $10}')
        SEEK_ERROR_RATE=$(echo "$SMART_DATA" | grep "Seek_Error_Rate" | awk '{print $10}')
        TEMP_C=$(echo "$SMART_DATA" | grep "Temperature_Celsius" | awk '{print $10}')
        
        # Get I/O performance metrics from iostat
        IOSTAT_DATA=$(iostat -dx $DEV 1 1 | grep "$DEV")
        READ_IOPS=$(echo "$IOSTAT_DATA" | awk '{print $4}')
        WRITE_IOPS=$(echo "$IOSTAT_DATA" | awk '{print $5}')
        READ_LATENCY=$(echo "$IOSTAT_DATA" | awk '{print $7}')
        WRITE_LATENCY=$(echo "$IOSTAT_DATA" | awk '{print $8}')
        UTILIZATION=$(echo "$IOSTAT_DATA" | awk '{print $NF}')
        
        # Append metrics to CSV file
        echo "$TIMESTAMP,$DEV,$READ_IOPS,$WRITE_IOPS,$READ_LATENCY,$WRITE_LATENCY,$UTILIZATION,$REALLOC_SECTORS,$SEEK_ERROR_RATE,$TEMP_C" >> "$OUTPUT_FILE"
    done
}

# Collect metrics every 60 seconds
while true; do
    collect_metrics
    sleep 60
done
