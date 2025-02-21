import pefile
import base64

def extract_sections(filename):
    try:
        pe = pefile.PE(filename)
        sequence_found = False
        found_section = None
        found_address = None
        #decoded_string = ""
    
        for section in pe.sections:
            section_data = section.get_data()
            
            #the pattern
            offset = section_data.find(b'\x62\x58')
            
            if offset !=-1:
                sequence_found = True
                found_section = section.Name.decode('utf-8')
                found_address = section.PointerToRawData + offset
                
                #this section responsible for finding the full string and decoding from base64
                full_string = section_data[offset:offset+40]
                decoded_bytes = base64.b64decode(full_string)
                decoded_string = decoded_bytes.decode('utf-8')
                
                break
        
            
        return sequence_found, found_section, found_address, decoded_string
        
    except pefile.PEFormatError:
            print(f"Error: {filename} is not a valid PE file.")
            return False, None, None

def main():

    filename = input("Enter PE File Name: ")
    sequence_found, found_section, found_address, decoded_string = extract_sections(filename)
    
    if sequence_found:
        print("\nThe decoded string is: ", decoded_string)
        print(f"The byte sequence is found in the {found_section} section at memory address 0x{found_address:x}.")
    else:
        print("Byte sequencee not found in any section.")

if __name__ == "__main__":
  main()
