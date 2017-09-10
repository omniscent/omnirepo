import sys
import ConfigParser
from Crypto.Cipher import AES
import hashlib
import base64
import string
import random
import os
import time
import getpass
from os import walk
from shutil import copyfile

'''
to later set the color of some objects this is needed:
from termcolor import colored

print colored('hello', 'red'), colored('world', 'green')

i just noted this cause i want to implemet it later
'''

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def centerify(text, width=-1):
  lines = text.split('\n')
  width = max(map(len, lines)) if width == -1 else width
  return '\n'.join(line.center(width) for line in lines)

def terminal_size():
    import fcntl, termios, struct
    th, tw, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return tw#, th       i only need tw

#important things first. ascii art.
def ascii_art():
    clear_screen()
    tw = terminal_size()
    print(centerify("                       _                         _     ",tw))
    print(centerify("                      (_)                       | |    ",tw))
    print(centerify("  ___  _ __ ___  _ __  _ ___  ___  __ _ _ __ ___| |__  ",tw))
    print(centerify(" / _ \| '_ ` _ \| '_ \| / __|/ _ \/ _` | '__/ __| '_ \ ",tw))
    print(centerify("| (_) | | | | | | | | | \__ \  __/ (_| | | | (__| | | |",tw))
    print(centerify(" \___/|_| |_| |_|_| |_|_|___/\___|\__,_|_|  \___|_| |_|",tw))
    print(centerify("",tw))
    print(centerify("                Version 0.7 closed beta                ",tw))
    print(centerify("",tw))
    print(centerify("",tw))

def press_enter():
    print ""
    any_key = raw_input("press enter to continue...")
    enter_pressed = True
    return enter_pressed

def changelog():
    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.2"
    print "-- show menu after view object"
    print "-- hide encryption password while typing and show it for 2.5 seconds after confirm input"
    print "-- changed name of body_height to body_height_(in_cm)"
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print "-- define ascii art as function"
    print "-- created function \"changelog\""
    print "-- created menu entry \"changelog\""
    print ""
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.3"
    print "-- changed label from \"car_brand\" and \"mobile_phone\" to \"car brand\" and \"mobile phone\""
    print "-- changed wrong label for option father. it was \"name of sister\" instead of \"name of father\""
    print "-- corrected misspelling of \"encrption\" in password query"
    print "-- fixed bug that section \"education\" was not saved in database file"
    print "-- changed name of option from \"xxx_aray\" to \"xxx\""
    print "-- changed menu text from \"Enter your choice [1-5]\" to \"Enter your choice [1-6]\""
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.3.1"
    print "-- changed label from \"car_brand\" and \"mobile_phone\" to \"car brand\" and \"mobile phone\""
    print "-- changed wrong label for option father. it was \"name of sister\" instead of \"name of father\""
    print "-- corrected misspelling of \"encrption\" in password query"
    print "-- fixed bug that section \"education\" was not saved in database file"
    print "-- changed name of option from \"xxx_aray\" to \"xxx\""
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print "-- changed menu text from \"Enter your choice [1-6]\" to \"enter your choice [1-6]\""
    print "-- created super fancy search function"
    print "-- print userfriendly error message when type anything else then a number in the menu"
    print "-- implementet a check if the database path exists after it was defined"
    print "-- while asking for encryption password, script now asks twice instead of showing the password for 2.5 seconds"
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.4"
    print "-- changed create function and reduced it from 523 lines to 52 lines"
    print "--- information options are now saved in a template file in the database directory and are not hardcoded anymore"
    print "-- other functions has been adaptet to the new create function"
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.5"
    print "-- created draft function"
    print "-- other functions has been adaptet to the new drafts function"
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.6"
    print "-- added a text output in all functions about \";\" as delimiter"
    print "-- created list_all function"
    print "-- changed define_password function to quit script after three wrong entries"
    print "-- changed define_database_path function to quit script after three wrong entries"
    print "-- fixed bug in drafts function which caused a \"no drafts found\" print even if a draft exists"
    print "-- changed default template file which is defined in check_template function"
    print "-- created export function to export entry as undecrypted txt files"
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print 40 * "-"
    print ""

    print ""
    print 20 * "-", " changelog ", 20 * "-"
    print ""
    print "- changelog version 0.7"
    print "-- changed search function to search for section \"identifier\" and option \"identifier1\" or \"identifier2\""
    print "--- adaptet default template to this"
    print "-- removed print of filenames in create function"
    print "-- centered ascii art"
    print "-- changed version number in the very important supercalifragilisticexpialidocious ascii art"
    print 40 * "-"
    print ""


