import argparse
import sys
from DatasetProcessor import DatasetManager


def main():
    parser = argparse.ArgumentParser(description="EDA tool")

    subparsers = parser.add_subparsers(dest="command")

    # Настроим подкоманду analyze_dataset
    dataset_parser = subparsers.add_parser("analyze_dataset", help="Analyze dataset")
    dataset_parser.add_argument("--config", required=True, help="Path to the config file")

    # Настроим подкоманду analyze_metafile
    metafile_parser = subparsers.add_parser("analyze_metafile", help="Analyze metafile")
    metafile_parser.add_argument("--json", required=True, help="Path to the JSON metafile")
    metafile_parser.add_argument("--output", required=True, help="Path to save the report")

    # Парсим аргументы командной строки
    args = parser.parse_args()
    if args.command == 'analyze_dataset':
        print("Analyzing dataset")
        manager = DatasetManager.DatasetManager(config_path=args.config)
        manager.run()
        print(f"The report was successfully saved in your output path")
    elif args.command == 'analyze_metafile':
        print("Build report by metafile")
        manager = DatasetManager.DatasetManager(json_filepath=args.json, save_filepath=args.output)
        manager.run_from_json()
        print(f"The report was successfully saved in {args.output}")
    else:
        parser.print_help()
        sys.exit(1)



if __name__ == "__main__":
    main()







