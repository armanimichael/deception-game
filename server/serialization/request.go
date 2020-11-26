package serialization

import (
	"encoding/json"
	"errors"
	"io"
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
	connection io.Reader
}

// NewRequest initializes a Request
func NewRequest(conn io.Reader) *Request {
	return &Request{
		connection: conn,
	}
}

// Decode JSON data to server legible data
func (req *Request) Decode() error {
	decoder := json.NewDecoder(req.connection)

	err := decoder.Decode(req)
	if req.Username == "" {
		err = errors.New("username cannot be an empty string")
	}
	return err
}
