def get_folder_path(title = 'Choose a Folder Path'):
    import PySimpleGUI as sg
    import os.path
    
    layout = [
        [sg.Text("Choose a Folder"),
         sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
         sg.FolderBrowse(),],
        [sg.Button("OK")]]
    
    window = sg.Window(title,layout)
    
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
        else:
            folder = None
    
    window.close()
    if folder == None:
        print('No Folder Chosen')
    else:
        return folder +'//'
    