import PySimpleGUI as sg


sg.theme('DarkAmber')

min_val=None
layout = [
    [sg.Text(min_val)],
    [sg.Button('Cancel')]
]
window = sg.Window('Time Series Analysis', layout)

def set_min_val(min_val):
    min_val =min_val
