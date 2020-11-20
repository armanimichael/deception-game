package main

import (
	"dg-server/config"
	"dg-server/web"
)

func main() {
	connType, connHost, connPort, playersSlots := config.GetEnvServerConfig(".server.env")
	srv := web.NewServer(connType, connHost, connPort, playersSlots)

	srv.Run()
}
