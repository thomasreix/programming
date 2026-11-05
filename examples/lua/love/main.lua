love = require("love")

local function color(r, g, b)
    if r < 6 and r >= 0 and g < 6 and g >= 0 and b < 6 and b >= 0 then
        return {(r * 48 + 15) / 255, (g * 48 + 15) / 255, (b * 48 + 15) / 255}
    end
end


function love.load()
    backgroundColor = color(2, 1, 2)
    love.graphics.setBackgroundColor(backgroundColor)

    alpha = {1, 1, 1, 1}

    rectangleColor = color(1, 3, 3)
    circleColor = color(0, 0, 1)

    pacman = {}
    pacman.x, pacman.y = 100, 200
    pacman.speed = 5
    pacman.ate = false
    pacman.mouth = 0
    pacman.chew = true
    pacman.chewingSpeed = 0.035
    pacmanColor = color(5, 5, 0)

    ghost = {}
    ghost.x, ghost.y = 700, 200
    ghost.size = 50
    ghostColor = color(5, 5, 5)

    tank = {}
    tank.x, tank.y = 300, 20
    tank.size = 50
    tank.speed = 5
    tank.direction = 0
    tankColor = color(0, 1, 1)
    canonColor = color(0, 2, 1)

    kirby = {}
    kirby.scale = 5
    kirby.speed = 5
    kirby.delay = 5
    kirby.tick = 1
    kirby.sprite = {}
    kirby.sprite.sheet = love.graphics.newImage("assets/kirby.png")
    kirby.sprite.sheet:setFilter("nearest", "nearest")
    kirby.sprite.size = 16
    kirby.sprite.amount = 2
    for i = 1, kirby.sprite.amount do
        kirby.sprite[i] = love.graphics.newQuad(kirby.sprite.size * (i - 1), 0, kirby.sprite.size, kirby.sprite.size, kirby.sprite.size * kirby.sprite.amount, kirby.sprite.size)
    end
    kirby.animation = {}
    kirby.direction = "right"
    kirby.idle = true
    kirby.sprite.current = 1
    kirby.size = kirby.scale * kirby.sprite.size
    kirby.jump = false
    kirby.position = {}
    kirby.position.x, kirby.position.y = 960 - kirby.size / 2, 460 - kirby.size / 2
    kirby.velocity = {}
    kirby.velocity.x, kirby.velocity.y = 1, 0

end

function love.update(dt)
    pacman.x = pacman.x + pacman.speed

    if pacman.x >= ghost.x - ghost.size then
        pacman.ate = true
    end

    if pacman.chew then
        pacman.mouth = pacman.mouth - pacman.chewingSpeed
    else
        pacman.mouth = pacman.mouth + pacman.chewingSpeed
    end

    if pacman.mouth <= 0 then
        pacman.chew = false
    elseif pacman.mouth > 1 then
        pacman.chew = true
    end

    if love.keyboard.isDown("j") then
        tank.x = tank.x - tank.speed
    end
    if love.keyboard.isDown("l") then
        tank.x = tank.x + tank.speed
    end
    if love.keyboard.isDown("i") then
        tank.y = tank.y - tank.speed
    end
    if love.keyboard.isDown("k") then
        tank.y = tank.y + tank.speed
    end

    if love.keyboard.isDown("right") or love.keyboard.isDown("left")then
        kirby.idle = false
    else
        kirby.idle = true
    end

    if love.keyboard.isDown("right") and kirby.x < 960 - kirby.size then
        kirby.position.x = kirby.position.x + kirby.speed
    end
    if love.keyboard.isDown("left") and kirby.x > 0 then
        kirby.position.x = kirby.position.x - kirby.speed
    end

    kirby.position.x = kirby.position.x + kirby.speed

    kirby.tick = kirby.tick + 1
    if kirby.tick > kirby.delay then
        kirby.tick = 1
        if not kirby.idle then
            kirby.sprite.current = kirby.sprite.current % kirby.sprite.amount + 1
        else
            kirby.sprite.current = 1
        end
    end

    if love.keyboard.isDown("space") and kirby.position.y == 460 then
        kirby.jump = true
    end

    if kirby.jump then
        kirby.velocity.y = 3 
    end
end

function love.draw()
    love.graphics.setColor(rectangleColor) -- use setColor to set the default color
    love.graphics.rectangle("line", 20, 20, 80, 50) -- use line for the ouline of the rectangle
    love.graphics.rectangle("fill", 120, 20, 80, 50) -- use fill to fill the rectangle

    love.graphics.setColor(circleColor)
    love.graphics.circle("line", 200, 100, 300)

    if not pacman.ate then
        love.graphics.setColor(ghostColor)
        love.graphics.circle("fill", ghost.x, ghost.y, ghost.size)
    end

    love.graphics.setColor(pacmanColor)
    love.graphics.arc("fill", pacman.x, pacman.y, 100, pacman.mouth, 2 * math.pi - pacman.mouth)

    love.graphics.setColor(tankColor)
    love.graphics.rectangle("fill", tank.x, tank.y, tank.size, tank.size)
    love.graphics.setColor(canonColor)
    love.graphics.rectangle("fill", tank.x + (tank.size / 3) , tank.y - (tank.size/ 3), (tank.size / 3), tank.size)

    love.graphics.setColor(alpha)
    love.graphics.draw(kirby.sprite.sheet, kirby.sprite[kirby.sprite.current], kirby.x, kirby.y, 0, kirby.scale, kirby.scale)
end

