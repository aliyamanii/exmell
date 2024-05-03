import xml.etree.ElementTree as ET

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

def main():
    xml_file = input("Enter the title of your XML file: ")
    automaton = load_automaton_from_xml(xml_file)
    print("Alphabet:", automaton['alphabet'])
    print("States:", automaton['states'])
    print("Initial State:", automaton['initial_state'])
    print("Final States:", automaton['final_states'])
    while True:
        string = input("Enter a string to check (type 'end' to quit): ")
        if string == 'end':
            break
        if check_string(automaton, string):
            print("String accepted.")
        else:
            print("String rejected.")

if __name__ == "__main__":
    main()
