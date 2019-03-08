#!/bin/bash

mv config.json config.json.bak
ln -s config.test.json config.json

pytest

rm config.json
mv config.json.bak config.json