from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import mysql.connector
import time

LOGIN = 'login'
PASSWORD = 'password'
URL = 'https://scihub.copernicus.eu/dhus'

api = SentinelAPI(LOGIN, PASSWORD, URL)

while True:
    mydb = mysql.connector.connect(
        host="host",
        user="user",
        password="password",
        database="db"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM links")
    myresult = mycursor.fetchall()

    # products = api.query(date=(date(2020, 8, 8), date(2020, 8, 9)), platformname='Sentinel-2')
    # products = api.query(date=('NOW-8HOURS', 'NOW'), producttype='SLC')
    products = api.query(date=('NOW-8HOURS', 'NOW'), platformname='Sentinel-1')

    links = []
    for i, v in enumerate(products):
        exist = False

        for link in myresult:
            if link[2] == products[v]['link']:
                exist = True


        if not exist:
            links.append([v, products[v]['link']])

    mycursor = mydb.cursor()
    sql = "INSERT INTO links (link_id, link) VALUES (%s, %s)"
    mycursor.executemany(sql, links)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

    time.sleep(60)


# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
#     # Print New Line on Complete
#     if iteration == total:
#         print()
#
#
# import time
#
# # A List of Items
# items = list(range(0, 57))
# l = len(items)
#
# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     print(i)
#     time.sleep(0.1)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