#id_generator function
def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def define_database_path():
    global database_path
    database_path = "path"
    try_counter = 0
    false = 0

    while os.path.isdir(database_path) != True:
        try_counter = try_counter + 1
        if try_counter > 3:
            print ""
            print "!!!!!! three wrong tries. please start script again. !!!!!!"
            print ""
            quit()
        if false != 0:
            print ""
            print "path does not exist. try again."
            print ""
        database_path = raw_input("enter database path (must end with \"/\"): ")
        print ""
        false = false + 1


def define_enc_password():
    try_counter = 0
    false = 0
    enc_password_plain_1 = "x"
    enc_password_plain_2 = "y"

    while enc_password_plain_1 != enc_password_plain_2:
        try_counter = try_counter + 1
        if try_counter > 3:
            print ""
            print "!!!!!! three wrong tries. please start script again. !!!!!!"
            print ""
            quit()

        if false != 0:
            print ""
            print "!!!!!! passwords do not match. try again. !!!!!!"
            print ""

        print "type in encryption password: "
        enc_password_plain_1 = getpass.getpass()
        print ""

        print "type in encryption password again: "
        enc_password_plain_2 = getpass.getpass()
        print ""

        if enc_password_plain_1 == enc_password_plain_2:
            global enc_password
            enc_password = hasher(enc_password_plain_1)
        else:
            false = false + 1

