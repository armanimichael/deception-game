package user

import (
	"dg-server/player"
	"net"
)

// User represent a connected client
type User struct {
	// TODO: UUID Maybe?
	Conn     net.Conn
	Username string
	Player   *player.Player
}

// GetConn ...
func (u *User) GetConn() net.Conn {
	return u.Conn
}

// GetUsername ...
func (u *User) GetUsername() string {
	return u.Username
}

// GetPlayer ...
func (u *User) GetPlayer() *player.Player {
	return u.Player
}
