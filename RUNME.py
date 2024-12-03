import os
import subprocess
import sys

if not os.path.exists('Data/data_lake_raw/RDC_Inventory_Core_Metrics_Zip_History.csv'):
    print("The raw data is not downloaded. Please follow instructions \
          in the README and place the data in the Data/data_lake_raw/ subdirectory")

def create_and_activate_env(env_name):
    subprocess.call([sys.executable, "-m", "venv", env_name])

    if sys.platform == "win32":
        activate_script = os.path.join(env_name, "Scripts", "activate")
    else:
        activate_script = os.path.join(env_name, "bin", "activate")
    
    return activate_script

def install_requirements(env_activate_script, requirements_file):
    subprocess.call(f"source {env_activate_script} && pip install -r {requirements_file}", shell=True)

def run_notebook(env_activate_script, notebook_path):
    subprocess.call(f"source {env_activate_script} && jupyter nbconvert --to notebook --execute {notebook_path}", shell=True)


env_name = "MGT_8203_GROUP_21" 
requirements_file = "requirements.txt"  
notebooks = ["Code/data_eng/ETL.ipynb", "Code/models/reggression.ipynb", "Code/models/regression_tree.ipynb","/home/ivanbliminse/Documents/Team-21/Code/models/ann.ipynb"]  

# Create and activate the environment
env_activate_script = create_and_activate_env(env_name)

print("created env")

# Install requirements
install_requirements(env_activate_script, requirements_file)

print("installed all the required dependencies")

# Run notebooks
for notebook in notebooks:
    run_notebook(env_activate_script, notebook)
    print(f"ran notebook {notebook}")