def check_template():
    template_bool = os.path.isfile(database_path + "template")
    if template_bool == True:
        return True
    elif template_bool == False:
        print ""
        print 73 * "-"
        print "template file does not exist. creating template file with default values."
        print 73 * "-"
        press_enter()

        filepath = database_path + "template"
        new_file = open(filepath,"w")
        #dont change this sections!:
        new_file.write("[entry_id]\n")
        new_file.write("entry_id =\n")
        new_file.write("\n")
        new_file.write("[identifier]\n")
        new_file.write("identifier1 =\n")
        new_file.write("identifier2 =\n")
        new_file.write("\n")

        #ths sections can be changed!:
        new_file.write("[personal details]\n")
        new_file.write("firstname =\n")
        new_file.write("second name =\n")
        new_file.write("lastname =\n")
        new_file.write("nationality =\n")
        new_file.write("birthday (day only) =\n")
        new_file.write("birthmonth (month only)=\n")
        new_file.write("birthyear (year  only)=\n")
        new_file.write("place of residence (street and number) =\n")
        new_file.write("place of residence (post code) =\n")
        new_file.write("place of residence (town/village) =\n")
        new_file.write("place of residence (country) =\n")
        new_file.write("religion =\n")
        new_file.write("languages spoken =\n")
        new_file.write("job =\n")
        new_file.write("car brand =\n")
        new_file.write("mobile phone brand =\n")
        new_file.write("\n")
        new_file.write("[notes to personal details] =\n")
        new_file.write("notes to firstname =\n")
        new_file.write("notes to lastname =\n")
        new_file.write("notes to nationality =\n")
        new_file.write("notes to birthday  (day only)=\n")
        new_file.write("notes to birthmonth  (month only)=\n")
        new_file.write("notes to birthyear  (year only)=\n")
        new_file.write("notes to place of residence (street and number) =\n")
        new_file.write("notes to place of residence (post code) =\n")
        new_file.write("notes to place of residence (town/village) =\n")
        new_file.write("notes to place of residence (country) =\n")
        new_file.write("notes to religion =\n")
        new_file.write("notes to languages spoken =\n")
        new_file.write("notes to job =\n")
        new_file.write("notes to car brand =\n")
        new_file.write("notes to mobile phone =\n")
        new_file.write("\n")
        new_file.write("[physical characteristics] =\n")
        new_file.write("body height (in cm) =\n")
        new_file.write("shoe size =\n")
        new_file.write("body figure =\n")
        new_file.write("hair color =\n")
        new_file.write("eye color =\n")
        new_file.write("\n")
        new_file.write("[notes to physical characteristics] =\n")
        new_file.write("notes to body height =\n")
        new_file.write("notes to shoe size =\n")
        new_file.write("notes to body figure =\n")
        new_file.write("notes to hair color =\n")
        new_file.write("notes to eye color =\n")
        new_file.write("\n")
        new_file.write("[tattoos] =\n")
        new_file.write("tattoo =\n")
        new_file.write("\n")
        new_file.write("[family] =\n")
        new_file.write("mother =\n")
        new_file.write("father =\n")
        new_file.write("brothers =\n")
        new_file.write("sisters =\n")
        new_file.write("\n")
        new_file.write("[personal interests] =\n")
        new_file.write("general interests =\n")
        new_file.write("favorite colors =\n")
        new_file.write("favorite music =\n")
        new_file.write("consumes alcohol =\n")
        new_file.write("vegetarian =\n")
        new_file.write("vegan =\n")
        new_file.write("\n")
        new_file.write("[media interests] =\n")
        new_file.write("tv general =\n")
        new_file.write("tv details =\n")
        new_file.write("\n")
        new_file.write("[pets] =\n")
        new_file.write("pets =\n")
        new_file.write("\n")
        new_file.write("[notes to pets] =\n")
        new_file.write("notes to pets =\n")
        new_file.write("\n")
        new_file.write("[accounts] =\n")
        new_file.write("email addresses =\n")
        new_file.write("mobile number =\n")
        new_file.write("whatsapp mobile number =\n")
        new_file.write("facebook username =\n")
        new_file.write("twitter username =\n")
        new_file.write("instagram username =\n")
        new_file.write("snapchat username =\n")
        new_file.write("skype username =\n")
        new_file.write("other accounts =\n")
        new_file.write("\n")
        new_file.write("[other notes] =\n")
        new_file.write("other notes =\n")
        new_file.close

def define_entry_id():
    entry_id = raw_input("type in the entry id: ")
    entry_path = database_path + entry_id
    isfile = os.path.isfile(entry_path)
    if isfile != True:
        print ""
        print "there is no entry with this id."
        print ""
        press_enter()
        menu()
    print ""
    return entry_id

def define_draft_id():
    draft_id = raw_input("type in the draft id or \"fin\" to go back to menu: ")
    draft_path = database_path + draft_id + ".draft"
    isfile = os.path.isfile(draft_path)
    draft_id_string = str(draft_id)
    if draft_id_string == "fin":
        menu()

    if isfile != True:
        print ""
        print "there is no draft with this id."
        print ""
        press_enter()
        menu()
    print ""
    return draft_id

def define_export_path():
    export_path = "path"
    try_counter = 0
    false = 0

    while os.path.isdir(export_path) != True:
        try_counter = try_counter + 1
        if try_counter > 3:
            print ""
            print "!!!!!! three wrong tries. please start script again. !!!!!!"
            print ""
            quit()
        if false != 0:
            print ""
            print "path does not exist. try again."
            print ""
        export_path = raw_input("enter export path (must end with \"/\"): ")
        false = false + 1
    return export_path

#--------- start define encryption and decryption functions ----------
def hasher(key):
	hash_object = hashlib.sha512(key)
	hexd = hash_object.hexdigest()
	hash_object = hashlib.md5(hexd)
	hex_dig = hash_object.hexdigest()
	return hex_dig

def encrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	cipher = AES.new(secret)
	encoded = EncodeAES(cipher, data)
	return encoded

def decrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
	cipher = AES.new(secret)
	decoded = DecodeAES(cipher, data)
	return decoded
#--------- stop define encryption and decryption functions ----------


