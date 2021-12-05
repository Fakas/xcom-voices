import logging
import subprocess
from pathlib import Path
import pandas


def main():
    audios = Path(r"G:\Modding\XCOM 2\audios")
    vgmstream = Path(r"G:\Modding\vgmstream\test.exe")
    index = Path(r"G:\Modding\XCOM 2\soldier-voices-cleaned.csv")
    csv = pandas.read_csv(index)

    converter = Converter(vgmstream)
    for _, row in csv.iterrows():
        path = audios / row["Generated audio file"]
        output = audios / (row["Name"] + ".wav")
        try:
            path = path.resolve(strict=True)
        except FileNotFoundError:
            logging.error("File not found: %s", path)
            continue
        converter.convert(path, output=output)


class Converter:
    def __init__(self, path: Path):
        self.converter_path = path

    def convert(self, path: Path, output: Path = None):
        output = str(output) if output else path.with_suffix(".wav")
        path = str(path)
        process = subprocess.run([self.converter_path, path, output], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if process.returncode:
            logging.error(process.stderr)
        else:
            Path(path + ".wav").rename(output)
            print(f"{path} -> {output}")


if __name__ == "__main__":
    main()
