

data Apple = Apple {
    size :: Int ,
    shape :: String,
    count :: Int
} deriving (Show)

-- one = Apple {size = 12, shape = "round", count = 1}

-- getSize = size one

-- data Banala = Banala Int String Int deriving (Show)

new = map (Apple 11  "round")  [1..10]

data Person = Person { age :: Int  
                     , height :: Float  
                     , phoneNumber :: String  
                     } deriving (Show)   

classes = map (Person 20 170) ["4532232", "9023482", "0923842"]
