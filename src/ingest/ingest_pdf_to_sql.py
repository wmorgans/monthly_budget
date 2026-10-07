import argparse
import logging
import os
import tabula
import pandas as pd

import bank_parser

logging.basicConfig(level=logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Ingest PDF to SQL")
    parser.add_argument("--pdf_directory", type=str, required=True, help="Path to the PDF directory")
    parser.add_argument("--ingested_file_list", type='str', required=True, help="Path to the ingested file list")
    return parser.parse_args()

def pdfs_to_dataframe(pdf_path):
    # Read the PDF file and extract tables
    
    
    parser = bank_parser.TescoParser()
    dfs_to_join = []
    for pdf in pdf_path:
        logging.info(f"Processing PDF: {pdf}")
        df = parser.parse(pdf)
        logging.info(f"DataFrame shape: {df.shape}")
        logging.info(f"DataFrame head:\n{df.head()}")

    joint_df = pd.concat(dfs_to_join, ignore_index=True)

def main():
    args = parse_arguments()

    # read ingested files if provided
    logging.info("Reading ingested files...")

    if args.ingested_file_list and os.path.exists(args.ingested_file_list):
        with open(args.ingested_file_list, 'r') as f:
            ingested_files = [line.strip() for line in f.readlines()]
    else:
        ingested_files = []
        logging.info("No ingested file list provided.")

    f = []
    for (dirpath, dirnames, filenames) in os.walk(args.pdf_directory):
        f.extend(filenames)
        break

    logging.info(f"Found {len(f)} files in the PDF directory.")

    # filter out already ingested files
    files_to_ingest = [file for file in f if file not in ingested_files]

    logging.info(f"Found {len(files_to_ingest)} files to ingest.")

    pdfs_to_dataframe(files_to_ingest)



if __name__ == "__main__":

    main()
