function love.conf(game)
    game.window.title = "game"
    game.window.icon = "assets/duck.jpg"
    game.window.width = 960
    game.window.height = 540
    game.window.resizable = false
    game.window.minwidth = 100
    game.window.minheight = 100
    game.window.borderless = false
    game.window.vsync = 1
    game.window.display = 1
    game.window.x = 100
    game.window.y = 100
    
    game.identity = "saves"
    --t.version = "1.7.3"
    game.console = true
    game.externalstorage = false
    game.gammacorrect = true
    game.audio.mic = true
    game.modules.timer = true
end