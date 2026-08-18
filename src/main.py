import argparse

from src.linkedin import write_csv


def main():
    parser = argparse.ArgumentParser(
        description="Lead generation tool written in python"
    )
    parser.add_argument(
        "-j",
        "--job",
        type=str,
        required=True,
        help="The job title for the target leads",
    )
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        required=True,
        help="The target location of the leads",
    )
    args = parser.parse_args()
    job_title: str = args.job
    location: str = args.location
    write_csv(job_title, location)


if __name__ == "__main__":
    main()
