import game

action = 'y'

g = game.Game()

while action == 'y':
	g.loop()
	action = raw_input('Would you like to play again? (y/n)').lower()
	if action == 'n':
		break
	elif action == 'y':
		g.reset()
	else:
		while action != y and action != 'n':
			action = raw_input('Please enter "y" or "n": ').lower()
print 'Quitting...'
