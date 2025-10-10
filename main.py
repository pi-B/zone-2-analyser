from garth import Client as GarthClient
import tomllib
import logging
import os
from data_processing import DataManager
from graphs import GraphManager
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

class GarminAPIManager:
    user: str
    password: str
    client: GarthClient

    def connectGarminClient(self):
        logger.info("Connecting to Garmin API")
        res = self.client.login(self.user,self.password)
        print(res)

def main():
    logging.basicConfig(level=logging.INFO)
    conf_file = open("./conf.toml", "r")
    conf = tomllib.loads(conf_file.read())

    data_conf = conf.get("data")
    if "data" in conf: 
        if conf["data"]["path"] in (None, "") :
            # retrieve_data(conf) # NOT USED ATM BC GARTH IS HAVING TROUBLE HANDLING PASSWORD WITH SPECIAL CHAR
            print("NOT IMPLEMENTED")
        else :
            data = DataManager(conf["data"]["path"],(conf["data"]["zone_2_low"],conf["data"]["zone_2_high"]))
            end_date = dt.now()
            if "duration" in conf["data"]:
                duration = int(conf["data"]["duration"])
            start_date = end_date - relativedelta(months=duration) 
            print("Start date : " + dt.strftime(start_date, "%d/%m/%Y") )
            dataset = data.parse_data(start_date,end_date)
            print(dataset)
    else :
        logger.critical("Missing data section in conf")

    graph = GraphManager(dataset)
    graph.create_graph()
    graph.display_graph()

def retrieve_data(conf: dict):
    
    garm_mng = GarminAPIManager()
    garm_mng.user = conf["garmin"]["user"]
    garm_mng.password = conf["garmin"]["password"]
    garm_mng.client = GarthClient()
    logger.info("Creating Garmin Client")
    garm_mng.connectGarminClient()

if __name__ == '__main__':
    main()
