#!/usr/bin/python

##
#
# Copyright 2018 Martin Böhmer
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
##

import configparser
import glob

# Open configuration
config = configparser.ConfigParser()
config.optionxform = str
config.read('tz-drawio.ini', 'utf-8')

# Read settings
settings_section = 'SETTINGS'
images_basedir = config.get(settings_section, "images.basedir")

# Index config
print('Indexing files mentoined in config file')
config_images = set()
# Loop through sections, each representing a library
for lib in config.sections():

	# Skip settings section
	if lib == settings_section:
		continue

	print('|- library: ' + lib)
	
	# Loop through images in section
	for image in config[lib]:
		print(' |- image: ' + image)
		config_images.add(image)


# Index pyhsical images files
print()
print('Scanning for SVG files in ' + images_basedir)
physical_images = set()
svg_files = glob.glob(images_basedir + '/**/*.svg', recursive=True)
for file in svg_files:
	# Strip base dir
	normalized_filename = file[len(images_basedir)+1:]
	# Normlized directory slashes
	normalized_filename = normalized_filename.replace('\\','/')
	print('|- file: ' + normalized_filename)
	physical_images.add(normalized_filename)

# Determine images in config file with no physical match
broken_references = config_images.difference(physical_images)
print()
print('Broken config references: ')
for image in broken_references:
	print('|- broken: ' + image)

# Determine new images
new_images = physical_images.difference(config_images)
print()
print('New file not considered in config')
for image in new_images:
	print('|- new: ' + image)