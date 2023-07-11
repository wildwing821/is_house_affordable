import requests
import bs4
import pathlib
import re
import pandas as pd
from datetime import date
import numpy as np

class MortgageCalculator:
    def __init__(self):
        self.dirpath = pathlib.Path(__file__).parent.resolve()
        self.docpath = self.dirpath.joinpath('pe_list')
        self.my_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3;zh-tw',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': None
        }
        self.urlrate = 'http://www.mortgagenewsdaily.com/mortgage_rates/'
        self.urlNewhome = 'https://fred.stlouisfed.org/series/MSPNHSUS'
        self.urlMedianincome = 'https://fred.stlouisfed.org/series/MEHOINUSA672N'

    def get_item(self, url):
        html = requests.get(url, headers=self.my_header)
        if html.status_code != 200:
            print('Invalid URL:', html.url)
            print(html.status)
        objSoup = bs4.BeautifulSoup(html.text, 'lxml')
        item = objSoup.find('span', 'series-meta-observation-value')
        return item

    def get_current_mortgage_rate(self):
        morthtml = requests.get(self.urlrate, headers=self.my_header)
        if morthtml.status_code != 200:
            print('Invalid URL:', morthtml.url)
            print(morthtml.status)
        mortobjSoup = bs4.BeautifulSoup(morthtml.text, 'lxml')
        mortitems = mortobjSoup.find_all('td', 'rate-product')

        for mortitem in mortitems:
            current = mortitem.find_next_sibling().text.strip()
            break

        return float(current.strip('%'))  # remove '%'

    def get_clean_number(self, item):
        return re.sub(',', '', item.text.strip())

    def calculate_mortgage(self):
        newHomeprice = self.get_clean_number(self.get_item(self.urlNewhome))
        annualIncome = self.get_clean_number(self.get_item(self.urlMedianincome))
        monthlyIncome = float(annualIncome) * 0.28 / 12

        loanAmount = float(newHomeprice)
        interestRate = self.get_current_mortgage_rate()
        repaymentLength = 30

        interestCalculation = interestRate / 100
        monthlyRate = interestCalculation / 12
        numberOfPayments = repaymentLength * 12

        aveMonthpayrate = (pow((1 + monthlyRate), numberOfPayments) * monthlyRate) / (
                pow((1 + monthlyRate), numberOfPayments) - 1)
        monthlyPay = aveMonthpayrate * loanAmount
        totalInterest = monthlyPay * numberOfPayments - loanAmount
        annualPay = monthlyPay * 12
        if monthlyPay > monthlyIncome:
            affordable = 'no'
        else:
            affordable = 'yes'
        today = date.today()
        data_now = pd.DataFrame(np.column_stack([today,loanAmount,interestCalculation,monthlyIncome,monthlyPay,affordable]),columns=['date','new_homeprice','interest_rate','monthlyIncome','monthlyPay','affordable'])
        
        return data_now
        
    def save_data_to_excel(self, data):
        path = pathlib.Path("mortgage_list.xlsx")
        data_now = pd.DataFrame(data)
        if path.is_file():
            data_previous = pd.read_excel("mortgage_list.xlsx")
            new_data = pd.concat([data_previous, data_now])
            new_data.to_excel("mortgage_list.xlsx", index=False)
        else:
            data_now.to_excel("mortgage_list.xlsx", index=False)


if __name__ == '__main__':
    calculator = MortgageCalculator()
    mortgage_data = calculator.calculate_mortgage()

    calculator.save_data_to_excel(mortgage_data)
    print(mortgage_data)