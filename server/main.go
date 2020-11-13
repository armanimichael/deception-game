package main

import (
	"dg-server/config"
	"dg-server/web"
)

func main() {
	connType, connHost, connPort := config.GetEnvServerConfig(".server.env")
	srv := web.NewServer(connType, connHost, connPort)

	srv.Run()
}
