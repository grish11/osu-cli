#!/bin/bash

echo "installing chopped latency-checker..."

# creating folder, move the script into ~/.local/bin, then remove 
mkdir -p ~/.local/bin
mv latency-check ~/.local/bin/latency-check
chmod +x ~/.local/bin/latency-check

# based on shell, add ~/.local/bin in PATH if not in PATH
if [[ $SHELL == *"bash"* ]]; then
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        echo "added ~/.local/bin to PATH in ~/.bashrc"
        echo "run: source ~/.bashrc"
    fi
elif [[ $SHELL == *"zsh"* ]]; then
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        echo "added ~/.local/bin to PATH in ~/.zshrc"
        echo "run: source ~/.zshrc"
    fi
else 
    echo "could not detect shell, this install only works with zsh and bash"
    echo "manually add ~/.local/bin to your PATH"
fi

echo "done! try running: latency-check"