#-------------------------------------------------
#--------- start define menu function ------------
#-------------------------------------------------
def print_menu():
    print ""
    print 30 * "-" , "menu" , 30 * "-"
    print "1. view"
    print "2. list all"
    print "3. search"
    print "4. create"
    print "5. edit drafts"
    print "6. change"
    print "7. export"
    print "8. delete"
    print "9. changelog"
    print "10. exit"
    print 67 * "-"

def menu():

    loop=True
    while loop:          ## While loop which will keep going until loop = False
        print_menu()    ## Displays menu
        choice = raw_input("enter your choice [1-7]: ")
        try:
            choice = int(choice)
        except:
            print ""
            print ""
            raw_input("Please enter a number. Enter any key to try again..")
            menu()

        print ""
        print ""
        if choice==1:
            view()
            press_enter()
        elif choice==2:
            list_all(database_path)
            press_enter()
        elif choice==3:
            search()
            press_enter()
        elif choice==4:
            create()
            time.sleep(2.5)
        elif choice==5:
            drafts()
            time.sleep(2.5)
        elif choice==6:
            change()
        elif choice==7:
            export()
        elif choice==8:
            delete()
        elif choice==9:
            changelog()
            press_enter()
        elif choice==10:
            quit()
            loop = False # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            raw_input("Wrong option selection. Enter any key to try again..")
        print ""
        print ""
#-------------------------------------------------
#--------- stop define menu function -------------
#-------------------------------------------------

#-------------------------------------------------
#--------- start define view function ------------
#-------------------------------------------------
def view(entry_id=""):
    print ""
    print 20 * "-", " view object ", 20 * "-"
    print ""

    if entry_id == "":
        entry_id = define_entry_id()

    parser = ConfigParser.ConfigParser()
    object_path = database_path + entry_id
    parser.read(object_path)
    sections = parser.sections()

    for section_name in sections:
        print ""
        print 30 * "-"
        print "[" + section_name + "]"

        option = parser.options(section_name)
        for option_name in option:
            option_value_encrypted = str(parser.get(section_name, option_name))

#----------------- start detect array and encrypt -----------------
            if "=;" in option_value_encrypted:
                print ""
                print option_name + ":"
                option_value_encrypted_array = option_value_encrypted.split(";")
                option_value_encrypted_array_value = []
                for option_value_encrypted_array_value in option_value_encrypted_array:
                    option_value_decrypted = decrypt(enc_password,option_value_encrypted_array_value)
                    print option_value_decrypted
            else:
                print ""
                print option_name + ":"
                option_value_decrypted = decrypt(enc_password, option_value_encrypted)
                print option_value_decrypted
                print ""
#----------------- start detect array and encrypt -----------------
    print ""
    print 53 * "-"
    print ""
#-------------------------------------------------
#--------- stop define view function -------------
#-------------------------------------------------

#-------------------------------------------------
#--------- start define list_all function --------
#-------------------------------------------------
def list_all(dir):
    print 30 * "-"
    print "this are all entrys"
    print 30 * "-"
    print ""
    filename_array = []
    for (elementdirpath, dirnames, filenames) in walk(database_path):
        filename_array.extend(filenames)
        for filename in filename_array:
            if filename != "template":
                parser = ConfigParser.ConfigParser()
                parser.read(database_path + filename)
                entry_id_encrypted = parser.get("entry_id", "entry_id")
                entry1_encrypted = parser.get("identifier","identifier1")
                entry2_encrypted = parser.get("identifier","identifier2")

                entry_id_decrypted = decrypt(enc_password,entry_id_encrypted)
                entry1_decrypted = decrypt(enc_password,entry1_encrypted)
                entry2_decrypted = decrypt(enc_password,entry2_encrypted)

                print entry_id_decrypted + " - " + entry1_decrypted + " " + entry2_decrypted

#-------------------------------------------------
#--------- stop define list_all function ---------
#-------------------------------------------------


