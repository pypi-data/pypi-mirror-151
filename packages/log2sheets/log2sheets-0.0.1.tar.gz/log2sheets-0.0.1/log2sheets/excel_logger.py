import os
import xlsxwriter
from datetime import datetime
import pandas as pd


class ExcelLogger:
    row = {}

    def __init__(
        self,
        logger_path: str,
        logger_name: str,
        sheet_name: str = "Default Logger",
        overwrite: bool = False,
        datetime_format="%A %d-%m-%Y, %H:%M:%S"
        # file_path: str = None,
        # use_colors: bool = False,
    ) -> None:
        self.logger = os.path.join(logger_path, logger_name + ".xlsx")
        if not overwrite and os.path.exists(self.logger):
            os.rename(
                self.logger,
                os.path.join(
                    logger_path,
                    logger_name + "_" + str(datetime.timestamp(datetime.now())),
                )
                + ".old.xlsx",
            )

        self.current_sheet = sheet_name
        self.wb = xlsxwriter.Workbook(self.logger)
        self.ws = self.wb.get_worksheet_by_name(sheet_name)

        if self.ws is None:
            self.ws = self.wb.add_worksheet(sheet_name)
            self.row[sheet_name] = 0
        else:
            self.row[sheet_name] = len(
                pd.read_excel(self.logger, sheet_name=sheet_name)
            )

        self.formatter_dict = {"datetime": 0, "type": 1, "message": 2}
        self.datetime_format = datetime_format

    def formatter(self, list):
        formatter_dict = {
            "datetime": 0,
            "type": 1,
        }
        for i, value in enumerate(list):
            formatter_dict[value] = i + 2
        self.formatter_dict = formatter_dict

    def switch(self, sheet_name: str) -> None:
        self.ws = self.wb.get_worksheet_by_name(sheet_name)
        self.current_sheet = sheet_name
        if self.ws is None:
            self.ws = self.wb.add_worksheet(sheet_name)
            self.row[sheet_name] = 0

    # def color_map(self, colors: dict) -> None:
    # TODO: Implement color_map
    #     pass

    def log_data(self, data: dict, type) -> None:
        self.ws.write(
            self.row[self.current_sheet],
            0,
            datetime.now().strftime(self.datetime_format),
        )  # write date_time
        self.ws.write(self.row[self.current_sheet], 1, type)  # write type
        for col, value in data.items():
            if self.formatter_dict.get(col, None) is None:
                self.formatter_dict[col] = len(self.formatter_dict)
            self.ws.write(self.row[self.current_sheet], self.formatter_dict[col], value)
        self.row[self.current_sheet] += 1

    def log_message(self, message: str, type: str) -> None:
        self.ws.write(
            self.row[self.current_sheet],
            0,
            datetime.now().strftime(self.datetime_format),
        )  # write date_time
        self.ws.write(self.row[self.current_sheet], 1, type)  # write type
        self.ws.write(
            self.row[self.current_sheet],
            self.formatter_dict.get("message", len(self.formatter_dict)),
            str(message),
        )
        self.row[self.current_sheet] += 1

    def ok(self, message: str) -> None:
        self.log_message(message, "OK")

    def ok_data(self, data: dict) -> None:
        self.log_data(data, "OK")

    def info(self, message: str) -> None:
        self.log_message(message, "INFO")

    def info_data(self, data: dict) -> None:
        self.log_data(data, "INFO")

    def warn(self, message: str) -> None:
        self.log_message(message, "WARN")

    def warn_data(self, data: dict) -> None:
        self.log_data(data, "WARN")

    def error(self, message: str) -> None:
        self.log_message(message, "ERROR")

    def error_data(self, data: dict) -> None:
        self.log_data(data, "ERROR")

    def flush(self) -> None:
        self.wb.close()
