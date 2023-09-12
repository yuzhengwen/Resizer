
import PySimpleGUI as sg
import os.path
from PIL import Image

#function to resize all image from input folder to a certain % and save in output folder
def resizeAllInFolder(inputPath, scale, outputPath):
    print("resize ALL")
    print("Input path: " + inputPath)
    #get names of picture files in list
    fileNames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(inputFolder, f))
            and f.lower().endswith((".png", "jpg", "jpeg"))]
    print("No of files: " + str(len(fileNames)))
    # Make dir recursively if output path doesnt exist
    print('output path: ' + outputPath)
    print(os.path.isdir(outputPath))
    if (os.path.isdir(outputPath)==False):
        print("New folder made")
        os.makedirs(outputPath)
    images = []
    for fileName in fileNames:
        images.append(Image.open(os.path.join(inputPath, fileName)))

    for i in images:
        print(i.size)
        print([int(scale * s) for s in i.size])
        #Image.size() returns 2 integers x and y
        output = i.resize( [int(scale * s) for s in i.size])
        #i.filename gives relative path from current folder
        baseFileName = os.path.basename(i.filename)
        print(" NEW " + outputPath+"/"+ baseFileName + " small.png")
        output.save(outputPath+"/"+ baseFileName + " small.png")

#GUI Column making
column = [
    [
        sg.Text("Input Folder"),
        sg.In(size=(25, 1), enable_events=True, key="inputFolder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Output Folder"),
        sg.In(size=(25, 1), enable_events=True, key="outputFolder"),
        sg.FolderBrowse(),
    ],
    {
        sg.Text("Resize Scale"),
        sg.In(size=(25, 1), enable_events=True, key="scale", default_text="0.5"),
    },
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="inputList"
        )
    ],
    [
        sg.Button("Resize", size=(15, 2), key="resize")
    ]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(column),
    ]
]

window = sg.Window("Resizer", layout)

inputFolder = None
outputFolder = None
scale = None

# Run the Event Loop (listen for inputs)
while True:
    # event gives the key, values[key] gives an array of the inputs from that element

    # to allow escaping loop when closing
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "inputFolder": # Folder name was filled in, make a list of files in the folder
        inputFolder = values["inputFolder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(inputFolder)
        except:
            file_list = []
        #get all filenames that are pictures in a list
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(inputFolder, f))
            and f.lower().endswith((".png", "jpg", "jpeg"))
        ]
        window["inputList"].update(fnames)
    elif event == "outputFolder":
        outputFolder=values["outputFolder"]
    elif event == "inputList":  # A file was chosen from the listbox
        try: 
            #Get fullPath of file and show
            fullPath = os.path.join(values["inputFolder"], values["inputList"][0])
            Image.open(fullPath).show()
        except:
            pass
    elif event == "resize":
        if inputFolder==None: 
            sg.popup_auto_close('Please select input folder')
        elif outputFolder==None: 
            sg.popup_auto_close('Please select output folder')
        else: 
            scale=float(values["scale"])
            print(inputFolder + "\n")
            print(str(scale) + "\n")
            print(outputFolder)
            resizeAllInFolder(inputFolder, scale, outputFolder)

window.close()