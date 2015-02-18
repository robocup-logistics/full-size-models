#!/usr/bin/python

import os

model_file_extensions = ('dae','blend','wrl','stp','stl')

script_note = "<!---\r\n This file is automatically generated by the script 'create_preview_list.py'. Any changes will be lost \r\n-->\r\n\r\n"

def walk_dir_rec(level, curr_dir):
	fileContent = ""

	if level > 1:
		#process files in current dir:

		fileContent += '#' * level + " " + os.path.basename(curr_dir) + "\r\n\r\n"

		previewFile = ""
		modelFiles = ""
		for filename in sorted(os.walk(curr_dir).next()[2]):
			if filename.lower() == "preview.png":
				previewFile = "![{0}]({1})\r\n".format(os.path.basename(curr_dir), curr_dir[2:] + "/" + filename)
			elif filename.lower().endswith(model_file_extensions):
				modelFiles += "* [{0}]({1}?raw=true)\r\n".format(filename, curr_dir[2:] + "/" + filename)

		if len(modelFiles) > 0:
			fileContent += previewFile + "\r\n" + modelFiles + "\r\n"

	for dirname in sorted(os.walk(curr_dir).next()[1]):
		if any(dirname in s for s in ['.git', 'textures']):
			continue

		fileContent += walk_dir_rec(level+1,os.path.join(curr_dir,dirname))

		if level == 1:
			fileContent += "_____________\r\n"

	if level > 1:
		f = open(os.path.join(curr_dir,"README.md"), 'w+')
		f.write(script_note + fileContent.replace("("+curr_dir[2:]+"/","("))    
		f.close()



	return fileContent;

def walk_dirs(base):
	return script_note + "# Model list & preview\r\n\r\n" + walk_dir_rec(1,base)


if __name__ == "__main__":
	print("Creating PREVIEW.md")
	f = open("PREVIEW.md", 'w+')
	f.write(walk_dirs('.'))    
	f.close()
	print("File created and saved.")
