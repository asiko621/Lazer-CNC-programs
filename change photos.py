import selenium
import pyautogui
import time
import os # file and folder usage
import shutil # copy and deleting files
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from PIL import Image,ImageOps #allows images to be tampered with

SIZE = 3000

#NOTES: Must have folders in desktop of windows machine named ""

def convertToPNG(fileLocation):
    
    # click and enter photo absolute refernced file location
    time.sleep(10)
    clickAtPoint(829,819)
    time.sleep(1)
    pyautogui.write(fileLocation)
    time.sleep(1)
    pyautogui.press("enter")

    #scroll down
    time.sleep(10)
    pyautogui.scroll(-200)

    #download png converted photo after waiting 20 second
    time.sleep(10)
    clickAtPoint(534,831)

# takes in a absolute referenced location of a file containing a picture
def removeBackground(fileLocation):

    # click and enter photo absolute refernced file location
    time.sleep(10) # gives browser time to open up
    clickAtPoint(1205,770)
    time.sleep(1)
    pyautogui.write(fileLocation)
    time.sleep(1)
    pyautogui.press('enter')
    
    #download background erased photo after waiting 20 second
    time.sleep(10)
    clickAtPoint(1063,655)

def removeExtension(nameOfFile):
    nameOfFile = str(nameOfFile)
    #rfind returns last "." in case file name has another "."
    #"before : means start of file while after : means stop at that index
    nameOfFile = nameOfFile[:nameOfFile.rfind(".")]
    
    return nameOfFile

# opens window in fullscreen at certain URL
def fullScreenTab(URL):
    URL = str(URL) 
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get(URL)
    return driver

def clickAtPoint( x,  y):
    #allows .moveTo to be used
    x = int(x)
    y = int(y)
    pyautogui.moveTo(x,y)
    time.sleep(1)
    pyautogui.click()

def removeBackgrounds(folder_path,file_names):
    #remove all backgrounds of photos
    for photoName in file_names:
        if not ("[PROCESSED]" in photoName): #Processed indicates photo has been processed (photo must be right format)
            driver = fullScreenTab("https://www.adobe.com/express/feature/image/remove-background?msockid=1249b0ec030167501d4da41902ab662a")
            removeBackground("C:\\Users\\chubb\\OneDrive\\Desktop\\New Photos\\" + photoName)
            time.sleep(5)
            driver.quit()
            #wait 10 seconds then copy the downloaded file from Downloads folder and place in background removed folder
            #assume there is only one "Adobe Express - file.png"
            time.sleep(10)
            #takes the .crdownload from the downloads folder and converts the name and place it in the background removed folder
            if not os.path.exists("C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos\\[NO-BACKGROUND]" + photoName.replace(".jpeg","")) and os.path.exists("C:\\Users\\chubb\\Downloads\\Adobe Express - file.png"):
                os.rename("C:\\Users\\chubb\\Downloads\\Adobe Express - file.png", "C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos\\[NO-BACKGROUND]" + photoName.replace(".jpeg",""))
            if not os.path.exists(folder_path + "\\[PROCESSED]" + photoName) and os.path.exists(folder_path + "\\" + photoName):
                os.rename(folder_path + "\\" + photoName, folder_path + "\\[PROCESSED]" + photoName)

def convertToPNGs(folder_path,file_names):
     #convert photos to png
    
    print(file_names)
    for photoName in file_names:
        if not ("[PROCESSED]" in photoName) and (not ".png" in photoName): #Processed indicates photo has been processed (photo must be jpeg)
            driver = fullScreenTab(r"https://jpg2png.com/")
            convertToPNG("C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos\\" + photoName)
            time.sleep(5)
            driver.quit()

            #wait 10 seconds then copy the downloaded file from Downloads folder and place in background removed folder
            #assume there is only one "Adobe Express - file.png"
            time.sleep(10)

            #photoName will not take into account the new extension
            photoPNGExt = removeExtension(photoName) + ".png"

            #takes the converted png from the downloads folder and converts the name and place it in the PNG converted folder
            if not os.path.exists("C:\\Users\\chubb\\OneDrive\\Desktop\\PNG Converted Photos\\[PNG-CONVERTED]" + photoPNGExt) and os.path.exists("C:\\Users\\chubb\\Downloads\\" + photoPNGExt):
                os.rename("C:\\Users\\chubb\\Downloads\\" + photoPNGExt, "C:\\Users\\chubb\\OneDrive\\Desktop\\PNG Converted Photos\\[PNG-CONVERTED]" + photoPNGExt)
            if not os.path.exists(folder_path + "\\[PROCESSED]" + photoName) and os.path.exists(folder_path + "\\" + photoName):
                os.rename(folder_path + "\\" + photoName, folder_path + "\\[PROCESSED]" + photoName)

        else: # still move file to png converted if it is already a png
            if not os.path.exists("C:\\Users\\chubb\\OneDrive\\Desktop\\PNG Converted Photos\\[PNG-CONVERTED]" + photoName) and os.path.exists("C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos\\" + photoName):
                os.rename("C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos\\" + photoName, "C:\\Users\\chubb\\OneDrive\\Desktop\\PNG Converted Photos\\[PNG-CONVERTED]" + photoName)
            if not os.path.exists(folder_path + "\\[PROCESSED]" + photoName) and os.path.exists(folder_path + "\\" + photoName):
                os.rename(folder_path + "\\" + photoName, folder_path + "\\[PROCESSED]" + photoName)

