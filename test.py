obj = Object([50, 50, 50, 50])
    rotation = 10
    for x in range(0, 100):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        screen.fill((0, 0, 0))
        obj.move(rotation)
        obj.draw()
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    sys.exit()