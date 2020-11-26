package config

import (
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// GetEnvServerConfig reads server fields from envFileName file
func GetEnvServerConfig(envFileName string) (connType, connHost, connPort string, playersSlots uint8) {
	err := godotenv.Load(envFileName)

	if err != nil {
		log.Fatal("Error loading .env file")
	}

	connType = "tcp"
	connHost = os.Getenv("HOST")
	connPort = os.Getenv("PORT")
	playersSlotsStr := os.Getenv("PLAYER_SLOTS")

	pSlots, err := strconv.Atoi(playersSlotsStr)

	if err != nil {
		playersSlots = 2
	} else {
		playersSlots = uint8(pSlots)
	}

	return
}
