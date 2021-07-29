import Turtle
import qualified Data.Text as T

cmd1 = "mplayer ~/Public/sound/ding.wav &"
cmd2 = "echo ${@} | tr -d '\n'"
-- cmd3 = "mplayer http://dict.youdao.com/dictvoice\?audio\=cmd2 &>/dev/null  &"
cmd4 = "ydcv -n -t 5 cmd2"

main = do
    shell (T.pack cmd1) empty
    shell (T.pack cmd2) empty
    shell (T.pack cmd4) empty

