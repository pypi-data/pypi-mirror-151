import os
import datetime


class Logger:
    """
    Logger Class
    """
    def __init__(self, visible):
        """
        Initialise the Logger Class
        :param visible: Statements should be printed or not.
        """
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.MAGENTA = '\033[95m'
        self.CYAN = '\033[96m'
        self.END = '\033[0m'
        self.visible = visible


    def log(self, log_data):
        """
        Main Logging Logic
        :param log_data: Data to be written.
        :return: None
        """
        try:
            log_folder = "./logs"
            if not os.path.exists(log_folder):
                os.mkdir(log_folder)

            log_file = os.path.join(log_folder, str(datetime.datetime.now().date())+".txt")

            with open(log_file, "a") as file:
                file.write(log_data + "\n")
                file.close()
        except Exception as E:
            print(E)

    def info(self, *args):
        """
        Information to be written in logs
        :param args: data to write
        :return: NONE
        """
        self.log("INFO "+ str(datetime.datetime.now()) + " " + " ".join([str(i) for i in args]))
        if self.visible:
            print("INFO", self.BLUE + " ".join([str(i) for i in args]) + self.END)

    def debug(self, *args):
        """
        Debug data to be written in logs
        :param args: data to write
        :return: NONE
        """
        self.log("DEBUG "+ str(datetime.datetime.now()) + " " + " ".join([str(i) for i in args]))
        if self.visible:
            print("DEBUG ", self.CYAN + " ".join([str(i) for i in args]) + self.END)

    def warning(self, *args):
        """
        Warning data to be written in logs
        :param args: data to write
        :return: NONE
        """
        self.log("WARNING "+ str(datetime.datetime.now()) + " " + " ".join([str(i) for i in args]))
        if self.visible:
            print("WARNING ", self.RED + " ".join([str(i) for i in args]) + self.END)

    def show(self, *args):
        """
        Data to be shown in terminal
        :param args: data to write
        :return: NONE
        """
        print(" - ", self.GREEN + " ".join([str(i) for i in args]) + self.END)

    def scrape_data(self, *args):
        """
        Scraping Info to be written in logs
        :param args: data to write
        :return: NONE
        """
        self.log("SCRAPER " + str(datetime.datetime.now()) + " " + " ".join([str(i) for i in args]))
        if self.visible:
            print("SCRAPER ", self.MAGENTA + " ".join([str(i) for i in args]) + self.END)

    def error_log(self, errval, err):
        """
        Error Details to be written in logs
        :param args: data to write
        :return: NONE
        """
        error_folder = "./error_details"
        if not os.path.exists(error_folder):
            os.mkdir(error_folder)

        error_file = os.path.join(error_folder, str(datetime.datetime.now().date()) + "_errror_Details.txt")

        with open(error_file, "a") as file:
            file.write("{} error = {}".format(errval, err) + "\n")
            file.close()
        if self.visible:
            print(self.CYAN + "Error Details Updated." + self.END)

    def delete_log(self):
        """
        Delete all Logs file
        :return: NONE
        """
        try:
            if os.path.isfile(os.path.join("./logs", str(datetime.datetime.now().date())+".txt")):
                os.remove(os.path.join("./logs", str(datetime.datetime.now().date())+".txt"))
                self.show("Log File Deleted")
        except:
            self.show("Log File not Present")

    def data_log(self, *args):
        """
        Enter data in a text file generation will be space seperated CSV file.
        Example usage:
            log = Logger()
            log.data_log(data1, data2, data3)
        Output:
            each line in the data_log .txt file will be
            data1 data2 data3
        :params args: data to be written
        :return: None
        """
        data_folder = "./data_log"
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)

        data_file = os.path.join(data_folder, str(datetime.datetime.now().date()) + "_data_log.txt")

        with open(data_file, "a") as file:
            file.write(" ".join([str(i) for i in args]) + "\n")
            file.close()
        if self.visible:
            print(self.CYAN + "Data Log Updated." + self.END)
