# Red Pitaya SCPI Python Data Acquisition

A Python script for streaming data acquisition from Red Pitaya using SCPI commands with real-time visualization and CSV logging.

## Overview

This project demonstrates how to use Red Pitaya's SCPI interface to:
- Generate sine wave signals with burst mode
- Continuously acquire data from analog inputs
- Stream data to CSV files with timestamps
- Provide real-time visualization of acquired signals

## Features

- **Signal Generation**: Configurable sine wave generation with burst mode
- **Continuous Acquisition**: Streaming data acquisition with configurable decimation
- **Data Logging**: Automatic CSV file creation with timestamps
- **Real-time Visualization**: Live plotting of acquired signals
- **Time-based Analysis**: Precise timing calculations based on sampling parameters

## Requirements

### Hardware
- Red Pitaya board (any model with SCPI support)
- Network connection to Red Pitaya
- Signal source connected to input channel 1 (optional, for external triggering)

### Software Dependencies

Install the required Python packages:

```bash
pip install matplotlib numpy PyVISA
```

### Red Pitaya Setup

1. **Download the SCPI Library**: 
   - Download `redpitaya_scpi.py` from [Red Pitaya Examples Repository](https://github.com/RedPitaya/RedPitaya-Examples/blob/dev/python/redpitaya_scpi.py)
   - Place it in the same directory as `python_scp_trial.py`

2. **Start SCPI Server**:
   - Access Red Pitaya web interface
   - Navigate to Development section
   - Click on "SCPI server" 
   - Press "RUN" button
   - Note the IP address displayed (e.g., `192.168.178.100`)

## File Structure

```
project_directory/
├── python_scp_trial.py         # Main acquisition script
├── redpitaya_scpi.py           # Red Pitaya SCPI library
└── README.md                   # This file
```

## Usage

### Basic Usage

```bash
python python_scp_trial.py <RED_PITAYA_IP>
```

**Example:**
```bash
python python_scp_trial.py 192.168.178.100
```

### Script Configuration

The script includes several configurable parameters:

#### Signal Generation Settings
```python
# Frequency: 1 kHz sine wave
rp_s.tx_txt('SOUR1:FREQ:FIX 1000')

# Amplitude: 1V peak-to-peak
rp_s.tx_txt('SOUR1:VOLT 1')

# Burst mode: Single cycle per trigger
rp_s.tx_txt('SOUR1:BURS:NCYC 1')
```

#### Acquisition Settings
```python
# Decimation factor (affects sampling rate)
rp_s.tx_txt('ACQ:DEC 64')

# Trigger level: 0V
rp_s.tx_txt('ACQ:TRIG:LEV 0')

# Trigger delay: 0 samples
rp_s.tx_txt('ACQ:TRIG:DLY 0')
```

### Sampling Rate Calculation

The effective sampling rate is calculated as:
```python
base_sample_rate = 125e6  # 125 MS/s (Red Pitaya base rate)
decimation = 64
effective_sample_rate = base_sample_rate / decimation  # ~1.95 MS/s
```

## Output Files

### CSV Data Format

Generated CSV files contain:
- **Filename**: `acq_streamed_YYYYMMDD_HHMMSS.csv`
- **Columns**: 
  - `Time (s)`: Timestamp for each sample
  - `Voltage`: Acquired voltage value

**Example CSV content:**
```csv
Time (s),Voltage
0.0,0.0012
8e-09,0.0023
1.6e-08,0.0034
...
```

## Operation Flow

1. **Initialization**:
   - Connect to Red Pitaya via IP address
   - Reset generator and acquisition modules
   - Configure signal generation parameters

2. **Acquisition Loop**:
   - Start acquisition
   - Trigger signal generation
   - Wait for trigger event
   - Wait for buffer fill
   - Read acquired data
   - Calculate time values
   - Save to CSV file
   - Update real-time plot

3. **Data Processing**:
   - Convert raw data to float values
   - Calculate precise timestamps
   - Append to CSV with continuous time indexing

## Stopping the Acquisition

- Press `Ctrl+C` to stop the acquisition
- The script will gracefully exit and display the final plot
- All acquired data will be saved in the CSV file

## Troubleshooting

### Common Issues

1. **Connection Error**:
   ```
   [ERROR] Cannot connect to Red Pitaya
   ```
   - Verify Red Pitaya IP address
   - Ensure SCPI server is running
   - Check network connectivity

2. **Import Error**:
   ```
   ModuleNotFoundError: No module named 'redpitaya_scpi'
   ```
   - Download `redpitaya_scpi.py` and place in project directory
   - Ensure the file is in the same folder as the script

3. **Permission Error**:
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   - Check file write permissions in the directory
   - Ensure CSV file is not open in another application

### Performance Considerations

- **Decimation**: Higher decimation values reduce data rate but lower resolution
- **Network**: Ensure stable network connection for continuous data streaming
- **Storage**: Monitor disk space for long-duration acquisitions

## Advanced Configuration

### Modifying Trigger Settings

```python
# External trigger
rp_s.tx_txt('ACQ:TRIG:SOUR EXT_PE')  # External positive edge

# Different trigger levels
rp_s.tx_txt('ACQ:TRIG:LEV 0.5')  # 500mV trigger level
```

### Changing Acquisition Parameters

```python
# Different decimation values
rp_s.tx_txt('ACQ:DEC 8')    # Higher sampling rate
rp_s.tx_txt('ACQ:DEC 1024') # Lower sampling rate

# Pre-trigger delay
rp_s.tx_txt('ACQ:TRIG:DLY 8192')  # Delay in samples
```

## Technical Details

### SCPI Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `GEN:RST` | Reset generator | - |
| `ACQ:RST` | Reset acquisition | - |
| `SOUR1:FUNC` | Set waveform type | `SINE`, `SQUARE`, `TRIANGLE` |
| `SOUR1:FREQ:FIX` | Set frequency | `1000` (1 kHz) |
| `SOUR1:VOLT` | Set amplitude | `1` (1V) |
| `ACQ:DEC` | Set decimation | `64` |
| `ACQ:TRIG:LEV` | Set trigger level | `0` (0V) |
| `ACQ:SOUR1:DATA?` | Query data | Returns data buffer |

### Data Flow Architecture

```
Red Pitaya → SCPI Server → TCP Socket → Python Script → CSV File
                                    ↓
                              Real-time Plot
```

## License

This project is based on Red Pitaya SCPI examples and follows the same licensing terms.

## Support

For issues related to:
- **Red Pitaya SCPI**: Check [Red Pitaya Documentation](https://redpitaya.readthedocs.io/)
- **Python Script**: Review the troubleshooting section above
- **Hardware Setup**: Consult Red Pitaya user manual

## Version History

- **v1.0**: Initial implementation with basic acquisition and plotting
- Current version includes CSV logging and continuous time indexing
