local Spaceship = require "Spaceship"

local screen = {
    width = love.graphics.getWidth(),
    height = love.graphics.getHeight()
}

function love.load()
    love.mouse.setVisible(false)
    mouse = {x = 0, y = 0}

    local debugging = false
    spaceship = Spaceship(debugging)
end

function love.keypressed(key)
    if key == "up" then
        spaceship.thrusting = true
    end
end

function love.keyreleased(key)
    if key == "up" then
        spaceship.thrusting = false
    end
end

function love.update(dt)
    mouse = love.mouse.getPosition()

    spaceship:move(dt)

end

function love.draw(dt)
    spaceship:draw(dt)
end