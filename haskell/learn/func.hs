import Turtle     
import qualified Data.Text as T
import Data.Maybe
                 

main = do
    putStrLn "hello world!"
    print "hello world!"

    echo $ fromJust $ textToLine $ T.pack "hello world!"
    echo $ repr "hello world"

    dir <- pwd 
    echo $ repr dir
    time <- date 
    echo $ repr time

    
    -- shell (T.pack "ps -ef |grep firefox")  empty
    -- echo $ repr info
    let cmd = repr "ls"
    -- let cmd = T.pack "firefox"
    -- shell cmd $ repr "/home"
    shell cmd empty 
    shell (T.pack "ls -alh $HOME | grep rc")  empty



    
    