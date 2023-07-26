from process_url import url_data_extractor
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
    url = 'https://imsdb.com/scripts/Joker.html'
    dialogue_dict = url_data_extractor.get_url_dialogue(url)
    print(dialogue_dict['JOKER'])

if __name__ == '__main__':
    main()