#-------------------------------------------------
#--------- start define search function ----------
#-------------------------------------------------
def search():
    search_string = raw_input("which entry id or identifier do you want to search (insert only one string): ")
    search_string_encrypted = encrypt(enc_password, search_string)

    message_bool = True
    filename_array = []

    for (elementdirpath, dirnames, filenames) in walk(database_path):
        filename_array.extend(filenames)

    for filename in filename_array:
        parser = ConfigParser.ConfigParser()
        parser.read(database_path + filename)
        entry_id_encrypted = parser.get("entry_id", "entry_id")
        identifier1_encrypted = parser.get("identifier", "identifier1")
        identifier2_encrypted = parser.get("identifier", "identifier2")

        if entry_id_encrypted == search_string_encrypted or identifier1_encrypted == search_string_encrypted or identifier2_encrypted == search_string_encrypted:
            if message_bool == True:
                print ""
                print 30 * "-"
                print 8 * "-" , "found entry" , 9 * "-"
                print ""
                message_bool = False
            entry_id_decrypted = decrypt(enc_password, entry_id_encrypted)
            identifier1_decrypted = decrypt(enc_password, identifier1_encrypted)
            identifier2_decrypted = decrypt(enc_password, identifier2_encrypted)
            print entry_id_decrypted + " = " + identifier1_decrypted + " " + identifier2_decrypted
    print ""
#-------------------------------------------------
#--------- stop define search function -----------
#-------------------------------------------------

#-------------------------------------------------
#--------- start define draft function -----------
#-------------------------------------------------
def drafts():
    counter = 0
    draft_counter = 0
    for filename in os.listdir(database_path):
        if "draft" in filename:
            draft_counter = draft_counter + 1
            if counter == 0:
                counter = counter + 1
                print 30 * "-"
                print "drafts found"
                print "draft ids are:"
                print ""
                draft_id = filename.replace(".draft", "")
                print draft_id
            else:
                draft_id = filename.replace(".draft", "")
                print draft_id
    if draft_counter == 0:
        print 30 * "-"
        print "no drafts found"
        print 30 * "-"
        return
    print ""
    draft_id = define_draft_id()
    change(draft_id + ".draft")

    configfile = str(database_path + draft_id)
    configfile_draft_string = str(database_path + draft_id + ".draft")
    print ""
    print 42 * "-"
    print "draft finished. draft is no draft anymore."
    print 42 * "-"

    os.rename(configfile_draft_string,configfile)
#-------------------------------------------------
#--------- stop define draft function ------------
#-------------------------------------------------

#-------------------------------------------------
#--------- start define create function ----------
#-------------------------------------------------
def create():

    print 30 * "-" , "create new entry" , 30 * "-"
    print ""
    print "database path is: " + database_path
    print ""
    entry_id = id_generator()
    print "entry id is: " + entry_id
    print ""
    print 76 * "-"
    print ""
    print "seperate multiple answers for one entry with a semicolon (\";\")"
    print ""

    template_path = database_path + "template"
    draft_path = database_path + entry_id + ".draft"
    copyfile(template_path,draft_path)

    parser1 = ConfigParser.ConfigParser()
    object_path = database_path + "template"
    parser1.read(object_path)
    sections = parser1.sections()

    entry_id_encrypted = encrypt(enc_password,entry_id)
    parser2 = ConfigParser.ConfigParser()
    parser2.read(object_path)
    parser2.set("entry_id", "entry_id", entry_id_encrypted)



    for section_name in sections:
        if section_name != "entry_id":

            print ""
            print 30 * "-"
            print "[" + section_name + "]"
            option = parser1.options(section_name)
            for option_name in option:
                value_array = []
                value_array_encrypted = []
                value = raw_input(option_name + ": ")
                if ";" in value:
                    value_array = value.split(";")
                    for element in value_array:
                        value_array_encrypted.append(encrypt(enc_password,element))
                        value_array_encrypted_string = ';'.join(value_array_encrypted)
                    parser2.set(section_name, option_name, value_array_encrypted_string)
                    with open(database_path + entry_id + ".draft", 'w') as configfile_draft:
                        parser2.write(configfile_draft)
                    print "- saved -"
                    print ""
                else:
                    value_encrypted = encrypt(enc_password,value)
                    parser2.set(section_name, option_name, value_encrypted)
                    with open(database_path + entry_id + ".draft", 'w') as configfile_draft:
                        parser2.write(configfile_draft)
                    print "- saved -"
                    print ""
    configfile = str(database_path + entry_id)
    configfile_draft_string = str(database_path + entry_id + ".draft")

    os.rename(configfile_draft_string,configfile)
    print ""
    print 30 * "-" , "finished" , 30 * "-"
    print 30 * "-" , "config written" , 30 * "-"
    print 68 * "-"
    print ""
    print "entry id is: " + entry_id
    print ""
    print 68 * "-"

