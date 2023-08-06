
from datetime import date


class ConvertDates():

    def __init__(self, format):
        if not format:
            raise ValueError('Format not defined')
        self.__format = format

    def convert(self, data):
        if not isinstance(data, str):
            raise ValueError("Invalid date type, send strings only")

        data = self.__verify_date(data)

        if self.__format == "/br":
            result = self.format_date_br(data[0], int(data[1]), int(data[2]))
        elif self.__format == "full_br":
            result = self.format_date_full_br(
                data[0], int(data[1]), int(data[2]))
        elif self.__format == "full_us":
            result = self.format_date_full_us(
                data[0], int(data[1]), int(data[2]))
        else:
            raise ValueError('Invalid format')

        return result

    def __verify_date(self, data):
        data = data.split('-')

        if data[2][0] == '0':
            data[2] = data[2].replace("0", "")
        if data[1][0] == '0':
            data[1] = data[1].replace("0", "")

        try:
            date(int(data[0]), int(data[1]), int(data[2]))
        except:
            raise('Invalid date')
        return data

    def format_date_br(self, year, month, day):
        if day < 1 or day > 31:
            raise ValueError("Insert a valid day")
        if day >= 1 and day <= 9:
            day = f'0{day}'
        if month >= 1 and month <= 9:
            month = f'0{month}'
        return f"{day}/{month}/{year}"

    def format_date_full_br(self, year, month, day):
        print(type(day))
        if day < 1 or day > 31:
            raise ValueError("Insert a valid day")
        return f"{day} de {self.__get_month_name(month, 'br')} de {year}"

    def format_date_full_us(self, year, month, day):
        __day = self.__get_us_day(day)
        __month = self.__get_month_name(month, 'us')
        upper_month = str(__month).title()

        return f"{upper_month} {__day}, {year}"

    def __get_us_day(self, day):

        if day < 1 or day > 31:
            raise ValueError("Insert a valid day")

        if day == 31 or day == 1:
            __day = f"{day}st"
        elif day == 2:
            __day = f'{day}nd'
        elif day == 3:
            __day = f'{day}rd'
        else:
            __day = f"{day}th"

        return __day

    def __get_month_name(self, month, format):
        if format == "br":
            if month == 1:
                __month = 'janeiro'
            elif month == 2:
                __month = 'fevereiro'
            elif month == 3:
                __month = 'março'
            elif month == 4:
                __month = 'abril'
            elif month == 5:
                __month = 'maio'
            elif month == 6:
                __month = 'junho'
            elif month == 7:
                __month = 'julho'
            elif month == 8:
                __month = 'agosto'
            elif month == 9:
                __month = 'setembro'
            elif month == 10:
                __month = 'outubro'
            elif month == 11:
                __month = 'novembro'
            elif month == 12:
                __month = 'dezembro'
            else:
                raise ValueError('Invalid Month')
        elif format == "us":
            if month == 1:
                __month = 'January'
            elif month == 2:
                __month = 'February'
            elif month == 3:
                __month = 'March'
            elif month == 4:
                __month = 'April'
            elif month == 5:
                __month = 'May'
            elif month == 6:
                __month = 'June'
            elif month == 7:
                __month = 'July'
            elif month == 8:
                __month = 'August'
            elif month == 9:
                __month = 'September'
            elif month == 10:
                __month = 'October'
            elif month == 11:
                __month = 'November'
            elif month == 12:
                __month = 'December'
            else:
                raise ValueError('Invalid Month')
        else:
            raise ValueError('Invalid format')

        return __month
