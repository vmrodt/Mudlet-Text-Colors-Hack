import sys
import os
import shutil


input("Please only use if you know what you're doing")
#if called with no arguments, show usage
if(len(sys.argv) < 2):
	print("Usage: python3", sys.argv[0], 'profile_to_modify', '[themes_directory]')
	sys.exit()

profile_to_modify = sys.argv[1]

#use this themes directory, or use the one passed as argument
themes_directory = "Color_Themes"
if(len(sys.argv) > 2):
	themes_directory = sys.argv[2]


if not os.path.isdir(themes_directory):
	print("not a valid themes directory")
	sys.exit()


#list themes for user to choose one
theme_list = os.listdir(themes_directory)
theme_list.sort()
i = 1
for theme in theme_list:
	print(i, ") ", theme)
	i = i + 1
chosen_theme = int(input("Choose the theme you want to use: ")) - 1 # -1 because list starts from 0 and listing from 1


#open the files
tmpfile = "newtmpfile.tmp"
filetomod_fh = open(profile_to_modify, 'r')
themefile_fh = open(os.path.join(themes_directory, theme_list[chosen_theme]), 'r')
newfile_fh = open(tmpfile, 'w')


#XX read the colors from the color theme file into a list XX


#read the colors theme file into a dictionary
theme_colors_dict = {}
for line in themefile_fh:
	#print(line)
	pair = line.split()
	theme_colors_dict[pair[0]] = pair[1]


# change the colors
# assumes the colors are between the <HostPackages> xml tags in the profile file, and only changes the colors there.
section_start_found = False
section_end_found = False
for line in filetomod_fh:		
	new_line = line
	if not section_start_found:
		if "<HostPackage>" in line:
			section_start_found = True
	elif not section_end_found:
		if "</HostPackage>" in line:
			section_end_found = True		
		color_found = False	
		for color in theme_colors_dict:			
			if color in line:
				hash_position = line.find("#")
				new_line = line[:hash_position] + theme_colors_dict[color] + line[hash_position + 7:]
				color_found = True
				break
	newfile_fh.write(new_line)
		

answer = input("Overwrite the profile, and make a backup? (Y/N) ")
if answer == "Y" or answer == "y":
	shutil.copy2(profile_to_modify, profile_to_modify + ".backup")
	shutil.copy2(tmpfile, profile_to_modify)
	
else:
	print("The modified copy is: ", tmpfile)
	


newfile_fh.close()
themefile_fh.close()
filetomod_fh.close()



