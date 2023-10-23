
import os
import csv

def save_csv(prompts_and_responses, character, movie):
    save_directory =  get_save_directory(movie)

    if not (os.path.exists(save_directory)):
        os.mkdir(save_directory)

    path = get_path(character, movie)
    if os.path.exists(path):
        print("Data already saved at: ")
        print(path)
        print("Continuing...")
        return


    field_names = prompts_and_responses[0].keys()
    #temporary bug fix
    del prompts_and_responses[0]


    with open(path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(prompts_and_responses)

    print("Prompts and responses sucessfully saved at: ")
    print(path)

def get_path(character, movie):
    save_directory =  get_save_directory(movie)
    character_for_filename = "".join(character.lower().split())
    csv_file = character_for_filename + "data.csv"
    path = save_directory + csv_file
    return path

def get_save_directory(movie):
    save_directory =  "data" + os.sep + movie + os.sep
    return save_directory