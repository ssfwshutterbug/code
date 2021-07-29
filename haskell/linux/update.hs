{-# LANGUAGE OverloadedStrings #-}

import Turtle

main = do
    shell "sudo pacman -Sy &>/dev/null" empty
    shell "echo `pacman -Qu |wc -l` update" empty
