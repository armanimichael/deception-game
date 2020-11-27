package web

import (
	"bytes"
	"fmt"
	"net"
	"testing"
	"time"
)

const (
	protocol    = "tcp"
	host        = "localhost"
	port        = "1234"
	playerSlots = 2
)

func init() {
	// Start the new server
	srv := NewServer(protocol, host, port, playerSlots)

	go func() {
		if err := srv.Run(false); err != nil {
			fmt.Println("Error running server: ", err)
			return
		}
	}()
}

func TestServerConnection(t *testing.T) {
	// Cannot use wait groups as server.Run() never exists until server closure
	// TODO: find better solution than timeout
	time.Sleep(100 * time.Millisecond)
	conn, err := net.Dial(protocol, host+":"+port)
	if err != nil {
		t.Error("could not connect to server: ", err)
		return
	}
	defer conn.Close()
	conn.Write([]byte(`{"action": "leave"}`)) // Safely leaving server
}

func TestServerResponse(t *testing.T) {
	tests := []struct {
		test     string
		payload  []byte
		expected []byte
	}{
		{
			"Sending valid data",
			[]byte(`{"username":"test"}`),
			[]byte(`{"result":"success","msg":"Server joined."}`),
		},
		{
			"Sending invalid data.",
			[]byte("some unformatted data\n"),
			[]byte(`{"result":"error","msg":"Invalid data format."}`),
		},
	}

	for _, tc := range tests {
		t.Run(tc.test, func(t *testing.T) {
			conn, err := net.Dial(protocol, host+":"+port)
			if err != nil {
				t.Error("could not connect to TCP server: ", err)
				return
			}
			defer conn.Close()
			defer conn.Write([]byte(`{"action": "leave"}`)) // Safely leaving server

			if _, err := conn.Write(tc.payload); err != nil {
				t.Error("could not write payload to TCP server:", err)
			}

			out := make([]byte, 64)

			if _, err := conn.Read(out); err == nil {
				// Convert server response to expected length (for comparison)
				out = out[:len(tc.expected)]
				if bytes.Compare(out, tc.expected) != 0 {
					t.Error("response did match expected output")
				}
			} else {
				t.Error("could not read from connection")
			}
		})
	}
}
