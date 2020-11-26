package web

import (
	"dg-server/gameboard"
	"dg-server/player"
	"dg-server/serialization"
	"dg-server/user"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net"
)

type serverConfig struct {
	ConnType string
	ConnHost string
	connPort string
}

type gameConfig struct {
	playerSlots uint8
	users       map[net.Addr]*user.User
	gameboard   gameboard.Gameboard
}

// Server contains information about the current Server
type Server struct {
	serverConfig
	gameConfig
	listener net.Listener
}

// NewServer instantiate a new server
func NewServer(connType, connHost, connPort string, playerSlots uint8) *Server {
	return &Server{
		listener: nil,
		serverConfig: serverConfig{
			ConnType: connType,
			ConnHost: connHost,
			connPort: connPort,
		},
		gameConfig: gameConfig{
			playerSlots: playerSlots,
			users:       make(map[net.Addr]*user.User),
			gameboard:   gameboard.Gameboard{},
		},
	}
}

// Run runs the Server on given protocol, host, and port
func (s *Server) Run(logging bool) (err error) {
	// Disable Logging
	if !logging {
		log.SetOutput(ioutil.Discard)
	}

	// Server Creation or error
	host := fmt.Sprintf("%v:%v", s.ConnHost, s.connPort)
	s.listener, err = net.Listen(s.ConnType, host)
	if err != nil {
		log.Fatal("Error listening server: ", err.Error())
		return
	}
	defer s.listener.Close()

	// Server Starting
	log.Printf("Listening on %v\n", s.listener.Addr())
	for {
		// Wait for Incoming Connections
		conn, err := s.listener.Accept()
		if err != nil {
			log.Fatal("Error accepting: ", err.Error())
			continue
		}

		go s.newConnection(conn)
	}
}

// Close safely terminates the running server
func (s *Server) Close() error {
	return s.listener.Close()
}

func (s *Server) newConnection(conn net.Conn) {
	addr := conn.RemoteAddr()
	err := s.newUserConnection(conn)
	if err != nil {
		log.Printf("User %v could not connect: %v", addr, err)
		return
	}

	for {
		request := serialization.NewRequest(conn)
		response := serialization.NewResponse(conn)
		if err := request.Decode(); err != nil {
			log.Printf("Invalid data from %v: %v\n", addr, err)
			response.Encode(serialization.Response{
				Result:  "error",
				Message: "Invalid data format.",
			})

			// TODO: Need more testing for users leaving correctly
			if conn.Close() == nil {
				delete(s.users, addr)
			}
			return
		}

		// Creating user or refusing conn
		user, err := s.createNewUser(conn, request.Username)
		if err != nil {
			log.Printf("User %v cannot join, cloned or invalid username.\n", addr)
			response.Encode(serialization.Response{
				Result:  "error",
				Message: "This username is either invalid or already in use.",
			})
			conn.Close()
			return
		}
		// User created
		log.Printf("User %v joined.\n", user.Username)
		response.Encode(serialization.Response{
			Result:  "success",
			Message: "Server joined.",
		})

		// Check for Full Server
		s.setupGame()

		// Actions
		switch request.Action {
		case "leave":
			log.Printf("User %v left.\n", user.Username)
			response.Encode(serialization.Response{
				Result:  "success",
				Message: "Server left.",
			})
			conn.Close()
			delete(s.users, addr)
			return
		}
	}
}

func (s *Server) setupGame() {
	// Setting up the gameboard
	if len(s.users) == int(s.playerSlots) {
		s.gameboard.PopulateGameboard(s.users)
		s.broadcastAll(serialization.Response{
			Result:  "success",
			Message: "Game Started.",
		})
	}
}

func (s *Server) newUserConnection(conn net.Conn) error {
	// Check for max user connections
	if len(s.users)+1 > int(s.playerSlots) {
		response := serialization.NewResponse(conn)
		response.Encode(serialization.Response{
			Result:  "error",
			Message: "Server Full.",
		})
		conn.Close()

		return errors.New("Server Full")
	}

	return nil
}

func (s *Server) createNewUser(conn net.Conn, username string) (*user.User, error) {
	// Add user to user map
	addr := conn.RemoteAddr()
	u, ok := s.users[addr]
	if s.validateUsername(username) && !ok {
		// User doesn't exist - creating a new one
		u = &user.User{
			Conn:     conn,
			Username: username,
			Player: &player.Player{
				AP: 5,
			},
		}
		s.users[addr] = u

		return u, nil
	}

	return nil, errors.New("user already exist")
}

func (s *Server) validateUsername(username string) bool {
	for _, user := range s.users {
		if user.Username == username {
			return false
		}
	}

	return true
}

func (s *Server) broadcast(sender *user.User, response serialization.Response) {
	for addr, user := range s.users {
		if addr != sender.Conn.RemoteAddr() {
			res := serialization.NewResponse(user.Conn)
			res.Encode(response)
		}
	}
}

func (s *Server) broadcastAll(response serialization.Response) {
	for _, user := range s.users {
		res := serialization.NewResponse(user.Conn)
		res.Encode(response)
	}
}

func (s *Server) isServerFull() bool {
	return s.playerSlots == uint8(len(s.users))
}
