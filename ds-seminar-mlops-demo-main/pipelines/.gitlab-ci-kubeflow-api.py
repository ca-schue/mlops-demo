import kfp
import sys

trigger = sys.argv[1]
timestamp = sys.argv[2]

run_name = "[" + trigger + "] at [" + timestamp + "]"
print("Current run: " + run_name)

client = kfp.Client(host='http://<Public Kubeflow API Endpoint>/')
client.create_run_from_pipeline_package('pipeline.yaml', arguments={"trigger":trigger, "timestamp":timestamp}, run_name=run_name, enable_caching=False)