#------------------------------------------------
#--------- stop define create function ----------
#------------------------------------------------


#------------------------------------------------
#--------- start define change function ---------
#------------------------------------------------
def change(entry_id=""):
    finished_counter = "0"
    if entry_id == "":
        entry_id = define_entry_id()
    while finished_counter == "0":
        parser = ConfigParser.ConfigParser()
        object_path = database_path + entry_id
        parser.read(object_path)
        sections = parser.sections()

    #----------------- start section menu -----------------
        sections_length = len(sections)
        menu_sections_int = 0
        for element in sections:
            menu_sections_int = menu_sections_int + 1
            if len(str(menu_sections_int)) == 1:
                print str(menu_sections_int) + ".  " + str(element)
            if len(str(menu_sections_int)) == 2:
                print str(menu_sections_int) + ". " + str(element)

        section_choice_bool = False
        while section_choice_bool != True or menu_section_choice < 1 or menu_section_choice > sections_length:
            print ""
            menu_section_choice = raw_input("section to change (type in the number) if finished type \"fin\": ")
            if menu_section_choice != "fin":
                try:
                    menu_section_choice = int(menu_section_choice)
                    section_choice_bool = True
                    if menu_section_choice < 1 or menu_section_choice > sections_length:
                        print "the number is to high or to low."
                except:
                    print "please input a number."
            elif menu_section_choice == "fin":
                print menu_section_choice
                return


        section_int = menu_section_choice - 1
        section_choice = sections[section_int]
    #----------------- stop section menu -----------------
        if section_choice == "entry_id":
            print ""
            print "you can't change the entry id!"
            print ""
            press_enter()

        else:
    #----------------- start option menu -----------------
            options = parser.options(section_choice)
            options_length = len(options)

            menu_options_int = 0
            for element in options:
                menu_options_int = menu_options_int + 1
                if len(str(menu_options_int)) == 1:
                    print str(menu_options_int) + ".  " + str(element)
                if len(str(menu_options_int)) == 2:
                    print str(menu_options_int) + ". " + str(element)

            option_choice_bool = False
            while option_choice_bool != True or menu_option_choice < 1 or menu_option_choice > options_length:
                print ""
                menu_option_choice = raw_input("option to change (type in the number): ")
                try:
                    menu_option_choice = int(menu_option_choice)
                    option_choice_bool = True
                    if menu_option_choice < 1 or menu_option_choice > options_length:
                        print "the number is to high or to low."
                except:
                    print "please input a number."
        #----------------- stop option menu -----------------

            option_int = menu_option_choice - 1

            option_choice = options[option_int]
            entry_encrypted = parser.get(section_choice, option_choice)

            entry_array_decrypted = []
            entry_decrypted = ""
            option_choice_array_bool = False

        #----------------- start detect array and encrypt -----------------
            if "=;" in entry_encrypted:
                option_choice_array_bool = True
                entry_encrypted_array = entry_encrypted.split(";")
                for element in entry_encrypted_array:
                    entry_array_decrypted.append(decrypt(enc_password,element))
                    entry_array_decrypted_length = len(entry_array_decrypted)
        #----------------- start detect array and encrypt -----------------

                menu_entry_int = 0
                for element in entry_array_decrypted:
                    menu_entry_int = menu_entry_int + 1
                    if len(str(menu_entry_int)) == 1:
                        print str(menu_entry_int) + ".  " + str(element)
                    if len(str(menu_entry_int)) == 2:
                        print str(menu_entry_int) + ". " + str(element)

                menu_entry_int = menu_entry_int + 1
                if len(str(menu_entry_int)) == 1:
                    print str(menu_entry_int) + ".  " + "add new entry"
                if len(str(menu_entry_int)) == 2:
                    print str(menu_entry_int) + ". " + "add new entry"

                entrys_length = len(entry_array_decrypted)
                entrys_length = entrys_length + 1

                entry_choice_bool = False
                while entry_choice_bool != True or menu_entry_choice < 1 or menu_entry_choice > entrys_length:
                    menu_entry_choice = raw_input("which entry do you want to change (type in the number): ")
                    try:
                        menu_entry_choice = int(menu_entry_choice)
                        entry_choice_bool = True
                        if menu_entry_choice < 1 or menu_entry_choice > entrys_length:
                            print "the number is to high or to low."
                    except:
                        print "please input a number."

                if menu_entry_choice == menu_entry_int:
                    new_value = raw_input("enter new value: ")
                    entry_array_decrypted.append(new_value)
                    entry_array_decrypted_encrypted = []

                    for element in entry_array_decrypted:
                        entry_array_decrypted_encrypted.append(encrypt(enc_password,element))

                    entry_array_decrypted_encrypted_string = ';'.join(entry_array_decrypted_encrypted)

                    parser.set(section_choice, option_choice, entry_array_decrypted_encrypted_string)
                    with open(database_path + entry_id, 'w') as configfile:
                        parser.write(configfile)
                        print ""
                        print 30 * "-" , "finished" , 30 * "-"
                        print 30 * "-" , "config changed" , 30 * "-"

                else:
                    entry_array_decrypted_choice = menu_entry_choice - 1
                    print ""
                    print "seperate multiple answers for one entry with a semicolon (\";\")"
                    print "the current value is: " + entry_array_decrypted[entry_array_decrypted_choice]
                    new_value = raw_input("enter new value: ")
                    entry_array_decrypted[entry_array_decrypted_choice] = new_value
                    entry_array_decrypted_encrypted = []

                    for element in entry_array_decrypted:
                        entry_array_decrypted_encrypted.append(encrypt(enc_password,element))

                    entry_array_decrypted_encrypted_string = ';'.join(entry_array_decrypted_encrypted)

                    parser.set(section_choice, option_choice, entry_array_decrypted_encrypted_string)
                    with open(database_path + entry_id, 'w') as configfile:
                        parser.write(configfile)
                        print ""
                        print 30 * "-" , "finished" , 30 * "-"
                        print 30 * "-" , "config changed" , 30 * "-"


            elif "=;" not in entry_encrypted:
                entry_decrypted = decrypt(enc_password, entry_encrypted)
                print ""
                print "seperate multiple answers for one entry with a semicolon (\";\")"
                print "the current value is: " + entry_decrypted
                new_value = raw_input("enter new value: ")
                new_value_encrypted = encrypt(enc_password,new_value)
                parser.set(section_choice, option_choice, new_value_encrypted)
                with open(database_path + entry_id, 'w') as configfile:
                    parser.write(configfile)
                    print ""
                    print 30 * "-" , "finished" , 30 * "-"
                    print 30 * "-" , "config changed" , 30 * "-"
