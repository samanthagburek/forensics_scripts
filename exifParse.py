import sys
import exifread


def main():
    if len(sys.argv) == 1:
        print("Error! - No Image File Specified!")
    try:
        #takes in JPG file
        file = open(sys.argv[1], "rb")
    except:
        print("Error! - File Not Found!")
        return

    #gets all metadata info and stores it in dictionary-view exifread documentation
    tags = exifread.process_file(file)

    #name of provided source file
    print("Source File: " + str(sys.argv[1]))

    #make of device that took the photo
    print("Make: " + str(tags['Image Make']))

    #model of device that took the photo
    print("Model: " + str(tags['Image Model']))

    #date and time photo was taken
    print("Original Date/Time: " + str(tags['Image DateTime']))

    # latitude of photo in degrees, minutes float, seconds float when given in format [int, int, int/int]
    latcoordinates = str(tags['GPS GPSLatitude']).split(',')
    latcoordinates_s = latcoordinates[2][:-1].split('/')
    secs = float(latcoordinates_s[0])/float(latcoordinates_s[1])
    print("Latitude: " + str(latcoordinates[0][1:]) + ' degrees, '
          + str(float(latcoordinates[1])) + ' minutes, '
          + str(secs) + ' seconds')

    # longitude of photo in degrees, minutes float, seconds float when given in format [int, int, int/int]
    longcoordinates = str(tags['GPS GPSLongitude']).split(',')
    print(tags['GPS GPSLongitude'])
    longcoordinates_s = longcoordinates[2][:-1].split('/')
    secs2 = float(longcoordinates_s[0]) / float(longcoordinates_s[1])
    print("Longitude: " + str(longcoordinates[0][1:]) + ' degrees, '
          + str(float(longcoordinates[1])) + ' minutes, '
          + str(secs2) + ' seconds')

if __name__ == "__main__":
    main()





