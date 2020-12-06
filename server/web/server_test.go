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
	bufferSize  = 1024
)

type testFormat struct {
	test     string
	payload  []byte
	expected []byte
}

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
	tests := []testFormat{
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

	testMultipleConn(t, tests, true)
}

func TestMultipleUsersConn(t *testing.T) {
	tests := []testFormat{
		{
			"Connecting 1# player",
			[]byte(`{"username":"test-0"}`),
			[]byte(`{"result":"success","msg":"Server joined."}`),
		},
		{
			"Connecting with cloned username",
			[]byte(`{"username":"test-0"}`),
			[]byte(`{"result":"error","msg":"This username is either invalid or already in use."}`),
		},
		{
			"Connecting 2# player",
			[]byte(`{"username":"test-1"}`),
			[]byte(`{"result":"success","msg":"Server joined."}`),
		},
		{
			"Connecting player over limit",
			[]byte(`{"username":"test-2"}`),
			[]byte(`{"result":"error","msg":"Server Full."}`),
		},
	}

	testMultipleConn(t, tests, false)
}

func testMultipleConn(t *testing.T, tests []testFormat, closeConn bool) {
	for _, tc := range tests {
		t.Run(tc.test, func(t *testing.T) {
			conn, err := net.Dial(protocol, host+":"+port)
			if err != nil {
				t.Error("could not connect to TCP server: ", err)
				return
			}

			// For testing server overpopulation or multiple opened connections
			if closeConn {
				defer conn.Close()
				defer conn.Write([]byte(`{"action": "leave"}`)) // Safely leaving server
			}

			if _, err := conn.Write(tc.payload); err != nil {
				t.Error("could not write payload to TCP server:", err)
			}

			out := make([]byte, bufferSize)

			if _, err := conn.Read(out); err == nil {
				// Convert server response to expected length (for comparison)
				outNorm := out[:len(tc.expected)]
				if bytes.Compare(outNorm, tc.expected) != 0 {
					t.Errorf("response did match expected output: \n\r\texpected: %v\n\r\tresponse %v", string(tc.expected), string(out))
				}
			} else {
				t.Error("could not read from connection")
			}
		})
	}
}