def reSizePNGs(folder_path,file_names):
    for photoName in file_names:
        if not ("[PROCESSED]" in photoName): 
            currentImage = Image.open(folder_path + "\\" + photoName).convert("RGBA")
            #gets transparent border of image
            border = currentImage.split()[-1].getbbox()
            #remove transparent border of image in order to have photo scale to larger size
            currentImage = currentImage.crop(border)

            
            #find largest dimension of current image
            if currentImage.height >= currentImage.width:
                largestDimension = currentImage.height
            else:
                largestDimension = currentImage.width
            
            #resize so largest Dimension is SIZE
            scaleFactor = SIZE/largestDimension
            new_size = (int(currentImage.width * scaleFactor), int(currentImage.height * scaleFactor))

            scaledImage = currentImage.resize(new_size,Image.LANCZOS)
            scaledImage = scaledImage.convert("RGBA")

            #find smallest size after scaling as the smallest size value will change after being scaled
            if scaledImage.height >= scaledImage.width:
                smallestDimension = scaledImage.width
            else:
                smallestDimension = scaledImage.height

            
            pixelsToAdd = SIZE - smallestDimension
            pixelsToAdd = int(pixelsToAdd)
            borderSizes = (0, 0, 0, 0) #left, Top, right, bottom

            #add pixels to each "half" of the smaller dimension
            if scaledImage.height >= scaledImage.width:
                print("HEIGHT")
                borderSizes = (int(pixelsToAdd/2),0,int(pixelsToAdd/2),0)

            else:
                print("WIDTH")
                borderSizes = (0 , int(pixelsToAdd/2) , 0 ,int(pixelsToAdd/2))





            print(borderSizes)
            #add lines to smaller dimension
            scaledImage = ImageOps.expand(scaledImage,border = borderSizes,fill = (0,0,0,0))
            scaledImage = scaledImage.resize((SIZE,SIZE)) # resize image to 3000 x 3000 since side could have 2999 value
            #smaller dimension may be 2999 pixels so we will slightly stretch image so it can be used late as 3000x3000
            
            scaledImage.save("C:\\Users\\chubb\\OneDrive\\Desktop\\Re-sized (3000x3000)\\" + photoName)



def mergeToFilter(folder_path,file_names,filterPath):
    for photoName in file_names:
        if not ("[PROCESSED]" in photoName): 
            filterImage = Image.open(filterPath).convert("RGBA")
            personImage = Image.open(folder_path + "\\" + photoName).convert("RGBA")

            finishedImage = Image.alpha_composite(personImage, filterImage)
                    
        finishedImage.save(os.path.join("C:\\Users\\chubb\\OneDrive\\Desktop\\Finished Photos", "Finished" + photoName))






            
            

           

        





def main():

    folder_path = "C:\\Users\\chubb\\OneDrive\\Desktop\\New Photos"
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    removeBackgrounds(folder_path,file_names)

    folder_path = "C:\\Users\\chubb\\OneDrive\\Desktop\\Background Removed Photos"
    file_names.clear()
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    convertToPNGs(folder_path,file_names)

    folder_path = "C:\\Users\\chubb\\OneDrive\\Desktop\\PNG Converted Photos"
    file_names.clear()
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    reSizePNGs(folder_path,file_names)

    folder_path = "C:\\Users\\chubb\\OneDrive\\Desktop\\Re-sized (3000x3000)"
    file_names.clear()
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    mergeToFilter(folder_path,file_names,"C:\\Users\\chubb\\OneDrive\\Desktop\\Photo Filters\\wreath.PNG")





    print("FINISHED")
    
    
            


    

main()