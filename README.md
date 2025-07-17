### A Hybrid Model/Data-Driven Solution to Channel, Position and Orientation Tracking in mmWave Vehicular Systems

####   **Description:**
    
This repository contains the code and dataset accompanying the paper 'A Hybrid Model/Data-Driven Solution to Channel, Position and Orientation Tracking in mmWave Vehicular Systems'. It implements a novel hybrid approach combining model-based techniques with data-driven learning for robust position and orientation tracking in challenging mmWave vehicular environments.

#### **Getting Started:**
* **Prerequisites:** Python 3.9+, pip, Git.

#### **Dataset:** `./data/`
    
**Description:** Contains 6 datasets of vehicle trajectories with different starting  positions. 
* `./data/ds#/AP_pos.txt`: the BS 3D position (known; never changes).
* `./data/ds#/UE_pos.txt`: the array 3D position on the vehicle. Every 4 of the positions correspond to the front, back, right, and left arrays of the vehicle.
* `./data/ds#/Info_selected.txt`: Channel information, where each channel associated with one array position contains 25 paths, with columns from the left to the right representing:
    | Channel Phase (deg) | Time of Arrival (ToA) | Channel Gain (dBm) | Downlink Azimuth AoA (deg) | Downlink Elevation AoA (deg) | Azimuth AoD (deg) | Elevation AoD (deg) |
    |---------------------|----------------------|--------------------|----------------------------|------------------------------|-------------------|---------------------|
* `./data/ds#/Num_inters.mat` contains the path order of the paths in the channels 
* `./data/ds#/orisPerShot.mat` determines the vehicle orientation (note there are 4 arrays on a vehicle, so every 4 of the poisions in `./data/ds#/UE_pos.txt` associate with one vehicle orientation).


<!-- * **Access/Download:** Provide instructions on how to obtain the dataset.
        * If it's small, include it directly in the `data/` folder.
        * If large, provide a link to a public repository (e.g., Zenodo, Figshare, university server) or instructions on how to generate/download it.
        * *Crucial:* Describe the structure of the data files (e.g., "The `raw/channel_data.csv` contains time-series channel measurements with columns: `timestamp, Rx_ID, Tx_ID, Path_Loss_dB, AoA_rad, AoD_rad`."). -->
