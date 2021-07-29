
import Data.Yaml




filePath = "/home/healer/Public/code/haskell/linux/syncDirectory.yaml"



main = do
    filecontent <- decodeFileThrow  filePath 
    print (filecontent :: Object)