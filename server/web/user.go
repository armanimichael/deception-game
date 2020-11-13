package web

import "net"

// User represent a connected client
type User struct {
	// TODO: UUID Maybe?
	Conn     net.Conn
	Username string
}
