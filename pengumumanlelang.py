'''
sonicskye @2018

tableparser is used to parse a table in LPSE website


'''


from bs4 import BeautifulSoup
import utilities as u
import vars as v
import csv


headerPreferred = ["Kode Tender", "Nama Tender", "Tanggal Pembuatan", "Tahap Tender Saat ini", "Instansi",
                       "Satuan Kerja", "Kategori", "Sistem Pengadaan", "Tahun Anggaran", "Nilai Pagu Paket",
                       "Nilai HPS Paket", "Peserta Tender"]

def generateurl(num):
    completeURL = v.frontURL + str(num) + v.staticCode + v.pengumumanLelangURL
    return completeURL


def generatecontent(url):
    page = u.getcontent(url)
    return page


def parsepage(page):
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
    with open(filename, mode='a') as pengumumanlelangfile:
        pengumumanlelangwriter = csv.writer(pengumumanlelangfile, delimiter=',')
        dataAkhir = []
        for i in range (0, len(thList)):
            daftarHeader = thList[i]
            daftarData = tdList[i]
            for j in range(0, len(daftarHeader)):
                header = daftarHeader[j]
                if header in headerPreferred:
                    # keep the \\n inside the data string
                    data = repr(daftarData[j])
                    dataAkhir.append(data)
        pengumumanlelangwriter.writerow(dataAkhir)


def main():
    # initialising csv
    filename: str = "results/pengumumanlelang" + "-" + v.govName + ".csv"
    with open(filename, mode='w') as pengumumanlelangfile:
        pengumumanlelangwriter = csv.writer(pengumumanlelangfile, delimiter=',')
        pengumumanlelangwriter.writerow(headerPreferred)

    # iterating from lowNum to highNum
    for i in range(v.lowNum, v.highNum):
        url = generateurl(i)
        print("Processing: " + url)
        # if 404 not found then do not process anything
        try:
            page = generatecontent(url)
            parsepage(page)
        except:
            continue


if __name__ == '__main__':
    main()