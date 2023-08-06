

class NormalizeDates():

    def normalize(self, data):
        if not isinstance(data, str):
            raise ValueError("Invalid date type, send strings only")
        result = self.format_date(data)
        # 1990-03-20

        return result

    def format_date(self, data):

        # 20-03-1990
        try:
            if "-" in data:
                date_split = data.split("-")
                data = f"{date_split[2]}-{date_split[1]}-{date_split[0]}"
        except:
            pass

        # 20/03/1990
        try:
            if "/" in data:
                date_split = data.split("/")
                data = f"{date_split[2]}-{date_split[1]}-{date_split[0]}"
        except:
            pass

        # 20 de março de 1990
        try:
            if "de" in data:
                date_split = data.split(" de ")
                month = self.__get_month_number(date_split[1].lower())
                data = f"{date_split[2]}-{month}-{date_split[0]}"
        except:
            pass

        # March 20th, 1990
        try:
            if "," in data:
                date_split = data.split(" ")
                day = self.__get_month_day(date_split[1])
                month = self.__get_month_number(date_split[0].lower())
                data = f"{date_split[2]}-{month}-{day}"
        except:
            pass

        return data

    def __get_month_day(self, day):

        if 'st' in day:
            __day = day.split('st')
            if __day[0] == '31':
                new_day = f'{__day[0]}'
            else:
                new_day = f'0{__day[0]}'
        elif 'nd' in day:
            __day = day.split('nd')
            new_day = f'0{__day[0]}'
        elif 'rd' in day:
            __day = day.split('rd')
            new_day = f'0{__day[0]}'
        else:
            __day = day.split('th')
            new_day = __day[0]

        return new_day

    def __get_month_number(self, month):
        if 'janeiro' in month or 'january' in month:
            month_number = '01'
        elif 'fevereiro' in month or 'february' in month:
            month_number = '02'
        elif 'março' in month or 'march' in month:
            month_number = '03'
        elif 'abril' in month or 'april' in month:
            month_number = '04'
        elif 'maio' in month or 'may' in month:
            month_number = '05'
        elif 'junho' in month or 'june' in month:
            month_number = '06'
        elif 'julho' in month or 'july' in month:
            month_number = '07'
        elif 'agosto' in month or 'august' in month:
            month_number = '08'
        elif 'setembro' in month or 'september' in month:
            month_number = '09'
        elif 'outubro' in month or 'october' in month:
            month_number = '10'
        elif 'novembro' in month or 'november' in month:
            month_number = '11'
        elif 'dezembro' in month or 'december' in month:
            month_number = '12'
        else:
            raise ValueError("Invalid month")

        return month_number
