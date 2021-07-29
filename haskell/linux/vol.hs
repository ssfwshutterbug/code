{-# LANGUAGE OverloadedStrings #-}

import Turtle


-- simple haskell program get system volume
main = shell "pamixer --get-volume" empty


