package serialization

import (
	"encoding/json"
	"io"
)

// Response represents the server response to the client
type Response struct {
	Result     string `json:"result"`
	Message    string `json:"msg"`
	connection io.Writer
}

// NewResponse initializes a Response
func NewResponse(conn io.Writer) *Response {
	return &Response{
		connection: conn,
	}
}

// Encode data to JSON
func (res *Response) Encode(response Response) error {
	encoder := json.NewEncoder(res.connection)
	return encoder.Encode(response)
}
