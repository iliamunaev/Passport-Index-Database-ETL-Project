from etl.etl import extract, transform, load, log_progress


def main():
    url = 'https://www.passportindex.org/byRank.php'

    log_progress("ETL Job Started.")
    log_progress("Extract phase Started.")

    extracted_data = extract(url)
    if extracted_data is not None:

        log_progress("Extract phase Ended.")
        log_progress("Transform phase Started.")

        transformed_data = transform(extracted_data)
        if transformed_data is not None:

            log_progress("Transform phase Started.")
            log_progress("Load phase Started.")

            load(transformed_data)

            log_progress("Load phase Ended.")
            log_progress("ETL process completed successfully.")

        else:
            log_progress("Error in transformation. ETL process aborted.")
    else:
        log_progress("Error in extraction. ETL process aborted.")


if __name__ == "__main__":
    main()
