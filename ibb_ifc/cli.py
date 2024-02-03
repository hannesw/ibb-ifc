import argparse
import time
import lib.bbsoft as bbsoft
import lib.quantity_takeoff as qto


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Process IFC file.')
    # Add the argument for the IFC file path
    parser.add_argument('ifc_file_path', type=str, help='Path to the IFC file')
    # Add the argument for skipping processing
    parser.add_argument('--skip-processing',
                        action='store_true', help='Skip the processing step')
    # Parse the arguments
    args = parser.parse_args()
    # Access the value of the ifc_file_path argument
    ifc_file_path = args.ifc_file_path

    # Call bbsoft processing
    if not args.skip_processing:
        start = time.time()
        processed_file_path = bbsoft.process(ifc_file_path)
        end = time.time()
        print(f"BBSoft rocessing time: {round(end - start)} seconds")
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
