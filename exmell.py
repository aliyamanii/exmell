import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

# Function to load automata from XML file
def load_automata_from_xml(xml_file):
    automata = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extracting alphabet
    alphabet = []
    for alphabet_tag in root.find('Alphabets'):
        if alphabet_tag.tag == 'alphabet':
            alphabet.append(alphabet_tag.attrib['letter'])
    automata['alphabet'] = alphabet
    
    # Extracting states
    states = []
    final_states = []
    initial_state = None
    for state_tag in root.find('States'):
        if state_tag.tag == 'state':
            states.append(state_tag.attrib['name'])
        elif state_tag.tag == 'initialState':
            initial_state = state_tag.attrib['name']
        elif state_tag.tag == 'FinalStates':
            for final_state_tag in state_tag:
                final_states.append(final_state_tag.attrib['name'])
    automata['states'] = states
    automata['initial_state'] = initial_state
    automata['final_states'] = final_states
    
    # Extracting transitions
    transitions = {}
    for transition_tag in root.find('Transitions'):
        if transition_tag.tag == 'transition':
            source = transition_tag.attrib['source']
            destination = transition_tag.attrib['destination']
            label = transition_tag.attrib['label']
            if source not in transitions:
                transitions[source] = {}
            transitions[source][label] = destination
    automata['transitions'] = transitions
    
    return automata

# Function to check if a string is accepted by the automata
def check_string(automata, string):
    current_state = automata['initial_state']
    for symbol in string:
        if symbol not in automata['alphabet']:
            return False
        if current_state not in automata['transitions']:
            return False
        if symbol not in automata['transitions'][current_state]:
            return False
        current_state = automata['transitions'][current_state][symbol]
    return current_state in automata['final_states']

# Function to select XML file using file dialog
def select_file():
    filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)

# Function to check string and display result
def check_and_display(event=None):
    filename = entry_file.get()
    if not filename:
        label_result.config(text="Please select an XML file first.", fg="red")
        return
    automata = load_automata_from_xml(filename)
    string = entry_string.get()
    if string == 'end':
        root.destroy()
        return
    if check_string(automata, string):
        label_result.config(text="String accepted.", fg="green")
    else:
        label_result.config(text="String rejected.", fg="red")

# Create main GUI window
root = tk.Tk()
root.title("Exmell")
root.geometry("450x300")

# Create a frame with border
frame = tk.Frame(root, relief="solid", borderwidth=2, width=300, height=600,bg="#FFD966" )
frame.pack(padx=10, pady=40)
root.configure(bg="#FFF2CC")

# Label for file selection
label_file = tk.Label(frame, text="Select XML file:", bg="#FFD966", fg="#6C3428", font=("Cooper Black", 12))
label_file.pack()

# Entry field for file path
entry_file = tk.Entry(frame, bg="#f0f0f0", bd=2, relief="solid", width=30, font=("Times New Roman", 12))
entry_file.pack(pady=5)

# Button to browse files
button_browse = tk.Button(frame, text="Browse", command=select_file, bg="#4793AF", fg="#FEFDED", bd=0, font=("Times New Roman", 12))
button_browse.pack()

# Label for string input instruction
label_instruction = tk.Label(frame, text="Enter a string to check (type 'end' to quit):", bg="#FFD966", fg="#6C3428", font=("Cooper Black", 12))
label_instruction.pack()

# Entry field for string input
entry_string = tk.Entry(frame, bg="white", bd=2, relief="solid", width=30, font=("Arial", 12))
entry_string.pack(pady=5)
entry_string.bind("<Return>", check_and_display)

# Button to check string
button_check = tk.Button(frame, text="Check", command=check_and_display, bg="#4793AF", fg="#FEFDED", bd=0, font=("Times New Roman", 12))
button_check.pack()

# Label to display result
label_result = tk.Label(frame, text="", fg="#f0f0f0", bg="#FFD966", font=("Times New Roman", 14, "bold"))
label_result.pack()

# Start the GUI event loop
root.mainloop()
