package main

import (
	"log"
	"net"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	connHost, connPort, connType := getServerConfig()

	// Creating TCP Connection
	host := connHost + ":" + connPort
	listeningServer, err := net.Listen(connType, host)
	if err != nil {
		log.Fatal("Error listening:", err.Error())
	}
	defer listeningServer.Close()

	// Server Starting
	log.Printf("Listening on %v:%v\n", connHost, connPort)
	for {
		// Wait Incoming Connections
		conn, err := listeningServer.Accept()
		if err != nil {
			log.Fatal("Error accepting: ", err.Error())
		}
		go handleRequest(conn, 1024)
	}
}

func getServerConfig() (connHost string, connPort string, connType string) {
	err := godotenv.Load(".server.env")

	if err != nil {
		log.Fatal("Error loading .env file")
	}

	connHost = os.Getenv("HOST")
	connPort = os.Getenv("PORT")
	connType = "tcp"

	return
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
	log.Println(string(buffer))
}
