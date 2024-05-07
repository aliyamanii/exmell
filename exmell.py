import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def load_automaton_from_xml(xml_file):
    automaton = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extracting alphabet
    alphabet = []
    for alphabet_tag in root.find('Alphabets'):
        if alphabet_tag.tag == 'alphabet':
            alphabet.append(alphabet_tag.attrib['letter'])
    automaton['alphabet'] = alphabet
    
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
    automaton['states'] = states
    automaton['initial_state'] = initial_state
    automaton['final_states'] = final_states
    
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
    automaton['transitions'] = transitions
    
    return automaton

def check_string(automaton, string):
    current_state = automaton['initial_state']
    for symbol in string:
        if symbol not in automaton['alphabet']:
            return False
        if current_state not in automaton['transitions']:
            return False
        if symbol not in automaton['transitions'][current_state]:
            return False
        current_state = automaton['transitions'][current_state][symbol]
    return current_state in automaton['final_states']

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)

def check_and_display(event=None):
    filename = entry_file.get()
    if not filename:
        label_result.config(text="Please select an XML file first.", fg="red")
        return
    automaton = load_automaton_from_xml(filename)
    string = entry_string.get()
    if string == 'end':
        root.destroy()
        return
    if check_string(automaton, string):
        label_result.config(text="String accepted.", fg="green")
    else:
        label_result.config(text="String rejected.", fg="red")

root = tk.Tk()
root.title("Exmell")

# Create a frame with border
frame = tk.Frame(root, relief="solid", borderwidth=1)
frame.pack(padx=10, pady=10)  # Add padding around the frame

# Styling
root.configure(bg="#f0f0f0")

label_file = tk.Label(frame, text="Select XML file:", bg="#f0f0f0")
label_file.pack()

entry_file = tk.Entry(frame, bg="white", bd=2, relief="solid")
entry_file.pack(pady=5)  # Add padding between entry and button

button_browse = tk.Button(frame, text="Browse", command=select_file, bg="#4CAF50", fg="white", bd=0)
button_browse.pack()

label_instruction = tk.Label(frame, text="Enter a string to check (type 'end' to quit):", bg="#f0f0f0")
label_instruction.pack()

entry_string = tk.Entry(frame, bg="white", bd=2, relief="solid")
entry_string.pack(pady=5)  # Add padding between entry and button
entry_string.bind("<Return>", check_and_display)  # Bind Enter key to check_and_display function

button_check = tk.Button(frame, text="Check", command=check_and_display, bg="#008CBA", fg="white", bd=0)
button_check.pack()

label_result = tk.Label(frame, text="", fg="black", bg="#f0f0f0")
label_result.pack()

root.mainloop()
