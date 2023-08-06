# import gspread


class GSheetLogger:
    def __init__(self, name: str, sheet_name: str, sheet_id: int) -> None:
        self.name = name

    def formatter(self):
        pass

    def use_colors(self, colors: dict) -> None:
        pass

    def ok(self, message: str) -> None:
        pass

    def info(self, message: str) -> None:
        pass

    def warn(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass

    def log(self, message: str) -> None:
        pass

    def flush(self) -> None:
        pass
