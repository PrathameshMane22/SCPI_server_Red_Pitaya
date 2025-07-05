import sys
import time
import csv
from datetime import datetime
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt

# Connect to Red Pitaya
rp_s = scpi.scpi(sys.argv[1])

# Reset Generator and Acquisition
rp_s.tx_txt('GEN:RST')
rp_s.tx_txt('ACQ:RST')

# Configure signal generation
rp_s.tx_txt('SOUR1:FUNC SINE')
rp_s.tx_txt('SOUR1:FREQ:FIX 1000')
rp_s.tx_txt('SOUR1:VOLT 1')
rp_s.tx_txt('SOUR1:BURS:STAT BURST')
rp_s.tx_txt('SOUR1:BURS:NCYC 1')

# Acquisition settings
rp_s.tx_txt('ACQ:DEC 64')
rp_s.tx_txt('ACQ:TRIG:LEV 0')
rp_s.tx_txt('ACQ:TRIG:DLY 0')

# Time base (sampling interval based on decimation)
base_sample_rate = 125e6  # 125 MS/s
decimation = 64
sample_interval = decimation / base_sample_rate  # seconds per sample

# CSV setup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"acq_streamed_{timestamp}.csv"
sample_index = 0  # Tracks global sample index

# Create and open the CSV file with header
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Voltage'])

# Start live plotting
plt.ion()
fig, ax = plt.subplots()

try:
    while True:
        # Reset acquisition
        rp_s.tx_txt('ACQ:START')
        time.sleep(1)
        rp_s.tx_txt('ACQ:TRIG AWG_PE')
        rp_s.tx_txt('OUTPUT1:STATE ON')
        rp_s.tx_txt('SOUR1:TRIG:INT')

        # Wait for trigger
        while True:
            rp_s.tx_txt('ACQ:TRIG:STAT?')
            if rp_s.rx_txt() == 'TD':
                break

        # Wait until buffer is filled
        while True:
            rp_s.tx_txt('ACQ:TRIG:FILL?')
            if rp_s.rx_txt() == '1':
                break

        # Read acquired data
        rp_s.tx_txt('ACQ:SOUR1:DATA?')
        buff_string = rp_s.rx_txt()
        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        buff = list(map(float, buff_string))

        # Calculate time values
        time_values = [sample_index * sample_interval + i * sample_interval for i in range(len(buff))]

        # Append to CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for t, v in zip(time_values, buff):
                writer.writerow([t, v])

        print(f"[+] Appended {len(buff)} samples to {csv_filename}")

        # Update sample index
        sample_index += len(buff)

        # Plot
        ax.clear()
        ax.plot(time_values, buff)
        ax.set_title("Streaming Acquisition: Time vs Voltage")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.grid(True)
        plt.pause(0.1)

        time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Acquisition stopped by user.")
    plt.ioff()
    plt.show()