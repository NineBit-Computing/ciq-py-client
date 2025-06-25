"""
Example usage of NineBit CIQ Python SDK.
"""

import threading
from ninebit_ciq import NineBitCIQClient


def on_workflow_complete(result):
    print("Workflow finished with status:")
    print(result)


def wait_for_completion_in_background(client, wf_id, callback):
    try:
        final_status = client.wait_for_completion(wf_id)
        callback(final_status)
    except Exception as e:
        print(f"Error during workflow execution: {e}")


def main():
    base_url = "https://api.ciq.ninebit.in"
    api_key = "YOUR_API_KEY"

    client = NineBitCIQClient(base_url=base_url, api_key=api_key)

    # Get design time workflow JSON
    workflow = client.get_design_time_workflow()
    print("Design Time Workflow JSON:")
    print(workflow)

    # Trigger a workflow with sample data
    sample_data = {"some": "data"}
    wf_id = client.trigger_workflow(sample_data)
    print(f"Triggered workflow with ID: {wf_id}")

    # Check workflow status
    status = client.get_workflow_status(wf_id)
    print(f"Status of workflow {wf_id}:")
    print(status)

    # Start background thread to wait for completion
    thread = threading.Thread(
        target=wait_for_completion_in_background,
        args=(client, wf_id, on_workflow_complete),
    )
    thread.start()

    # Meanwhile, continue doing other things
    print("Main thread is free to do other tasks...")


if __name__ == "__main__":
    main()
