package main

import (
	"dg-server/web"
	"log"
)

func main() {
	const (
		connType    = "tcp"
		connHost    = "localhost"
		connPort    = "1234"
		playerSlots = 2
	)

	srv := web.NewServer(connType, connHost, connPort, playerSlots)

	if err := srv.Run(true); err != nil {
		log.Fatal(err)
	}
}
