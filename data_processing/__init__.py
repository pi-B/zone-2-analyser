import pathlib
import logging
from datetime import datetime as dt
from datetime import date
import csv
import string
import pandas
from typing import Tuple

logger = logging.getLogger(__name__)

class DataManager:
    file: str
    raw_data: bytearray
    zone_2_limits : Tuple[int,int]

    def __init__(self,path: str, limits: Tuple[int,int]):
        if not pathlib.Path(path).exists():
            logger.critical("Could not find the data file, exiting")
            exit(0)
        if not is_csv(path):
            logger.critical("Could not validate the file passed is a CSV, exiting")
            exit(0)
        self.file = path
        if limits[0] is None or limits[1] is None :
            logger.critical("Zone 2 values are badly formatted : " + limits )
            logger.critical("Exiting...")
            exit(0)
        self.zone_2_limits = limits

    def parse_data(self, start_date: date, end_date: date ):
        with open(self.file, 'r') as file :
            dataset = pandas.read_csv(file)
            for column_name, column in dataset.transpose().iterrows():
                if column_name not in ("Allure moyenne","Durée","Fréquence cardiaque moyenne","Date"):
                    del dataset[column_name]
            file.close()

        # Since the data is not typed in the CSV file we need to assign them 
        print(dataset["Date"])
        dataset["Allure moyenne"] = pandas.to_timedelta("00:" + dataset["Allure moyenne"])
        dataset["Date"] = pandas.to_datetime(dataset["Date"], format="%Y-%m-%d %H:%M:%S")
        dataset = dataset.sort_values("Date",ascending=True)

        dataset = self.remove_outside_z2_data(dataset)
        # dataset = dataset.sort_values("Allure moyenne", ascending=True)
        return dataset    
        
    def remove_outside_z2_data(self, dataset: pandas.DataFrame):
        for index, value in dataset["Fréquence cardiaque moyenne"].items():
            value = int(value)
            if value < self.zone_2_limits[0] or value > self.zone_2_limits[1]:
                dataset = dataset.drop(index=index)
        
        return dataset
        
def is_csv(file) :
    try:
        with open(file, newline='') as csvfile:
            start = csvfile.read(4096)

            # isprintable does not allow newlines, printable does not allow umlauts...
            if not all([c in string.printable or c.isprintable() for c in start]):
                return False
            dialect = csv.Sniffer().sniff(start)
            return True
    except csv.Error as e:
        # Could not get a csv dialect -> probably not a csv.
        logger.error(f"{e=}")
        return False
