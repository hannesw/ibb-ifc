import click
import time
import lib.bbsoft as bbsoft
import lib.quantity_takeoff as qto


@click.command()
@click.argument('ifc_file_path', type=click.Path(exists=True))
@click.option('--skip-processing', is_flag=True, help='Skip the processing step if file was already processed.)')
def main(ifc_file_path, skip_processing):
    # check if file has the correct ending
    if not ifc_file_path.endswith(".ifc"):
        raise ValueError("Invalid file format. Only IFC files are supported.")

    # Call bbsoft processing
    if not skip_processing:
        start = time.time()
        processed_file_path = bbsoft.process(ifc_file_path)
        end = time.time()
        print(f"BBSoft processing time: {round(end - start)} seconds")
    else:
        processed_file_path = ifc_file_path
        print("Skipping processing")

    # Call quantity takeoff
    start = time.time()
    qto.get(processed_file_path)
    end = time.time()
    print(f"Quantity takeoff time: {round(end - start)} seconds")


if __name__ == '__main__':
    main()
