Converter of date values ​​and currency values.

Adjusts the values ​​to be able to save to the database and also adjusts some output formats for returns.

To convert a date to the US standard (for database), import NormalizeDates() class *from normalize.dates.normalize_dates import NormalizeDates*
then use NormalizeDates().normalize(string_of_your_date)

Accepted date formats:
20/03/1990
20-30-1990
March 30th, 1990
20 de março de 1990

To convert the date to a detailed format, import ConvertDates() class *from normalize.dates.convert_dates import ConvertDates*
then use ConvertDates(string_your_format).convert(string_of_your_date*)
* US standard - 1990-03-20

Accepted formats:
/br returns 20/03/1990
full_br returns 20 de março de 1990
full_us returns March 30th, 1990


To convert a currency value, import the NormalizeCurrency() class *from normalize.currency.currency import NormalizeCurrency*

then use NormalizeCurrency()normalize_currency(string_of_your_currency*) function

Accepted currency:
R$ 5.000,00
R$ 5000,00
R$ 5,000
$ 5,000.00

then returns 5000.0

To convert a currency value, import the NormalizeCurrency() class *from normalize.currency.currency import NormalizeCurrency*

then use NormalizeCurrency(locale*)convert_currency(float_of_your_currency*) function

* the "locale" argument return according to the given argument:

locale="en_US" returns $ 5,000.00
locale="pt_BR" returns R$ 5.000,00

