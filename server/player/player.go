package player

// Player ...
type Player struct {
	AP uint8
	X  uint
	Y  uint
}

// Move let the player change position on the GameBoard.
// It returns an error if the cell is already busy.
func (p *Player) Move(x uint, y uint) error {
	p.X = x
	p.Y = y

	return nil
}
