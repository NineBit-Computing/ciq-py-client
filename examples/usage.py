"""
Example usage of NineBit CIQ Python SDK.
"""

import sys
import os
import io
from typing import Union, IO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ninebit_ciq import NineBitCIQClient, get_sharepoint_configuration, download_file_from_sharepoint  # noqa: E402

ENABLE_SHAREPOINT_TEST = False
ENABLE_FILE_INGESTION = True
ENABLE_QUERY_TEST = True

try:
    api_key = os.getenv("API_KEY") or "ci_agent_datahub_access"
    client = NineBitCIQClient(api_key=api_key)
except Exception as e:
    print(f"Error while setting up CIQ client {e}")
    sys.exit(1)


def handle_file_ingestion(file: Union[str, IO[bytes]], associated_file_name=None, callback=None):
    print("Begin: handle_file_ingestion")
    client.ingest_file(file=file, callback=callback, associated_file_name=associated_file_name)
    print("Success: handle_file_ingestion")


def handle_query_execution(query: str, callback=None):
    print("Begin: handle_query_execution")
    response = client.rag_query(query=query)
    print("Success: handle_query_execution")
    return response


def main():
    def on_done(error, data):
        if error:
            print(f"Error: Ingest_file failed: {error}")
            sys.exit(1)
        else:
            print(f"Ingest_file succeeded: {str(data)}")

    try:
        if ENABLE_FILE_INGESTION is True:
            handle_file_ingestion(file="examples/files/geo_chap_9.pdf", callback=on_done)

        if ENABLE_SHAREPOINT_TEST is True:
            sp_config = get_sharepoint_configuration(
                site_name="KnowledgeCenter", folder="CIQDocs", file_name="BOFA-CC-Elite.pdf"
            )
            remote_file_buffer = download_file_from_sharepoint(sp_config)
            handle_file_ingestion(
                file=io.BytesIO(remote_file_buffer),
                callback=on_done,
                associated_file_name=sp_config.get("target_file_name"),
            )

        if ENABLE_QUERY_TEST is True:
            query = "What are land breeze?"
            response = handle_query_execution(query=query)
            print(f"Query response is {response}")

    except Exception as ex:
        print(f"Error while performing main execution: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()
