import os
import argparse
from core import Parser, Process


def parse_arguments():
    """Command line arguments parser"""
    parser = argparse.ArgumentParser(description="Genome Regions - Coding Project")
    parser.add_argument("-in", "--input_dir", default="Regions_Large.txt", help="Input regions file. Optional argument default is 'Regions_Large.txt'")
    parser.add_argument("-part1", action="store_true", help="Return result file of part1 task")
    parser.add_argument("-part2", action="store_true", help="Return result file of part2 Task")
    return parser


def main():
    """Application manage function"""
    parser_args = parse_arguments()
    args = parser_args.parse_args()

    # Check if exist input directory
    if not(os.path.exists(args.input_dir)):
        raise FileNotFoundError(f'{args.input_dir} file does not exists')

    parser = Parser(args.input_dir)
    process = Process(parser.regions, parser.segments)
    
    if args.part1:
        output_file_name = os.path.splitext(args.input_dir)[0] + "_part1_result.txt"
        process.part1_task()
        process.export_data(process.regions, output_file_name)

    if args.part2:
        output_file_name = os.path.splitext(args.input_dir)[0] + "_part2_result.txt"
        process.part2_task()
        process.export_data(process.segments, output_file_name)

if __name__ == "__main__":
    main()
    