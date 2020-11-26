package main

import (
	"dg-server/config"
	"dg-server/web"
	"log"
)

func main() {
	connType, connHost, connPort, playersSlots := config.GetEnvServerConfig(".server.env")
	srv := web.NewServer(connType, connHost, connPort, playersSlots)

	if err := srv.Run(true); err != nil {
		log.Fatal(err)
	}
}
