import sys


class NetworkSecurityException(Exception):
    """
    Custom Exception class for the Network Security project.
    Provides detailed error information including file name and line number.
    """

    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(str(error_message))

        self.error_message = self._get_detailed_error_message(
            error_message, error_detail
        )

    def _get_detailed_error_message(self, error_message: Exception, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown"
            line_number = "Unknown"

        return (
            f"Error occurred in file: {file_name}, "
            f"line: {line_number}, "
            f"message: {error_message}"
        )

    def __str__(self):
        return self.error_message
