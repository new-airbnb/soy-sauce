#!/bin/bash

mv config.json config.json.bak
ln -s config.test.json config.json

coverage run --source=house,user,utils -m pytest
coveralls

rm config.json
mv config.json.bak config.json
