local function Spaceship(debugging)
    local size = 30
    local orientation = math.pi / 2

    local screen = {
        width = love.graphics.getWidth(),
        height = love.graphics.getHeight()
    }

    return {
        position = {
            x = screen.width / 2,
            y = screen.height / 2,
        },
        radius = size / 2,
        orientation = orientation,
        thrusting = false,
        thrust = {
            x = 0,
            y = 0,
            speed = 500,
            big_flame = false,
            flame = 2.0
        },
        drawFlame = function (self, fillType, color)
            love.graphics.setColor(color)

            love.graphics.polygon(
                fillType,
                self.position.x - self.radius * (((2 / 3) * math.cos(self.orientation)) + math.sin(self.orientation) / 2),
                self.position.y + self.radius * (((2 / 3) * math.cos(self.orientation)) - math.sin(self.orientation) / 2),
                self.position.x - self.radius * self.thrust.flame + math.cos(self.orientation),
                self.position.y + self.radius * self.thrust.flame + math.cos(self.orientation),
                self.position.x - self.radius * (((2 / 3) * math.cos(self.orientation)) - math.sin(self.orientation) / 2),
                self.position.y + self.radius * (((2 / 3) * math.cos(self.orientation)) + math.sin(self.orientation) / 2)

            )
        end,

        draw = function (self, dt)
            local opacity = 1

            if self.thrusting then
            --     if not self.thrust.big_flame then
            --         self.thrust.big_flame = self.thrust.big_flame - 1 * dt
            --     end

                self:drawFlame("fill", {1, 0.5, 0.1})
            end

            if debugging then
                love.graphics.setColor(1, 0, 0)
                love.graphics.rectangle("fill", self.position.x - 1, self.position.y -2, 2, 2)
                love.graphics.circle("line", self.position.x, self.position.y, self.radius)
            end

            love.graphics.setColor(1, 1, 1, opacity)
            love.graphics.polygon(
                "line",
                self.position.x + ((4 / 3) * self.radius) * math.cos(self.orientation),
                self.position.y - ((4 / 3) * self.radius) * math.sin(self.orientation),
                self.position.x - self.radius * ((2 / 3) * math.cos(self.orientation) + math.sin(self.orientation)),
                self.position.y + self.radius * ((2 / 3) * math.sin(self.orientation) - math.cos(self.orientation)),
                self.position.x - self.radius * ((2 / 3) * math.cos(self.orientation) - math.sin(self.orientation)),
                self.position.y + self.radius * ((2 / 3) * math.sin(self.orientation) + math.cos(self.orientation))
            )
        end,
        move = function(self, dt)
            local friction = 0.95
            local drag = math.exp(-friction * dt)

            if self.thrusting then
                self.thrust.x = self.thrust.x + self.thrust.speed * math.cos(self.orientation) * dt
                self.thrust.y = self.thrust.y - self.thrust.speed * math.sin(self.orientation) * dt
            else
                self.thrust.x = self.thrust.x * drag
                self.thrust.y = self.thrust.y * drag
            end

            self.rotation = 2 * math.pi * dt

            if love.keyboard.isDown("left") then
                self.orientation = self.orientation + self.rotation
            end
            if love.keyboard.isDown("right") then
                self.orientation = self.orientation - self.rotation
            end

            if self.thrusting then
                self.thrust.x = self.thrust.x + self.thrust.speed * math.cos(self.orientation) * dt
                self.thrust.y = self.thrust.y - self.thrust.speed * math.sin(self.orientation) * dt
            else
                self.thrust.x = self.thrust.x * friction
                self.thrust.y = self.thrust.y * friction
            end

            self.position.x = self.position.x + self.thrust.x * dt
            self.position.y = self.position.y + self.thrust.y * dt
        end

    }
end

return Spaceship