#------------------------------------------------
#--------- stop define change function ----------
#------------------------------------------------

#-------------------------------------------------
#--------- start define export function ----------
#-------------------------------------------------
def export(entry_id=""):
    print ""
    print 20 * "-", " export object ", 20 * "-"
    print ""

    if entry_id == "":
        entry_id = define_entry_id()

    export_file_path = define_export_path() + entry_id
    export_file_path_txt = export_file_path + ".txt"

    parser = ConfigParser.ConfigParser()
    object_path = database_path + entry_id
    parser.read(object_path)
    sections = parser.sections()

    for section_name in sections:
        print ""
        print 30 * "-"

        line = "[" + section_name + "]"
        f = open(export_file_path_txt,"a")
        f.write("\n")
        f.write(line + "\n")
        f.close()
        print "[" + section_name + "]"

        option = parser.options(section_name)
        for option_name in option:
            option_value_encrypted = str(parser.get(section_name, option_name))

#----------------- start detect array and encrypt -----------------
            if "=;" in option_value_encrypted:
                print ""
                print option_name + ":"
                option_value_encrypted_array = option_value_encrypted.split(";")
                option_value_encrypted_array_value = []
                for option_value_encrypted_array_value in option_value_encrypted_array:
                    option_value_decrypted = decrypt(enc_password,option_value_encrypted_array_value)
                    line = option_name + " = " + option_value_decrypted
                    f = open(export_file_path_txt,"a")
                    f.write(line + "\n")
                    f.close()

                    print option_value_decrypted
                    print ""
            else:
                print ""
                print option_name + ":"
                option_value_decrypted = decrypt(enc_password, option_value_encrypted)
                line = option_name + " = " + option_value_decrypted
                f = open(export_file_path_txt,"a")
                f.write(line + "\n")
                f.close()

                print option_value_decrypted
                print ""
