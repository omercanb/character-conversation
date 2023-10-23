from process_url import url_data_extractor
import csv 
import sys

"""
example urls: 
halloween: https://imsdb.com/scripts/Halloween.html
joker: https://imsdb.com/scripts/Joker.html
https://imsdb.com/scripts/BlacKkKlansman.html
https://imsdb.com/scripts/A-Prayer-Before-Dawn.html
https://imsdb.com/scripts/A-Quiet-Place.html
https://imsdb.com/scripts/Coco.html
"""

def main():
    url = 'https://imsdb.com/scripts/Shrek.html'
    possible_characters = url_data_extractor.choose_character(url)
    print("Choose a character")
    print(possible_characters)
    character = input()
    if character not in possible_characters:
        sys.exit()
    promt_response_list = url_data_extractor.get_prompt_response_list(url, character)
    
    csv_file = character.lower() + "data.csv"
    field_names = promt_response_list[0].keys()
    #temporary bug fix
    del promt_response_list[0]


    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(promt_response_list)

if __name__ == '__main__':
    main()