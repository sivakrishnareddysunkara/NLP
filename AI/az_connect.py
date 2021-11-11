import os
import sys
import pathlib
import argparse
import configparser
from config import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.identity import ClientSecretCredential

class AzBlob:
    def __init__(self, cfg):
       self.cfg = cfg 
       self.blob_service_client = BlobServiceClient.from_connection_string(cfg.az_connection_string())
       account_info = self.blob_service_client.get_account_information()
       print('Using Storage SKU: {}'.format(account_info['sku_name']))

    def get_blobs (self):
       container_client = self.blob_service_client.get_container_client("candjobdata")
       for blob in container_client.list_blobs():
          print("Found blob: ", blob.name)


if __name__ == "__main__":

    """
    Main driver program to launch the parallel pipeline for processing 
    github commits. 
    """

    parser = argparse.ArgumentParser(description='rbuddy_data')
    parser.add_argument('-c', '--config', help='Config file path', required=True)

    cfg_parser = configparser.ConfigParser()

    args = parser.parse_args()

    cfg_parser.read(args.config)

    cfg = Config(cfg_parser)

    print(cfg.az_connection_string())

    AZ = AzBlob(cfg)
    AZ.get_blobs()


