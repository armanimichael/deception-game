package serialization

import (
	"encoding/json"
	"net"
)

type playerMove struct {
	Action   string `json:"action"`
	Position []uint `json:"pos"`
}

type playerJoin struct {
	Username string `json:"username"`
}

// Request represent data sent from Client to Server
type Request struct {
	playerMove
	playerJoin
}

// NewRequest initializes an empty struct of type Request
func NewRequest() *Request {
	return &Request{}
}

// Decode JSON data to server legible data
func (d *Request) Decode(conn net.Conn) error {
	decoder := json.NewDecoder(conn)
	return decoder.Decode(d)
}