#----------------- stop detect array and encrypt -----------------
    print ""
    print 53 * "-"
    print ""
    print "successfully exported to " + export_file_path_txt
    press_enter()
#-------------------------------------------------
#--------- stop define export function -----------
#-------------------------------------------------

#------------------------------------------------
#--------- start define delete function ---------
#------------------------------------------------
def delete():
    entry_id = define_entry_id()
    print 69 * "-"
    print 12 * "-" + " are you sure you want to delete the object " + 13 * "-" #42chars
    print 69 * "-"
    print 4 * "-" + " IT WILL BE OVERWRITTEN AND IS NOT RECOVERABLE AFTER REMOVAL " + 4 * "-" #59chars
    print 69 * "-"
    print 19 * "-" + " IN EMERGENCYS TYPE \"wipeall\" " + 19 * "-" #31chars
    print 69 * "-"
    print ""
    print ""
    print "are you sure you want to delete the object?"
    security_question = raw_input("if you are sure type \"sure\": ")
    print ""
    security_question_lowercase = security_question.lower()

    if security_question_lowercase == "sure":
        filepath = database_path + entry_id
        file = open(filepath, "wb")
        file.write("1"*os.path.getsize(filepath)) #1
        file.write("0"*os.path.getsize(filepath)) #2
        file.write("1"*os.path.getsize(filepath)) #3
        file.write("0"*os.path.getsize(filepath)) #4
        file.write("1"*os.path.getsize(filepath)) #5
        file.write("0"*os.path.getsize(filepath)) #6
        file.write("1"*os.path.getsize(filepath)) #7
        file.write("0"*os.path.getsize(filepath)) #8
        file.write("1"*os.path.getsize(filepath)) #9
        file.write("0"*os.path.getsize(filepath)) #10
        file.close
        os.remove(filepath)
        print "file has been overwritten and deleted"

    elif security_question_lowercase == "wipeall":
            filename_array = os.listdir(database_path)
            for filename in filename_array:
                filepath = database_path + filename
                file = open(filepath, "wb")
                file.write("1"*os.path.getsize(filepath)) #1
                file.write("0"*os.path.getsize(filepath)) #2
                file.write("1"*os.path.getsize(filepath)) #3
                file.write("0"*os.path.getsize(filepath)) #4
                file.write("1"*os.path.getsize(filepath)) #5
                file.write("0"*os.path.getsize(filepath)) #6
                file.write("1"*os.path.getsize(filepath)) #7
                file.write("0"*os.path.getsize(filepath)) #8
                file.write("1"*os.path.getsize(filepath)) #9
                file.write("0"*os.path.getsize(filepath)) #10
                file.close
                os.remove(filepath)
                print "everthing is wiped"
                quit()
    else:
        print "aborting cause of invalid input."
#------------------------------------------------
#--------- stop define delete function ----------
#------------------------------------------------

def main():
    ascii_art()
    define_database_path()
    define_enc_password()
    check_template()
    menu()

main()
