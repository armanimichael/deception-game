package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

// GetEnvServerConfig reads server fields from envFileName file
func GetEnvServerConfig(envFileName string) (connType, connHost, connPort string) {
	err := godotenv.Load(envFileName)

	if err != nil {
		log.Fatal("Error loading .env file")
	}

	connType = "tcp"
	connHost = os.Getenv("HOST")
	connPort = os.Getenv("PORT")

	return
}
