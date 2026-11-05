function love.conf(t)
    t.window.title = "game"
    t.window.icon = "assets/duck.jpg"
    t.window.width = 960
    t.window.height = 540
    t.window.resizable = false
    t.window.minwidth = 100
    t.window.minheight = 100
    t.window.borderless = false
    t.window.vsync = 1
    t.window.display = 1
    t.window.x = 100
    t.window.y = 100
    
    t.identity = "saves"
    --t.version = "1.7.3"
    t.console = true
    t.externalstorage = false
    t.gammacorrect = true
    t.audio.mic = true
    t.modules.timer = true
end