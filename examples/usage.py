"""
Example usage of NineBit CIQ Python SDK.
"""

import sys
import os
import io
from dotenv import load_dotenv
from typing import Union, IO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ninebit_ciq import NineBitCIQClient, get_sharepoint_configuration, download_file_from_sharepoint  # noqa: E402


load_dotenv()

api_key = "d1b30b1c-b585-4339-9dc5-fc628598117c"

client = NineBitCIQClient(api_key=api_key)


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
            print(f"Ingest_file failed: {error}")
        else:
            print(f"Ingest_file succeeded: {str(data)}")

    # handle_file_ingestion(file="files/geo_chap_8.pdf", callback=on_done)

    # query = "What are land breeze?"
    # response = handle_query_execution(query=query)
    # print(f"Query response is {response}")

    # User handles remote access
    # buffer = download_from_sharepoint(
    #     sharepoint_url="https://company.sharepoint.com/file.docx", access_token="user_access_token"
    # )

    sp_config = get_sharepoint_configuration(
        site_name="KnowledgeCenter", folder="CIQDocs", file_name="BOFA-CC-Elite.pdf"
    )
    remote_file_buffer = download_file_from_sharepoint(sp_config)
    # with open("downloaded_file.pdf", "wb") as f:
    #     f.write(remote_file_buffer)
    handle_file_ingestion(
        file=io.BytesIO(remote_file_buffer), callback=on_done, associated_file_name=sp_config.get("target_file_name")
    )


if __name__ == "__main__":
    main()
