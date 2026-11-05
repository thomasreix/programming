-- Game Development with LÖVE 2D and Lua
-- https://www.youtube.com/watch?v=I549C6SmUnk

-- this is a comment
--[[
    this
    is
    a
    multiline
    comment
]]

print("Hello World")

print("start", "finish") -- , will seperate with a tab
print("concatenate ".."is concatenated") -- use .. to concatenate

var = nil
num = 5
str = "yes"
bool = true
tabl = { 1, 2, 3}

local square = 49 -- initialise a variable
local root = math.sqrt(square)
print(square.." is the square of "..root)

local one, two, three = true, 2, "three"

local text = [[
    this text
is
        a string
]]

print("sample text:\n"..text)

local animal = "crocodile"
local letters = #animal -- # gets the lenth
print(animal.." has "..letters.." letters")

local num = 20
local str = tostring(num) -- converts a variable to a string
print(str.." is a "..type(str))
print()

print("newline:\nmore text")      -- \n adds a newline
print("tab:\tmore text")          -- \t adds a tab
print("vertical tab:\vmore text") -- \v adds a vertical tab
print("backslash: \\")            -- \\ adds a literal backslash
print("quote: \"")                -- \" adds a quote

local word = "Water Fountain"
print("normal: "..word)
print("uppercase: "..string.upper(word))
print("lowercase: "..string.lower(word))
print("characters: "..string.len(word))
print()

local numX = 3
local numY = 7

local numA = numX + numY -- adition
print(numX.." + "..numY.." = "..numA)

local numS = numY - numX  -- substraction
print(numY.." - "..numX.." = "..numS)

local numM = numX * numY -- multiplication
print(numX.." * "..numY.." = "..numM)

local numD = numY / numX -- division
print(numY.." / "..numX.." = "..numD)

local numP = numY ^ numX -- power
print(numY.." ^ "..numX.." = "..numP)

local numN = numY % numX -- modulo
print(numY.." % "..numX.." = "..numN)

local numL = math.max(numX, numY) -- max returns the greatest value
local numK = math.min(numX, numY) -- min returns the smallest value
print(numL.." > "..numK)

local numC = math.ceil(numD) -- ceil rounds up
print(numY.." / "..numX.." <= "..numC)

local numF = math.floor(numD) -- floor rounds down
print(numY.." / "..numX.." >= "..numF)

math.randomseed(os.time()) -- set the random seed

local numQ = math.random() -- random retuns a random number between 0 and 1
print(numQ.." is random")

local numR = math.random(numX, numY) -- random retuns a random number between a specified range
print(numR.." is a random integer")

local pi = math.pi
print("pi: "..pi)

print()

local raining = false
if raining then -- use if to execute code when a statement is true
    print("it's raining")
elseif not raining then -- use elseif to execute code when a statement is true
    print("it's not raining") -- and all previous statement are false
else -- use else to execute code when all previous statements are false
    print("there are not clouds")
end

local temperature = 16
if temperature > 40 then -- use > for bigger
    print("it's melting")
elseif temperature >= 28 then -- use >= for bigger or equal
    print("it's hot")
elseif temperature == 20 then -- use == for equal
    print("it's chill")
elseif temperature < 20 then -- use < for smaller
    print("it's cold")
elseif temperature ~= 0 then -- use ~= for not equal
    print("it's melting or freezing")
elseif temperature <= 4 then -- use <= for smaller or equal
    print("it's freezing")
else
    print("it's good")
end

local cloudy = true
if cloudy and raining then -- use and to check to both are true
    print("it's a thunderstorm")
elseif not raining and cloudy then -- use not to invert a statement
    print("it's cloudy")
elseif cloudy or raining then -- use or to check if ether is true
    print("it's a bad weather")
elseif not(cloudy and raining) then -- use not before brakets to invert it
    print("it's sunny")
else
    print("it's a tornado")
end

local weather = cloudy and "stay at home" or "go outside"
print("you should "..weather)