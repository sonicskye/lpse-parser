'''
sonicskye @2018

pemenang.py is used to parse pemenang page in LPSE website
it stores class pemenang


'''


from bs4 import BeautifulSoup
import utilities as u
import vars as v
import csv
from pathlib import Path


class pemenang:

    _HEADERPREFERRED = ["Kode Tender", "Nama Tender", "Kategori", "Instansi", "Satker", "Pagu", "HPS",
                        "Nama Pemenang", "Alamat", "NPWP", "Harga Penawaran"]

    def generateurl(self, num):
        completeURL = v.menuEvaluasiURL + str(num) + v.staticCode + v.pemenangURL
        return completeURL

    def generatecontent(self, url):
        page = u.getcontent(url)
        return page

    def parsepage(self, page, num):
        # https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
        soup = BeautifulSoup(page, 'html.parser')

        # https://stackoverflow.com/questions/18966368/python-beautifulsoup-scrape-tables
        thList = []
        tdList = []
        thTemp = []
        tdTemp = []

        kodeTenderTempHeader = []
        kodeTenderTempData = []
        kodeTenderTempHeader.append("Kode Tender")
        kodeTenderTempData.append(str(num) + v.staticCode)
        thList.append(kodeTenderTempHeader)
        tdList.append(kodeTenderTempData)

        for tr in soup.find_all('tr'):
            # process the header cell
            ths = tr.find_all('th')
            thTemp2 = []
            for th in ths:
                thText = th.text.strip()
                #print(thText)
                if thText != "":
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
                #print(len(thList), len(tdList))

                for i in range(0,len(thTemp)-1):
                    header = thTemp[i]
                    dat = tdTemp[i]
                    #print (header, repr(dat))
        # cleanup unwanted data
        thList.pop(-2)
        tdList.pop(-2)

        # now we serialize the last data
        thLast = thList.pop(-1)
        tdLast = tdList.pop(-1)
        for i in range(0, len(thLast)):
            tempList = []
            tempList.append(thLast[i])
            thList.append(tempList)

        for i in range(0, len(tdLast)):
            tempList2 = []
            tempList2.append(tdLast[i])
            tdList.append(tempList2)

        # write to a csv file, named pemenang.csv
        # https://realpython.com/python-csv/
        filename: str = "results/pemenang" + "-" + v.govName + ".csv"

        # write the header
        # check whether the file exists
        # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions

        checkFile = Path(filename)
        if not checkFile.is_file():
            # file does not exist
            with open(filename, mode='w') as pemenangfile:
                pemenangwriter = csv.writer(pemenangfile, delimiter=',')
                pemenangwriter.writerow(self._HEADERPREFERRED)

        # @ToDo do not allow duplicates
        # https://stackoverflow.com/questions/15741564/removing-duplicate-rows-from-a-csv-file-using-a-python-script

        # write the data
        with open(filename, mode='a') as pemenangfile:
            pemenangwriter = csv.writer(pemenangfile, delimiter=',')
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
            pemenangwriter.writerow(dataAkhir)


    def iterate(self, lowNum, highNum):
        # iterating from lowNum to highNum
        for i in range(lowNum, highNum):
            url = self.generateurl(i)
            print("Processing: " + url)
            # if 404 not found then do not process anything
            try:
                page = self.generatecontent(url)
                self.parsepage(page, i)
            except:
                print ("Page not found or Error has happened")
                continue
