#!/bin/bash

if pip freeze | grep -q "poetry"; then
    echo "Poetry is installed"
else
    pip install poetry 
fi
