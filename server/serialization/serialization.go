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

// DataFromClient represent data sent from Client to Server
type DataFromClient struct {
	playerMove
	playerJoin
}

// NewDataFromClient initializes en empty struct of type DataFromClient
func NewDataFromClient() *DataFromClient {
	return &DataFromClient{}
}

// Decode JSON data to server legible data
func (d *DataFromClient) Decode(conn net.Conn) error {
	decoder := json.NewDecoder(conn)
	return decoder.Decode(d)
}
