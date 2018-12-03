'''
sonicskye @2018

pengumumanlelang.py is used to parse pengumumanlelang page in LPSE website
it stores class pengumumanlelang


'''


from bs4 import BeautifulSoup
import utilities as u
import vars as v
import csv
from pathlib import Path


class pengumumanlelang:

    _HEADERPREFERRED = ["Kode Tender", "Nama Tender", "Tanggal Pembuatan", "Tahap Tender Saat ini", "Instansi",
                           "Satuan Kerja", "Kategori", "Sistem Pengadaan", "Tahun Anggaran", "Nilai Pagu Paket",
                           "Nilai HPS Paket", "Peserta Tender"]

    def generateurl(self, num):
        completeURL = v.frontURL + str(num) + v.staticCode + v.pengumumanLelangURL
        return completeURL

    def generatecontent(self, url):
        page = u.getcontent(url)
        return page

    def parsepage(self, page):
        # https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
        soup = BeautifulSoup(page, 'html.parser')

        # https://stackoverflow.com/questions/18966368/python-beautifulsoup-scrape-tables
        thList = []
        tdList = []
        thTemp = []
        tdTemp = []
        for tr in soup.find_all('tr'):
            # process the header cell
            ths = tr.find_all('th')
            thTemp2 = []
            for th in ths:
                thText = th.text.strip()
                # Jenis Kontrak is hard to handle. Exclude for now
                if thText != "" and thText != "Jenis Kontrak":
                    thTemp2.append(thText)
            if len(thTemp2) != 0:
                thTemp = thTemp2


            #process the data cell
            tds = tr.find_all('td')
            tdTemp2 = []
            for td in tds:
                tdText = td.text.strip()
                if tdText != "":
                    tdTemp2.append(tdText)
            if len(tdTemp2) != 0:
                tdTemp = tdTemp2
                thList.append(thTemp)
                tdList.append(tdTemp)

                for i in range(0,len(thTemp)-1):
                    header = thTemp[i]
                    dat = tdTemp[i]

        # write to a csv file, named pengumumanlelang.csv
        # https://realpython.com/python-csv/
        filename: str = "results/pengumumanlelang" + "-" + v.govName + ".csv"

        # write the header
        # check whether the file exists
        # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        checkFile = Path(filename)
        if not checkFile.is_file():
            # file does not exist
            with open(filename, mode='w') as pengumumanlelangfile:
                pengumumanlelangwriter = csv.writer(pengumumanlelangfile, delimiter=',')
                pengumumanlelangwriter.writerow(self._HEADERPREFERRED)

        # @ToDo do not allow duplicates
        # https://stackoverflow.com/questions/15741564/removing-duplicate-rows-from-a-csv-file-using-a-python-script

        # write the data
        with open(filename, mode='a') as pengumumanlelangfile:
            pengumumanlelangwriter = csv.writer(pengumumanlelangfile, delimiter=',')
            dataAkhir = []
            for i in range (0, len(thList)):
                daftarHeader = thList[i]
                daftarData = tdList[i]
                for j in range(0, len(daftarHeader)):
                    header = daftarHeader[j]
                    if header in self._HEADERPREFERRED:
                        # keep the \\n inside the data string
                        data = repr(daftarData[j])
                        dataAkhir.append(data)
            pengumumanlelangwriter.writerow(dataAkhir)

    def iterate(self, lowNum, highNum):
        # iterating from lowNum to highNum
        for i in range(lowNum, highNum):
            print(i)
            url = self.generateurl(i)
            print("Processing: " + url)
            # if 404 not found then do not process anything
            try:
                page = self.generatecontent(url)
                self.parsepage(page)
            except:
                continue
