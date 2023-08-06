import re


class NormalizeCurrency():

    def __init__(self, locale="pt_BR"):
        self.__locale = locale

    # R$ 5.000,00
    # R$5000,00
    # R$5,000,000
    # $5000.00

    def normalize_currency(self, value):
        new_value = self.__normalize_currency(value)
        return new_value

    def convert_currency(self, value):
        if self.__locale == "pt_BR":
            return self.__convert_brazilian_currency(value, self.__locale)
        elif self.__locale == "en_US":
            return self.__convert_us_currency(value, self.__locale)
        else:
            raise ValueError("Locale not found or not supported")

    def __convert_brazilian_currency(self, value, sufix):
        __format = "{:0,.2f}"
        if sufix:
            __format = "R$ {:0,.2f}"

        new_value = __format.format(value)
        new_value = new_value.replace(".", "v")
        new_value = new_value.replace(",", ".")
        new_value = new_value.replace("v", ",")

        return new_value

    def __convert_us_currency(self, value, sufix):
        __format = "{:0,.2f}"
        if sufix:
            __format = "$ {:0,.2f}"
        new_value = __format.format(value)
        return new_value

    def __normalize_currency(self, value):
        new_value = value.replace(" ", "")
        numbe_str = new_value[-3:]

        if "," in numbe_str:
            new_value = new_value.replace(".", "").replace(",", ".")
        else:
            new_value = new_value.replace(",", "")

        new_value = new_value.replace("R", "").replace("$", "")

        try:
            new_value = float(new_value)
        except Exception as ex:
            print(ex)

        return new_value
