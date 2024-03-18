import click
import time
import lib.bbsoft as bbsoft
import lib.quantity_takeoff as qto
import lib.model_checker as model_checker


@click.command()
@click.option('--checks', is_flag=True, help="Run checks on the IFC file")
@click.option('--quantity-takeoff', is_flag=True, help="Also create a quantity takeoff")
@click.argument('ifc_file_path', type=click.Path(exists=True))
def main(ifc_file_path, checks, quantity_takeoff):
    # check if file has the correct ending
    if not ifc_file_path.endswith(".ifc"):
        raise ValueError("Invalid file format. Only IFC files are supported.")

    # Call bbsoft processing
    start = time.time()
    processed_file_path = bbsoft.process(ifc_file_path)
    end = time.time()
    print(f"BBSoft processing time: {round(end - start)} seconds")

    # Call checks
    if checks:
        start = time.time()
        model_checker.run(processed_file_path)
        end = time.time()
        print(f"Checks time: {round(end - start)} seconds")

    # Call quantity takeoff
    if quantity_takeoff:
        start = time.time()
        qto.get(processed_file_path)
        end = time.time()
        print(f"Quantity takeoff time: {round(end - start)} seconds")


if __name__ == '__main__':
    main()
