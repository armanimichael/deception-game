package gameboard

import (
	"dg-server/player"
	"dg-server/web"
	"errors"
	"math/rand"
)

// TableSize represents the GameBoard size
const TableSize = 8

// Entity is anything representable inside a Gameboard cell
type Entity struct {
	Name   string
	Player *player.Player
}

// Gameboard represents the Game Board and its content
type Gameboard struct {
	Content [TableSize][TableSize][]Entity
}

// NewGameBoard generates a new GameBoard struct
func NewGameBoard(content [TableSize][TableSize][]Entity) *Gameboard {
	return &Gameboard{
		Content: content,
	}
}

// SetGameBoardCell inserts a game object or player inside a cell.
// If the cell if busy and cannot be occupied it returns an error
func (gb *Gameboard) SetGameBoardCell(x int, y int, item Entity) (err error) {
	if y >= len(gb.Content) || x >= len(gb.Content[y]) {
		err = errors.New("index out of boundaries")
	}

	gb.Content[y][x] = append(gb.Content[y][x], item)

	err = nil
	return
}

// PopulateGameboard defines a GameBoard grid
func (gb *Gameboard) PopulateGameboard(users []web.User) {
	type coords struct {
		x uint
		y uint
	}
	var tempPos []coords

	for _, user := range users {
		var newCoords coords
		if len(tempPos) != 0 {
			isCoordUsed := true
			for isCoordUsed {
				newCoords = coords{
					x: uint(rand.Int31n(TableSize)),
					y: uint(rand.Int31n(TableSize)),
				}

				temp := false
				for _, pp := range tempPos {
					if pp.x == newCoords.x && pp.y == newCoords.y {
						temp = true
					}
				}
				isCoordUsed = temp
			}
		} else {
			newCoords.x = uint(rand.Int31n(TableSize))
			newCoords.y = uint(rand.Int31n(TableSize))
		}
		tempPos = append(tempPos, newCoords)

		user.Player.X = newCoords.x
		user.Player.Y = newCoords.y

		// Setting Gameboard Cell
		gb.Content[newCoords.y][newCoords.x][0] = Entity{
			Name:   user.Username,
			Player: user.Player,
		}
	}
}
