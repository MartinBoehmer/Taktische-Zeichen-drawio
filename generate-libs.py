#!/usr/bin/python

##
#
# Copyright 2017 Martin Böhmer
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
##

import configparser
import os
import json
import base64
import re
import xml.etree.ElementTree
import urllib.parse

# Open configuration
config = configparser.ConfigParser()
config.optionxform = str
config.read('tz-drawio.ini', 'utf-8')

# Read settings
settings_section = 'SETTINGS'
images_basedir = config.get(settings_section, "images.basedir")
temp_dir = config.get(settings_section, "temp.dir")
dist_dir = config.get(settings_section, "dist.dir")
dist_dir_url = config.get(settings_section, "dist.dir.url")
fontfamily_source = config.get(settings_section, "font_family.source")
fontfamily_target = config.get(settings_section, "font_family.target")
debug_mode = config.getboolean(settings_section, "debug_mode")
shortcut_base_url = config.get(settings_section, "shortcut.base_url")
uber_lib_name = config.get(settings_section, "uber_lib.name")

# Create directories
os.makedirs(dist_dir, exist_ok=True)
if debug_mode:
	os.makedirs(temp_dir, exist_ok=True)
	
uber_library_items = []
	
# Loop through sections, each representing a library
for lib in config.sections():

	# Skip settings section
	if lib == settings_section:
		continue

	print('Generating library: ' + lib)

	# Init library container
	library_items = []
		
	# Loop through images in section
	for image in config[lib]:
		
		# Determine paths
		image_source_path = os.path.join(images_basedir, image)
		image_target_path = os.path.join(temp_dir, image)
		image_target_dir = os.path.dirname(image_target_path)
		# Create output dir, when in debug mode
		if debug_mode:
			os.makedirs(image_target_dir, exist_ok=True)
		
		print('|- Processing image: ' + image)
		
		# Parse XML
		xml.etree.ElementTree.register_namespace('', "http://www.w3.org/2000/svg")
		namespaces = {'svg': 'http://www.w3.org/2000/svg'}
		image_xml = xml.etree.ElementTree.parse(image_source_path);
		svg_root = image_xml.getroot()
		
		# Get image dimensions from XML
		image_width = int(svg_root.attrib.get('width', -1))
		image_height = int(svg_root.attrib.get('height', -1))
		if image_width <= 0 and image_height > 0:
			image_width = image_height
			svg_root.attrib['width'] = image_width
		elif image_height <= 0 and image_width > 0:
			image_height = image_width
			svg_root.attrib['height'] = image_height
		elif image_width + image_height <= 0:
			assert (False), "Width and height unset for image: " + image_source_path
		# Set viewbox, if not set (required by draw.io)
		image_viewbox = svg_root.attrib.get('viewBox', '')
		image_has_viewbox = (image_viewbox != '')
		if not image_has_viewbox:
			image_viewbox = '0 0 ' + str(image_width) + ' ' + str(image_height)
			svg_root.attrib['viewBox'] = image_viewbox
		
		# The XML tree cannot be used for generating the target XML as the images contain CDATA elements, which get lost using the ElementTree
		##image_data = xml.etree.ElementTree.tostring(svg_root, encoding='utf-8').decode()
		
		# So, open the original image source file and read it again as into a string
		with open(image_source_path, mode='r', encoding='utf-8') as image_source_file :
			image_data = image_source_file.read()
		
		# Replace XML header, because it is not tolerated by draw.io (sad, but true)
		image_data = re.sub(r'<\?xml[^>]+\?>\s?', '', image_data, flags=re.IGNORECASE)
		# Replace DTD, if present, because it is not tolerated by draw.io (sad, but true)
		image_data = re.sub(r'<!DOCTYPE[^>]+>\s?', '', image_data, flags=re.IGNORECASE)
		# Replace font familiy, if specified (this may be necessary in case CSS-based font settings are not compatible with some browsers)
		if fontfamily_source and fontfamily_target:
			# Remove style definitions related to the font famility to be replaced (smaller symbol file)
			image_data = re.sub(r'\@font-face[ ]*\{[^\}]+' + fontfamily_source + '[^\}]+\}', '', image_data, flags=re.IGNORECASE)
			image_data = image_data.replace(fontfamily_source, fontfamily_target)
			# Alternative, more restricted replacment
			#image_data = re.sub(r'(font-family[ ]*=[ ]*)"' + fontfamily_source + '"', r'\1"' + fontfamily_target + '"', image_data, flags=re.IGNORECASE)
		
		# Trim
		image_data = image_data.strip()
		# XML-escape line breaks as required by draw.io (otherwise library will not work properly)
		image_data = image_data.replace("\n", "&#xa;")
		# Add viewBox, if found missing
		if not image_has_viewbox:
			image_data = re.sub(r'(<svg[^>]+)>', r"\1" + ' viewBox="' + image_viewbox + '">', image_data, 1)
		
		# Output modified image, when in debug mode
		if debug_mode:
			with open(image_target_path, mode='w', encoding='utf-8') as image_target_file:
				image_target_file.write(image_data)
		
		# Gather image data to create library item
		image_base64 = base64.b64encode(image_data.encode())
		library_item = {}
		library_item['data'] = 'data:image/svg+xml;base64,' + image_base64.decode('utf-8')
		library_item['w'] = image_width
		library_item['h'] = image_height
		library_item['title'] = config.get(lib, image)
		library_item['aspect'] = 'fixed'
		library_items.append(library_item)
		
	# Save libray to file
	library_path = os.path.join(dist_dir, lib + ".xml")
	with open(library_path, mode='w', encoding='utf-8') as library_file:
		json_indent = 4 if debug_mode else None
		library_json = json.dumps(library_items, indent=json_indent)
		library_file.write('<mxlibrary>')
		library_file.write(library_json)
		library_file.write('</mxlibrary>')
	# Add library items to uber lib
	uber_library_items.extend(library_items)
		
	# Output shortcut URLs for adding library to draw.io (debug mode only)
	if debug_mode:
		library_shortcut_path = os.path.join(temp_dir, lib + ".txt")
		library_url = dist_dir_url + lib + ".xml"
		# Note: URLs need to be double-encoded to work (expect transport specification part, e.g. https://)
		library_url = urllib.parse.quote(library_url, safe='/:')
		library_url = urllib.parse.quote(library_url)
		library_shortcut_url = shortcut_base_url + 'U' + library_url
		with open(library_shortcut_path, mode='w', encoding='utf-8') as library_shotcut_file:
			library_shotcut_file.write(library_shortcut_url + '\n')
		# Markup (for README.md)
		with open(os.path.join(temp_dir, 'shortcuts.md'), mode='a', encoding='utf-8') as shortcuts_markup_file:
			shortcuts_markup_file.write('- [' + lib + '](' + library_shortcut_url + ')\n')
			
	print()

# Save uber lib
print('Generating uber library: ' + uber_lib_name)
uber_library_path = os.path.join(dist_dir, uber_lib_name + ".xml")
with open(uber_library_path, mode='w', encoding='utf-8') as library_file:
	json_indent = 4 if debug_mode else None
	library_json = json.dumps(uber_library_items, indent=json_indent)
	library_file.write('<mxlibrary>')
	library_file.write(library_json)
	library_file.write('</mxlibrary>')

print()
print('Done.')
