import sys
import sqlite3
from datetime import datetime

def main():
    if len(sys.argv) == 1:
        print("Error! - No History File Specified!")
    try:
        file = open(sys.argv[1], "rb")
    except:
        print("Error! - File Not Found!")
        return

    #takes in a Google ChromeHistory SQLite database file
    con = sqlite3.connect(sys.argv[1])
    cur = con.cursor()

    #name of provided source file
    print("Source File: " + sys.argv[1])

    #total number of downloads
    numDownloads = cur.execute("SELECT COUNT (*) FROM downloads")
    print("Total Downloads: " + str(numDownloads.fetchall()[0][0]))

    #name and size of file that took the longest to download, not whole path just file name
    largest = cur.execute("SELECT d.target_path, total_bytes FROM downloads d ORDER BY d.end_time - d.start_time DESC")
    file_data = largest.fetchone()
    print("File Name: " + str(file_data[0]).split('\\')[-1])
    print("File Size: " + str(file_data[1]))

    #number of unique search terms
    src = cur.execute("SELECT Count(DISTINCT term) FROM keyword_search_terms")
    print("Unique Search Terms: " + str(src.fetchall()[0][0]))

    #term, date and time of most recent search, converted to Y-M-D H-M-S from webkit/chrome timestamp
    distinct_search = cur.execute("SELECT k.term, strftime('%Y-', datetime((u.last_visit_time / 1000000) - 11644473600, 'unixepoch', 'localtime')) || CASE strftime('%m', datetime((u.last_visit_time / 1000000) - 11644473600, 'unixepoch', 'localtime')) WHEN '01' THEN 'Jan' WHEN '02' THEN 'Feb' WHEN '03' THEN 'Mar' WHEN '04' THEN 'Apr' WHEN '05' THEN 'May' WHEN '06' THEN 'Jun' WHEN '07' THEN 'Jul' WHEN '08' THEN 'Aug' WHEN '09' THEN 'Sep' WHEN '10' THEN 'Oct' WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dec' END || strftime('-%d %H:%M:%S', datetime((u.last_visit_time / 1000000) - 11644473600, 'unixepoch', 'localtime')) AS formatted_time FROM keyword_search_terms k JOIN urls u ON u.id = k.url_id ORDER BY u.last_visit_time DESC;")
    recent_search = distinct_search.fetchone()
    print("Most Recent Search: " + str(recent_search[0]))
    print("Most Recent Search Date/Time: " + str(recent_search[1]))

    # for row in cur.execute("SELECT * FROM sqlite_master WHERE type='table'"):
    #     print(row)

if __name__ == "__main__":
    main()
