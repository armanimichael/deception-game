package serialization

import (
	"encoding/json"
	"net"
)

// Response represents the server response to the client
type Response struct {
	Result  string `json:"result"`
	Message string `json:"msg"`
}

// NewResponse initializes an empty struct of type Response
func NewResponse() *Response {
	return &Response{}
}

// Encode data to JSON
func (r *Response) Encode(conn net.Conn) error {
	encoder := json.NewEncoder(conn)
	return encoder.Encode(r)
}
