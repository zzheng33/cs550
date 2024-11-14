import os
import subprocess
import shutil

# Base directory containing the trace folders
TRACE_DIR = "/home/zzheng33/codes-dev/traces"

# Binary location
BIN = "/home/zzheng33/codes-dev/codes/build/src/network-workloads/model-net-mpi-replay"
config_path="/home/zzheng33/cs550/conf/modelnet-mpi-test-dfly.conf"

workload_conf = ["/home/zzheng33/cs550/conf/workloads_amg_minife.conf"]
alloca_conf = ["/home/zzheng33/cs550/conf/allocation_amg_minife.conf"]



# List of specific folders to process
folders_to_process = [
    "amg_216",
    "miniamr_64",
    "minife_18",
    "MultiGrid_125",
    "CR_100"
]





# MPI execution settings
RANKS = 4

# Iterate over the two configurations and their respective suffixes
for i in range(len(workload_conf)):
    WORKLOAD = workload_conf[i]
    ALLOC = alloca_conf[i]
    # Build the command for mpirun
    command = [
        BIN,
        "--sync=1",
        "--workload_type=dumpi",
        f"--workload_conf_file={WORKLOAD}",
        f"--alloc_file={ALLOC}",
        "--extramem=500000",
        f"--lp-io-dir=test",
        "--lp-io-use-suffix=1",
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

