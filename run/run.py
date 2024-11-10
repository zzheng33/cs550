import os
import subprocess
import shutil

# Base directory containing the trace folders
TRACE_DIR = "/home/zzheng33/codes-dev/traces"

# Binary location
BIN = "/home/zzheng33/codes-dev/codes/build/src/network-workloads/model-net-mpi-replay"

# # Configuration files for two rounds
# CONFIGS = [
#     ("/home/zzheng33/conf/modelnet-mpi-test-dfly-amg-1728.conf", "dfly"),
#     ("/home/zzheng33/conf/modelnet-mpi-test-fattree.conf", "fattree")
# ]


# CONFIGS = [
#      ("/home/zzheng33/conf/modelnet-mpi-test-fattree.conf", "fattree")
# ]

CONFIGS = [
    ("/home/zzheng33/conf/modelnet-mpi-test-dfly-1056.conf", "dfly")
    
]

# List of specific folders to process
folders_to_process = [
    "amg_27",
    "amg_216",
    "miniamr_64",
    "minife_18",
    "MultiGrid_125",
    "CR_100"
]

folders_to_process = [
    "MultiGrid_1000"
]


# MPI execution settings
RANKS = 80

# Iterate over the two configurations and their respective suffixes
for config_path, suffix in CONFIGS:
    # Iterate over the specific folders
    for app_dir in folders_to_process:
        app_path = os.path.join(TRACE_DIR, app_dir)

        # Ensure the folder exists
        if not os.path.isdir(app_path):
            continue

        # Get the list of files, select the first one, and generate the workload prefix
        files = sorted(os.listdir(app_path))
        if files:
            first_file = files[0]
            workload_prefix = first_file.rsplit('-', 1)[0] + '-'
            WORKLOAD = os.path.join(app_path, workload_prefix)

            # Extract the application number from the folder name (e.g., "amg_27" -> 27)
            app_number = int(app_dir.split('_')[1])
            NUM_TRACE = app_number  # Use this number for --num_net_traces

            # Set the lp-io-dir with the appropriate suffix (e.g., "amg_27_dfly" or "amg_27_fattree")
            lp_io_dir = f"{app_dir}_{suffix}"

            # Build the command for mpirun
            command = [
                "mpirun", "-np", str(RANKS), BIN,
                "--sync=3",
                f"--num_net_traces={NUM_TRACE}",
                "--workload_type=dumpi",
                f"--workload_file={WORKLOAD}",
                f"--lp-io-dir={lp_io_dir}",
                "--lp-io-use-suffix=1",
                "--extramem=500000",
                config_path
            ]
            try:
                
                subprocess.run(command, check=True)

            except subprocess.CalledProcessError as e:
      
                continue  # Skip to the next workload


            # Clean up .bin and .meta files after execution
            for file in os.listdir('.'):
                if file.endswith(".bin") or file.endswith(".meta"):
                    os.remove(file)
                  

            # Rename any output folders that have extra suffixes
            for folder in os.listdir('.'):
                if folder.startswith(lp_io_dir) and folder != lp_io_dir:
                    shutil.move(folder, lp_io_dir)

