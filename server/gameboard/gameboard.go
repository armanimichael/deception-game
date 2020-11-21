package gameboard

import (
	"dg-server/player"
	"dg-server/user"

	"errors"
	"math/rand"
	"net"
)

// TableSize represents the GameBoard size
const TableSize = 2

// Entity is anything representable inside a Gameboard cell
type Entity struct {
	Name   string
	Player *player.Player
}

// Gameboard represents the Game Board and its content
type Gameboard struct {
	Content [TableSize][TableSize][]Entity
	Turn    *player.Player
}

// NewGameBoard generates a new GameBoard struct
func NewGameBoard(content [TableSize][TableSize][]Entity) *Gameboard {
	return &Gameboard{
		Content: content,
	}
}

// SetGameBoardCell inserts a game object or player inside a cell.
// If the cell if busy and cannot be occupied it returns an error
func (gb *Gameboard) SetGameBoardCell(x uint, y uint, item Entity) (err error) {
	if int(y) >= len(gb.Content) || int(x) >= len(gb.Content[y]) {
		err = errors.New("index out of boundaries")
	}

	gb.Content[y][x] = append(gb.Content[y][x], item)

	err = nil
	return
}

// PopulateGameboard defines a GameBoard grid
func (gb *Gameboard) PopulateGameboard(users map[net.Addr]*user.User) {
	type coords struct {
		x uint
		y uint
	}
	var tempPos []coords

	isTurnSet := false
	for _, u := range users {
		// Set first turn
		if !isTurnSet {
			gb.Turn = u.Player
			isTurnSet = true
		}

		// Setting player coords
		var newCoords coords
		if len(tempPos) != 0 {
			// Generating new Coordinates until they're unique
			findNewCoords := true
			for findNewCoords {
				newCoords = coords{
					x: uint(rand.Int31n(TableSize)),
					y: uint(rand.Int31n(TableSize)),
				}

				// Check for occupied cells
				isCoordUsed := false
				for _, pp := range tempPos {
					if pp.x == newCoords.x && pp.y == newCoords.y {
						isCoordUsed = true
					}
				}
				findNewCoords = isCoordUsed
			}
		} else {
			newCoords.x = uint(rand.Int31n(TableSize))
			newCoords.y = uint(rand.Int31n(TableSize))
		}
		tempPos = append(tempPos, newCoords)

		// Setting Player Coords
		u.Player.X = newCoords.x
		u.Player.Y = newCoords.y

		// Setting Gameboard Cell
		gb.Content[u.Player.Y][u.Player.X] =
			append(gb.Content[u.Player.Y][u.Player.X], Entity{
				Name:   u.Username,
				Player: u.Player,
			})
	}
}
