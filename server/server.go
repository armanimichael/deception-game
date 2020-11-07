package main

import (
	"log"
	"net"
	"os"
)

const (
	connHost = "127.0.0.1"
	connPort = "1234"
	connType = "tcp"
)

func main() {
	// Creating TCP Connection
	const host = connHost + ":" + connPort
	listeningServer, err := net.Listen(connType, host)
	if err != nil {
		log.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	defer listeningServer.Close()

	log.Printf("Listening on %v:%v\n", connHost, connPort)
	for {
		// Wait Incoming Connections
		conn, err := listeningServer.Accept()
		if err != nil {
			log.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		go handleRequest(conn, 1024)
	}
}

// Handles incoming requests
func handleRequest(conn net.Conn, bufferSize int) {
	// Connection Data Buffer
	buffer := make([]byte, bufferSize)

	// Read Connection Data
	_, err := conn.Read(buffer)
	defer conn.Close()
	if err != nil {
		log.Println("Error reading:", err.Error())
	}

	// Responding
	conn.Write([]byte("Message received."))
}
